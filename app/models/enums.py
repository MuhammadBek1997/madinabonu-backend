from enum import Enum

class UserRole(str, Enum):
    """Foydalanuvchi rollari"""
    SUPERADMIN = "superadmin"  # Barcha huquqlar, tizim sozlamalari
    ADMIN = "admin"            # Kontent boshqarish, foydalanuvchilar
    TEACHER = "teacher"        # Kurslar, testlar yaratish va tahrirlash
    CLIENT = "client"          # Oddiy foydalanuvchi (o'quvchi)

    @classmethod
    def has_admin_access(cls, role: str) -> bool:
        """Admin darajasidagi huquqni tekshirish"""
        return role in [cls.SUPERADMIN, cls.ADMIN]

    @classmethod
    def has_teacher_access(cls, role: str) -> bool:
        """Teacher darajasidagi huquqni tekshirish"""
        return role in [cls.SUPERADMIN, cls.ADMIN, cls.TEACHER]

    @classmethod
    def can_manage_users(cls, role: str) -> bool:
        """Foydalanuvchilarni boshqarish huquqi"""
        return role in [cls.SUPERADMIN, cls.ADMIN]

    @classmethod
    def can_create_content(cls, role: str) -> bool:
        """Kontent yaratish huquqi"""
        return role in [cls.SUPERADMIN, cls.ADMIN, cls.TEACHER]
