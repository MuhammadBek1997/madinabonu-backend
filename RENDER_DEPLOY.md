# 🚀 Render.com ga Deploy Qilish Qo'llanmasi

## 📋 Tayyor Fayllar

✅ `render.yaml` - Render konfiguratsiya
✅ `build.sh` - Build script
✅ `requirements.txt` - Python dependencies
✅ `Procfile` - Fallback
✅ `.env.example` - Environment variables namuna

---

## 🌐 Render.com ga Deploy

### 1️⃣ **Render.com ga Kirish**

1. [https://render.com](https://render.com) ga kiring
2. Sign up/Login (GitHub bilan login qilish tavsiya etiladi)

---

### 2️⃣ **GitHub Repository Yaratish**

Agar GitHub repo yo'q bo'lsa:

```bash
cd MadinabonuBackend

# Git init
git init
git add .
git commit -m "Initial commit - MadinabonuBackend"

# GitHub da yangi repo yarating, keyin:
git remote add origin https://github.com/username/madinabonu-backend.git
git branch -M main
git push -u origin main
```

---

### 3️⃣ **Render da New Web Service Yaratish**

#### A. Dashboard dan:
1. Render Dashboard → **New +** → **Web Service**
2. **Connect GitHub repository** → `madinabonu-backend` ni tanlang
3. Yoki **Public Git Repository** ga repo URL kiriting

#### B. Sozlamalar:

**Build & Deploy:**
- **Name:** `madinabonu-backend`
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh` yoki `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- **Instance Type:** Free

---

### 4️⃣ **Environment Variables Sozlash**

Render Dashboard → Web Service → **Environment** bo'limida:

#### Kerakli Variables:

```env
# Database (Render PostgreSQL dan olasiz)
DATABASE_URL=postgresql://user:password@host/database

# JWT Secret (random string)
SECRET_KEY=your-super-secret-key-here-at-least-32-characters-long

# App Settings
APP_NAME=Madinabonu
API_VERSION=v1
DEBUG=False

# CORS (frontend URL)
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# AWS S3 (agar kerak bo'lsa)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_KEY=your-secret
S3_REGION=us-east-1
S3_BUCKET_NAME=madinabonu-videos
```

**Auto-generate SECRET_KEY:**
Render da `SECRET_KEY` ni **Generate** tugmasini bosing - avtomatik yaratadi.

---

### 5️⃣ **PostgreSQL Database Qo'shish**

#### A. Render Dashboard:
1. **New +** → **PostgreSQL**
2. **Name:** `madinabonu-db`
3. **Database Name:** `madinabonu`
4. **Plan:** Free
5. **Create Database**

#### B. Internal Connection String Olish:
1. PostgreSQL dashboard → **Info** tab
2. **Internal Database URL** ni ko'chirib oling
3. Web Service → Environment → `DATABASE_URL` ga qo'ying

**Misol:**
```
postgresql://madinabonu_user:***@dpg-xxx-a.oregon-postgres.render.com/madinabonu_db
```

---

### 6️⃣ **Deploy Qilish**

1. **Manual Deploy:** Render Dashboard → **Manual Deploy** → **Deploy latest commit**
2. **Auto Deploy:** Har git push da avtomatik deploy bo'ladi

**Deploy logs ko'rish:**
- **Logs** tab da real-time ko'rishingiz mumkin

---

## 🔍 **Deploy Muvaffaqiyatli Bo'lgach**

### Sizning API URL:
```
https://madinabonu-backend.onrender.com
```

### Swagger UI:
```
https://madinabonu-backend.onrender.com/docs
```

### ReDoc:
```
https://madinabonu-backend.onrender.com/redoc
```

### Health Check:
```
https://madinabonu-backend.onrender.com/
```

---

## 🖥️ **Render Shell (Terminal) ga Ulanish**

### **Web Dashboard orqali:**

1. Render Dashboard → Web Service tanlang
2. Yuqori o'ng burchakda **Shell** tugmasini bosing
3. Terminal ochiladi ✅

### **Shell Commands:**

```bash
# Python shell
python

# Database migration
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Superadmin yaratish
python -c "
from app.models.user import User
from app.models.enums import UserRole
from app.utils import hash_password
from app.database import SessionLocal

db = SessionLocal()
admin = User(
    username='superadmin',
    email='admin@madinabonu.uz',
    full_name='Super Admin',
    hashed_password=hash_password('admin123'),
    role=UserRole.SUPERADMIN,
    is_active=True
)
db.add(admin)
db.commit()
print('✅ Superadmin created!')
"

# Logs ko'rish
tail -f /var/log/render.log

# Environment variables ko'rish
env | grep DATABASE
```

---

## 🛠️ **Troubleshooting**

### 1. **Build Failed**

**Xato:** `Error: No module named 'app'`

**Yechim:**
```bash
# render.yaml tekshiring
# Start command to'g'ri:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2. **Database Connection Error**

**Xato:** `connection refused`

**Yechim:**
- `DATABASE_URL` to'g'ri ekanligini tekshiring
- Internal Database URL ishlatilganligini tasdiqlang
- SSL mode: Render PostgreSQL avtomatik SSL ishlatadi

### 3. **CORS Error**

**Xato:** `CORS policy blocked`

**Yechim:**
```env
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

### 4. **Swagger UI ko'rinmayapti**

**Yechim:**
- `/docs` ga boring: `https://your-app.onrender.com/docs`
- `DEBUG=False` bo'lsa ham Swagger ishlaydi (FastAPI default)

---

## 📊 **Monitoring**

### Render Dashboard:
- **Metrics:** CPU, Memory, Requests
- **Logs:** Real-time logs
- **Events:** Deploy tarixi

### Logs ko'rish:
```bash
# Shell da
tail -f /opt/render/project/src/logs/app.log
```

---

## 🔄 **Yangilanishlar Deploy Qilish**

### Git orqali:
```bash
git add .
git commit -m "Update: yangi feature qo'shildi"
git push origin main
```

Render avtomatik deploy qiladi!

### Manual:
Render Dashboard → **Manual Deploy** → **Clear build cache & deploy**

---

## 🎯 **Birinchi Superadmin Yaratish**

Deploy bo'lgach, Shell da:

```bash
python << 'EOF'
from app.models.user import User
from app.models.enums import UserRole
from app.utils import hash_password
from app.database import SessionLocal

db = SessionLocal()

# Superadmin yaratish
admin = User(
    username="superadmin",
    email="admin@madinabonu.uz",
    full_name="Super Administrator",
    hashed_password=hash_password("SecurePassword123!"),
    role=UserRole.SUPERADMIN,
    is_active=True
)

db.add(admin)
db.commit()
db.close()

print("✅ Superadmin successfully created!")
print("Username: superadmin")
print("Password: SecurePassword123!")
EOF
```

---

## 🧪 **API Test Qilish**

### cURL:
```bash
# Health check
curl https://madinabonu-backend.onrender.com/

# Login
curl -X POST https://madinabonu-backend.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"superadmin","password":"SecurePassword123!"}'

# Get current user
curl https://madinabonu-backend.onrender.com/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Python:
```python
import requests

BASE_URL = "https://madinabonu-backend.onrender.com"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "superadmin",
    "password": "SecurePassword123!"
})
token = response.json()["access_token"]

# Get videos
headers = {"Authorization": f"Bearer {token}"}
videos = requests.get(f"{BASE_URL}/videos", headers=headers)
print(videos.json())
```

---

## 📱 **Frontend Integratsiya**

React/React Native:

```javascript
// config.js
export const API_URL = "https://madinabonu-backend.onrender.com";

// api.js
import axios from 'axios';
import { API_URL } from './config';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

---

## ⚡ **Performance Tips**

1. **Free plan limitations:**
   - Sleep after 15 min inactivity
   - 750 hours/month free

2. **Keep alive:**
   - Cron job har 10 daqiqada ping qilish
   - UptimeRobot.com ishlatish

3. **Caching:**
   - Redis qo'shish (Render Redis addon)

---

## 📞 **Yordam**

- Render Docs: https://render.com/docs
- Discord: https://discord.gg/render
- GitHub Issues: Repository issues section

**Muvaffaqiyatli deploy! 🎉**