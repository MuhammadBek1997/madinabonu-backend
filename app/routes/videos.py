from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.video import Video, VideoCategory
from app.models.user import User
from app.schemas.video import VideoCreate, VideoResponse, VideoCategoryCreate, VideoCategoryResponse
from app.dependencies import get_current_user, require_teacher

router = APIRouter(prefix="/videos", tags=["Videos"])

# ===== VIDEO CATEGORIES =====

@router.post("/categories", response_model=VideoCategoryResponse, dependencies=[Depends(require_teacher)])
async def create_category(
    category_data: VideoCategoryCreate,
    db: Session = Depends(get_db)
):
    """Video kategoriya yaratish (Teacher+)"""
    category = VideoCategory(**category_data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories", response_model=List[VideoCategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Barcha kategoriyalarni olish"""
    return db.query(VideoCategory).order_by(VideoCategory.order).all()

# ===== VIDEOS =====

@router.post("/", response_model=VideoResponse, dependencies=[Depends(require_teacher)])
async def create_video(
    video_data: VideoCreate,
    db: Session = Depends(get_db)
):
    """Video yaratish (Teacher+)"""
    video = Video(**video_data.dict())
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

@router.get("/", response_model=List[VideoResponse])
async def get_videos(
    category_id: Optional[int] = Query(None),
    subject: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Videolarni olish (filter bilan)

    - category_id: Kategoriya bo'yicha
    - subject: Mavzu bo'yicha
    - search: Qidiruv (title, description)
    """
    query = db.query(Video).filter(Video.is_published == True)

    if category_id:
        query = query.filter(Video.category_id == category_id)
    if subject:
        query = query.filter(Video.subject == subject)
    if search:
        query = query.filter(
            (Video.title.ilike(f"%{search}%")) | (Video.description.ilike(f"%{search}%"))
        )

    return query.order_by(Video.order, Video.created_at.desc()).all()

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    """Bitta videoni olish"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video topilmadi")

    # Views count oshirish
    video.views_count += 1
    db.commit()

    return video

@router.put("/{video_id}", response_model=VideoResponse, dependencies=[Depends(require_teacher)])
async def update_video(
    video_id: int,
    video_data: VideoCreate,
    db: Session = Depends(get_db)
):
    """Video tahrirlash (Teacher+)"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video topilmadi")

    for key, value in video_data.dict(exclude_unset=True).items():
        setattr(video, key, value)

    db.commit()
    db.refresh(video)
    return video

@router.delete("/{video_id}", dependencies=[Depends(require_teacher)])
async def delete_video(video_id: int, db: Session = Depends(get_db)):
    """Video o'chirish (Teacher+)"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video topilmadi")

    db.delete(video)
    db.commit()
    return {"message": "Video o'chirildi"}
