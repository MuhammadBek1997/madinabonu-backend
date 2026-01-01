from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.teacher import Teacher
from app.models.subject import Subject, TeacherSubject
from app.schemas.teacher import (
    TeacherCreate, TeacherUpdate, TeacherResponse, TeacherListItem,
    TeacherSubjectCreate, TeacherSubjectResponse
)
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/teachers", tags=["Teachers"])

# ============ TEACHER CRUD ============

@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    O'qituvchi profili yaratish

    **Faqat ADMIN va SUPERADMIN uchun.**
    User_id orqali mavjud foydalanuvchiga Teacher profili biriktiradi.
    """

    # User mavjudligini tekshirish
    user = db.query(User).filter(User.id == teacher_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi"
        )

    # Teacher profili allaqachon mavjudligini tekshirish
    existing_teacher = db.query(Teacher).filter(Teacher.user_id == teacher_data.user_id).first()
    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu foydalanuvchi uchun teacher profili allaqachon mavjud"
        )

    # Yangi Teacher yaratish
    new_teacher = Teacher(
        user_id=teacher_data.user_id,
        full_name=teacher_data.full_name,
        bio=teacher_data.bio,
        avatar_url=teacher_data.avatar_url,
        experience_years=teacher_data.experience_years
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher

@router.get("/", response_model=List[TeacherListItem])
async def get_all_teachers(
    subject_id: Optional[int] = Query(None, description="Fan bo'yicha filter"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Barcha o'qituvchilarni olish

    **Public endpoint** - hamma ko'ra oladi.
    Subject_id orqali ma'lum fanni o'qitadigan o'qituvchilarni filter qilish mumkin.
    """

    query = db.query(Teacher)

    # Fan bo'yicha filter
    if subject_id:
        query = query.join(TeacherSubject).filter(TeacherSubject.subject_id == subject_id)

    teachers = query.offset(offset).limit(limit).all()
    return teachers

@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_by_id(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    """
    O'qituvchi ma'lumotlarini ID bo'yicha olish

    **Public endpoint** - hamma ko'ra oladi.
    """

    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O'qituvchi topilmadi"
        )

    return teacher

@router.patch("/{teacher_id}", response_model=TeacherResponse)
async def update_teacher(
    teacher_id: int,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    O'qituvchi profilini yangilash

    Teacher o'zining profilini yoki Admin+ boshqa teacherning profilini yangilashi mumkin.
    """

    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O'qituvchi topilmadi"
        )

    # Huquqni tekshirish: o'zining profili yoki Admin+
    if teacher.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sizda bu profilni tahrirlash huquqi yo'q"
        )

    # Ma'lumotlarni yangilash
    update_data = teacher_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(teacher, field, value)

    db.commit()
    db.refresh(teacher)

    return teacher

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    O'qituvchi profilini o'chirish

    **Faqat ADMIN va SUPERADMIN uchun.**
    """

    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O'qituvchi topilmadi"
        )

    db.delete(teacher)
    db.commit()

    return None

# ============ TEACHER-SUBJECT ASSIGNMENT ============

@router.post("/subjects/assign", response_model=TeacherSubjectResponse, status_code=status.HTTP_201_CREATED)
async def assign_teacher_to_subject(
    assignment: TeacherSubjectCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    O'qituvchini fanga birikitirish

    **Faqat ADMIN va SUPERADMIN uchun.**
    """

    # Teacher mavjudligini tekshirish
    teacher = db.query(Teacher).filter(Teacher.id == assignment.teacher_id).first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O'qituvchi topilmadi"
        )

    # Subject mavjudligini tekshirish
    subject = db.query(Subject).filter(Subject.id == assignment.subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fan topilmadi"
        )

    # Allaqachon biriktirilganligini tekshirish
    existing = db.query(TeacherSubject).filter(
        TeacherSubject.teacher_id == assignment.teacher_id,
        TeacherSubject.subject_id == assignment.subject_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu o'qituvchi allaqachon ushbu fanga biriktirilgan"
        )

    # Yangi biriktirish
    new_assignment = TeacherSubject(
        teacher_id=assignment.teacher_id,
        subject_id=assignment.subject_id
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment

@router.delete("/subjects/unassign/{teacher_id}/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unassign_teacher_from_subject(
    teacher_id: int,
    subject_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    O'qituvchini fandan ajratish

    **Faqat ADMIN va SUPERADMIN uchun.**
    """

    assignment = db.query(TeacherSubject).filter(
        TeacherSubject.teacher_id == teacher_id,
        TeacherSubject.subject_id == subject_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bunday biriktirish topilmadi"
        )

    db.delete(assignment)
    db.commit()

    return None

@router.get("/{teacher_id}/subjects", response_model=List[int])
async def get_teacher_subjects(
    teacher_id: int,
    db: Session = Depends(get_db)
):
    """
    O'qituvchining barcha fanlarini olish

    **Public endpoint** - subject_id larni qaytaradi.
    """

    assignments = db.query(TeacherSubject).filter(TeacherSubject.teacher_id == teacher_id).all()
    subject_ids = [assignment.subject_id for assignment in assignments]

    return subject_ids