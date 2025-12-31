from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.test import Test, TestQuestion, TestResult
from app.models.user import User
from app.schemas.test import TestCreate, TestResponse, TestResultCreate, TestResultResponse
from app.dependencies import get_current_user, require_teacher

router = APIRouter(prefix="/tests", tags=["Tests"])

@router.post("/", response_model=TestResponse, dependencies=[Depends(require_teacher)])
async def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db)
):
    """Test yaratish (Teacher+)"""

    # Test yaratish
    test = Test(
        title=test_data.title,
        description=test_data.description,
        video_id=test_data.video_id,
        category=test_data.category,
        subject=test_data.subject,
        time_limit=test_data.time_limit,
        passing_score=test_data.passing_score,
        is_published=test_data.is_published
    )
    db.add(test)
    db.flush()  # ID olish uchun

    # Savollarni qo'shish
    for q_data in test_data.questions:
        question = TestQuestion(
            test_id=test.id,
            **q_data.dict()
        )
        db.add(question)

    db.commit()
    db.refresh(test)
    return test

@router.get("/", response_model=List[TestResponse])
async def get_tests(
    category: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    video_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Testlarni olish (filter bilan)"""
    query = db.query(Test).filter(Test.is_published == True)

    if category:
        query = query.filter(Test.category == category)
    if subject:
        query = query.filter(Test.subject == subject)
    if video_id:
        query = query.filter(Test.video_id == video_id)

    return query.order_by(Test.created_at.desc()).all()

@router.get("/{test_id}", response_model=TestResponse)
async def get_test(test_id: int, db: Session = Depends(get_db)):
    """Bitta testni olish"""
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")
    return test

@router.post("/submit", response_model=TestResultResponse)
async def submit_test(
    result_data: TestResultCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Test natijasini yuborish"""

    # Testni topish
    test = db.query(Test).filter(Test.id == result_data.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")

    # Savollarni olish
    questions = db.query(TestQuestion).filter(TestQuestion.test_id == test.id).order_by(TestQuestion.order).all()

    if len(result_data.answers) != len(questions):
        raise HTTPException(status_code=400, detail="Javoblar soni savollar soniga mos emas")

    # Natijani hisoblash
    score = 0
    for i, question in enumerate(questions):
        if i < len(result_data.answers) and result_data.answers[i] == question.correct_answer:
            score += 1

    total_questions = len(questions)
    percentage = int((score / total_questions) * 100) if total_questions > 0 else 0
    passed = percentage >= test.passing_score

    # Natijani saqlash
    test_result = TestResult(
        user_id=current_user.id,
        test_id=test.id,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        time_spent=result_data.time_spent,
        passed=passed,
        answers=result_data.answers
    )

    db.add(test_result)
    db.commit()
    db.refresh(test_result)

    return test_result

@router.get("/results/me", response_model=List[TestResultResponse])
async def get_my_results(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """O'zimning test natijalarim"""
    results = db.query(TestResult).filter(
        TestResult.user_id == current_user.id
    ).order_by(TestResult.created_at.desc()).all()

    return results

@router.delete("/{test_id}", dependencies=[Depends(require_teacher)])
async def delete_test(test_id: int, db: Session = Depends(get_db)):
    """Test o'chirish (Teacher+)"""
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")

    db.delete(test)
    db.commit()
    return {"message": "Test o'chirildi"}
