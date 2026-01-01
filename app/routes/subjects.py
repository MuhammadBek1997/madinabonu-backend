from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.subject import Subject, TeacherSubject
from app.models.teacher import Teacher
from app.schemas.teacher import SubjectCreate, SubjectUpdate, SubjectResponse, TeacherListItem
from app.dependencies import require_admin

router = APIRouter(prefix="/subjects", tags=["Subjects"])

# ============ SUBJECT CRUD ============

@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Yangi fan yaratish

    **Faqat ADMIN va SUPERADMIN uchun.**
    """

    # Fan nomi mavjudligini tekshirish
    existing_subject = db.query(Subject).filter(Subject.name == subject_data.name).first()
    if existing_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu nomli fan allaqachon mavjud"
        )

    # Yangi fan yaratish
    new_subject = Subject(**subject_data.model_dump())

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject

@router.get("/", response_model=List[SubjectResponse])
async def get_all_subjects(
    is_active: Optional[bool] = Query(None, description="Faol fanlarni filter qilish"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Barcha fanlarni olish

    **Public endpoint** - hamma ko'ra oladi.
    is_active parametri orqali faqat faol fanlarni ko'rish mumkin.
    """

    query = db.query(Subject)

    # Faol fanlar filteri
    if is_active is not None:
        query = query.filter(Subject.is_active == is_active)

    # Tartib bo'yicha
    query = query.order_by(Subject.order.asc(), Subject.name.asc())

    subjects = query.offset(offset).limit(limit).all()
    return subjects

@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject_by_id(
    subject_id: int,
    db: Session = Depends(get_db)
):
    """
    Fan ma'lumotlarini ID bo'yicha olish

    **Public endpoint** - hamma ko'ra oladi.
    """

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fan topilmadi"
        )

    return subject

@router.patch("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: int,
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Fanni yangilash

    **Faqat ADMIN va SUPERADMIN uchun.**
    """

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fan topilmadi"
        )

    # Agar nom o'zgartirilsa, mavjudligini tekshirish
    if subject_data.name and subject_data.name != subject.name:
        existing = db.query(Subject).filter(Subject.name == subject_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu nomli fan allaqachon mavjud"
            )

    # Ma'lumotlarni yangilash
    update_data = subject_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subject, field, value)

    db.commit()
    db.refresh(subject)

    return subject

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Fanni o'chirish

    **Faqat ADMIN va SUPERADMIN uchun.**
    """

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fan topilmadi"
        )

    db.delete(subject)
    db.commit()

    return None

# ============ SUBJECT TEACHERS ============

@router.get("/{subject_id}/teachers", response_model=List[TeacherListItem])
async def get_subject_teachers(
    subject_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Fanni o'qitadigan barcha o'qituvchilarni olish

    **Public endpoint** - hamma ko'ra oladi.
    Ma'lum fan bo'yicha o'qituvchilar ro'yxati.
    """

    # Subject mavjudligini tekshirish
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fan topilmadi"
        )

    # O'qituvchilarni olish
    teachers = db.query(Teacher).join(TeacherSubject).filter(
        TeacherSubject.subject_id == subject_id
    ).offset(offset).limit(limit).all()

    return teachers