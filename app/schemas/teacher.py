from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ============ Teacher Schemas ============

class TeacherBase(BaseModel):
    """Base Teacher schema"""
    full_name: str = Field(..., min_length=1, max_length=255)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    experience_years: int = Field(default=0, ge=0)

class TeacherCreate(TeacherBase):
    """Create Teacher - Admin+ only"""
    user_id: int

class TeacherUpdate(BaseModel):
    """Update Teacher profile"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0)

class TeacherResponse(TeacherBase):
    """Teacher response with full info"""
    id: int
    user_id: int
    rating: float
    total_students: int
    total_videos: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TeacherListItem(BaseModel):
    """Minimal teacher info for lists"""
    id: int
    full_name: str
    avatar_url: Optional[str] = None
    experience_years: int
    rating: float
    total_videos: int

    class Config:
        from_attributes = True

# ============ Subject Schemas ============

class SubjectBase(BaseModel):
    """Base Subject schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    order: int = Field(default=0, ge=0)

class SubjectCreate(SubjectBase):
    """Create new subject - Admin+ only"""
    pass

class SubjectUpdate(BaseModel):
    """Update subject"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class SubjectResponse(SubjectBase):
    """Subject response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============ TeacherSubject Schemas ============

class TeacherSubjectCreate(BaseModel):
    """Assign teacher to subject"""
    teacher_id: int
    subject_id: int

class TeacherSubjectResponse(BaseModel):
    """TeacherSubject response"""
    id: int
    teacher_id: int
    subject_id: int
    created_at: datetime

    class Config:
        from_attributes = True