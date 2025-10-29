# 🚀 GITHUB'GA PUSH QILISH QO'LLANMASI

**Proyekt:** Buxoro Bilimdonlar Maktabi - Test Platformasi  
**Sana:** 29 Oktabr, 2025

---

## 📋 BOSHLASH OLDI

### 1. GitHub Account
- ✅ GitHub accountingiz bo'lishi kerak: https://github.com
- ✅ Login qiling

### 2. Personal Access Token (Tavsiya etiladi)
GitHub password o'rniga Personal Access Token ishlatish xavfsizroq.

---

## 🎯 VARIANT 1: TERMINAL ORQALI (TEZKOR)

### Qadam 1: GitHub'da Yangi Repository Yaratish

1. **GitHub'ga kiring:** https://github.com
2. **Yangi repository yaratish:**
   - Yuqori o'ng burchakda `+` → `New repository`
   - **Repository name:** `buxoro-maktab` (yoki boshqa nom)
   - **Description:** "Buxoro Bilimdonlar Maktabi - Test Platformasi"
   - **Visibility:** 
     - ✅ **Private** (maxfiy) - Tavsiya etiladi
     - ⚠️ **Public** (ochiq) - Barchaga ko'rinadi
   - ❌ **README, .gitignore, license qo'shmang** (bizda bor)
   - `Create repository` tugmasini bosing

### Qadam 2: Terminal'da Comandalarni Bajaring

GitHub sizga comandalar ko'rsatadi. Quyidagi comandalarni bajaring:

```bash
cd /Users/macbookpro/Downloads/buxoro-maktab-main

# GitHub repository URL'ini qo'shish
# URL'ni GitHub sahifasidan ko'chirib oling!
git remote add origin https://github.com/YOUR_USERNAME/buxoro-maktab.git

# Branch nomini main ga o'zgartirish (agar kerak bo'lsa)
git branch -M main

# GitHub'ga push qilish
git push -u origin main
```

**MUHIM:** `YOUR_USERNAME` ni o'z GitHub username'ingizga almashtiring!

---

## 🎯 VARIANT 2: CURSOR ORQALI (OSon)

### Qadam 1: GitHub'da Repository Yarating
Yuqoridagi `VARIANT 1, Qadam 1`ni bajaring.

### Qadam 2: Cursor'da Git Remote Qo'shing

Cursor terminalida:

```bash
# 1. Remote qo'shish
git remote add origin https://github.com/YOUR_USERNAME/buxoro-maktab.git

# 2. Remote tekshirish
git remote -v

# 3. Push qilish
git push -u origin main
```

### Agar Login So'ralsa:

**Username:** GitHub username'ingiz  
**Password:** Personal Access Token (PAT) - Quyida ko'ramiz

---

## 🔑 PERSONAL ACCESS TOKEN (PAT) YARATISH

GitHub password o'rniga PAT ishlatish kerak (2021 yildan beri).

### Qadam 1: GitHub Settings
1. GitHub'da yuqori o'ng burchakdagi profil rasmingizni bosing
2. `Settings` → `Developer settings` (pastda)
3. `Personal access tokens` → `Tokens (classic)`
4. `Generate new token` → `Generate new token (classic)`

### Qadam 2: Token Sozlamalari
- **Note:** "Buxoro Maktab - Cursor"
- **Expiration:** 90 days yoki No expiration
- **Scopes (Permissions):**
  - ✅ `repo` (Barcha repo permissions)
  - ✅ `workflow` (Agar GitHub Actions bo'lsa)

### Qadam 3: Token Yaratish
- `Generate token` tugmasini bosing
- **Token'ni ko'chirib oling va xavfsiz joyga saqlang!**
- ⚠️ **Token faqat bir marta ko'rinadi!**

### Qadam 4: Token Ishlatish

Push qilganda password so'ralsa, PAT'ni kiriting:

```bash
Username: your_github_username
Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx  # PAT ni joylashtiring
```

---

## 🚀 TO'LIQ PUSH QILISH JARAYONI

### Tayyorgarlik:

```bash
cd /Users/macbookpro/Downloads/buxoro-maktab-main

# 1. Git status tekshirish
git status

# 2. O'zgarishlarni qo'shish
git add .

# 3. Commit qilish
git commit -m "Initial commit: Buxoro Bilimdonlar Maktabi Test Platform"

# 4. Remote qo'shish (faqat bir marta)
git remote add origin https://github.com/YOUR_USERNAME/buxoro-maktab.git

# 5. Push qilish
git push -u origin main
```

---

## 📝 .GITIGNORE TEKSHIRISH

`.gitignore` fayli allaqachon yaratilgan! U quyidagilarni ignore qiladi:

✅ `venv/` - Virtual environment  
✅ `__pycache__/` - Python cache  
✅ `*.pyc` - Python bytecode  
✅ `db.sqlite3` - Database (maxfiy ma'lumotlar)  
✅ `*.log` - Log files  
✅ `.env` - Environment variables  
✅ `media/` - User uploaded files  

---

## ⚠️ MUHIM XAVFSIZLIK

### GitHub'ga PUSH QILMASLIK KERAK:

❌ `db.sqlite3` - Database (foydalanuvchi ma'lumotlari)  
❌ `db_backup.sqlite3` - Backup database  
❌ `.env` - Environment variables  
❌ `SECRET_KEY` - Django secret key  
❌ `venv/` - Virtual environment  
❌ `*.log` - Log files  

`.gitignore` fayli bularni avtomatik ignore qiladi! ✅

---

## 🔧 MUAMMOLARNI HAL QILISH

### Problem 1: "Permission denied"

**Yechim:** Personal Access Token (PAT) ishlatish

### Problem 2: "fatal: remote origin already exists"

```bash
# Eski remote'ni o'chirish
git remote remove origin

# Yangi remote qo'shish
git remote add origin https://github.com/YOUR_USERNAME/buxoro-maktab.git
```

### Problem 3: "Updates were rejected"

```bash
# GitHub'dan oldin pull qilish
git pull origin main --allow-unrelated-histories

# Keyin push qilish
git push -u origin main
```

### Problem 4: "Username for 'https://github.com':"

Bu normal! Username va PAT kiriting.

---

## 📊 KEYINGI O'ZGARISHLARNI PUSH QILISH

Kelajakda o'zgarishlar qilganingizda:

```bash
# 1. Status tekshirish
git status

# 2. O'zgargan fayllarni qo'shish
git add .

# 3. Commit qilish
git commit -m "O'zgarish tavsifi"

# 4. Push qilish
git push origin main
```

---

## 🎯 QISQA BUYRUQLAR

### Birinchi marta push qilish:

```bash
cd /Users/macbookpro/Downloads/buxoro-maktab-main
git remote add origin https://github.com/YOUR_USERNAME/buxoro-maktab.git
git branch -M main
git push -u origin main
```

### Keyingi push'lar:

```bash
cd /Users/macbookpro/Downloads/buxoro-maktab-main
git add .
git commit -m "O'zgarish tavsifi"
git push
```

---

## ✅ CURSOR'DA GIT

### Cursor'da Git boshqarish:

1. **Source Control (Git):**
   - Chap panelda Git belgisi (3-branch icon)
   - O'zgargan fayllar ko'rinadi

2. **Staging:**
   - `+` belgisini bosib fayllarni stage qiling

3. **Commit:**
   - Yuqoridagi input'ga commit message yozing
   - ✓ (checkmark) bosing

4. **Push:**
   - `...` → `Push` yoki `Sync Changes`

---

## 🌐 GITHUB REPOSITORY LINKI

Push qilgandan keyin, GitHub repositoryingizga kiring:

```
https://github.com/YOUR_USERNAME/buxoro-maktab
```

Bu yerda:
- ✅ Kodlaringiz ko'rinadi
- ✅ Commit history
- ✅ Branch'lar
- ✅ README.md ko'rinadi

---

## 📞 YORDAM

### GitHub Documentation:
- https://docs.github.com/en/get-started

### Personal Access Token:
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

### Git Tutorial:
- https://git-scm.com/doc

---

## 🎉 TAYYOR!

Endi siz:
1. ✅ GitHub'da repository yaratdingiz
2. ✅ Local repository'ni GitHub'ga bog'ladingiz
3. ✅ Push qildingiz
4. ✅ Kodlaringiz GitHub'da!

**Tabriklaymiz!** 🎊

---

## 📝 KEYINGI QADAMLAR

### 1. README.md ni yangilash
```bash
# GitHub'da README.md faylini tahrirlang
# Proyekt haqida to'liqroq ma'lumot qo'shing
```

### 2. Collaborators qo'shish
```bash
# Repository Settings → Collaborators
# Boshqa dasturchilarni qo'shing
```

### 3. Branch strategiyasi
```bash
# Development branch yaratish
git checkout -b development
git push -u origin development
```

---

**Muallif:** AI Assistant  
**Proyekt:** Buxoro Bilimdonlar Maktabi  
**Sana:** 29 Oktabr, 2025

© 2025 Buxoro Bilimdonlar Maktabi

