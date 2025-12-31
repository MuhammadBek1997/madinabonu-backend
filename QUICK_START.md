# ⚡ Quick Start - Render.com

## 🎯 5 Daqiqada Deploy

### 1. GitHub Push
```bash
git add .
git commit -m "Ready for deploy"
git push origin main
```

### 2. Render.com da Service Yaratish
1. [render.com](https://render.com) → Login
2. **New +** → **Web Service**
3. GitHub repo ni connect qiling
4. **Create Web Service**

### 3. Environment Variables
```env
DATABASE_URL=<render-postgres-url>
SECRET_KEY=<auto-generate>
CORS_ORIGINS=https://your-frontend.vercel.app
```

### 4. PostgreSQL Qo'shish
1. **New +** → **PostgreSQL** → Free plan
2. Internal URL ni copy qiling
3. Web Service → Environment → DATABASE_URL ga qo'ying

### 5. Deploy!
**Manual Deploy** → Deploy latest commit

---

## 🖥️ Render Shell Commands

### Deploy bo'lgach Shell ni oching:

**Dashboard → Shell tugmasi**

#### 1. Superadmin yaratish:
```bash
python setup_initial_data.py
```

#### 2. Manual command:
```bash
python << 'EOF'
from app.models.user import User
from app.models.enums import UserRole
from app.utils import hash_password
from app.database import SessionLocal

db = SessionLocal()
admin = User(
    username="superadmin",
    email="admin@madinabonu.uz",
    full_name="Super Admin",
    hashed_password=hash_password("admin123"),
    role=UserRole.SUPERADMIN,
    is_active=True
)
db.add(admin)
db.commit()
print("✅ Done!")
EOF
```

#### 3. Database tekshirish:
```bash
python << 'EOF'
from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
users = db.query(User).all()
for u in users:
    print(f"{u.username} - {u.role}")
EOF
```

#### 4. Logs ko'rish:
```bash
# Real-time logs
tail -f /var/log/render.log

# Environment
env | grep DATABASE
```

---

## 🌐 API URLs

Deployed URL: `https://your-app.onrender.com`

- **Health:** `/`
- **Swagger:** `/docs` ⭐
- **ReDoc:** `/redoc`
- **API Info:** `/api/info`

---

## 🧪 Test Qilish

### Browser:
```
https://your-app.onrender.com/docs
```

### cURL:
```bash
curl https://your-app.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"superadmin","password":"admin123"}'
```

---

## 🔧 Troubleshooting

### Build failed?
- Check `requirements.txt`
- Shell: `pip list`

### Database error?
- Check `DATABASE_URL` in Environment
- Shell: `python -c "from app.database import engine; print(engine.url)"`

### Swagger yo'q?
- `/docs` ga boring
- Shell: `curl http://localhost:$PORT/docs`

---

## 📞 Yordam

Muammo? → [RENDER_DEPLOY.md](RENDER_DEPLOY.md) ga qarang!