# 🔧 GITHUB PUSH XATOSINI TUZATISH

**Xato:**
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/Bahriddin2005/buxoro-maktab'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

**Sabab:** GitHub'da allaqachon fayllar mavjud (README, .gitignore, LICENSE)

---

## ✅ YECHIM: Qadamma-Qadam

### Qadam 1: GitHub'dan fayllarni pull qiling

Terminal'da quyidagi comandani bajaring:

```bash
cd /Users/macbookpro/Downloads/buxoro-maktab-main

git pull origin main --allow-unrelated-histories
```

**Username va Password so'raladi:**
- **Username:** `Bahriddin2005`
- **Password:** Personal Access Token (PAT)

### Qadam 2: Merge qiling

Agar conflict bo'lmasa:
```bash
# Avtomatik merge bo'ladi
```

Agar conflict bo'lsa:
```bash
# Conflict'larni qo'lda hal qiling
# Keyin:
git add .
git commit -m "Merge remote changes"
```

### Qadam 3: Push qiling

```bash
git push origin main
```

---

## 🎯 VARIANT 2: Force Push (EHTIYOTKOR!)

Agar GitHub'dagi fayllar kerak bo'lmasa:

```bash
git push origin main --force
```

⚠️ **OGOHLANTIRISH:** Bu GitHub'dagi barcha fayllarni o'chiradi!

---

## 🎯 VARIANT 3: GitHub'dagi fayllarni saqlab qolish

### 1. GitHub'dan fayllarni pull qiling:

```bash
cd /Users/macbookpro/Downloads/buxoro-maktab-main

git pull origin main --allow-unrelated-histories --no-edit
```

### 2. Agar merge commit kerak bo'lsa:

```bash
# Avtomatik merge message yaratiladi
```

### 3. Push qiling:

```bash
git push origin main
```

---

## 📝 TAVSIYA ETILGAN YO'L

### Qadam 1: Pull (Merge)

```bash
cd /Users/macbookpro/Downloads/buxoro-maktab-main

git pull origin main --allow-unrelated-histories
```

**So'ralganda:**
- Username: `Bahriddin2005`
- Password: `your_personal_access_token`

### Qadam 2: Conflict'larni tekshirish

```bash
git status
```

Agar conflict bo'lsa:
```bash
# Conflict'li fayllarni ochib tuzating
# Keyin:
git add .
git commit -m "Resolved merge conflicts"
```

### Qadam 3: Push

```bash
git push origin main
```

---

## 🔑 Personal Access Token (PAT)

Agar PAT yo'q bo'lsa:

1. **GitHub → Settings → Developer settings**
2. **Personal access tokens → Tokens (classic)**
3. **Generate new token (classic)**
4. **Scopes:** ✅ `repo`
5. **Generate token**
6. **Token'ni ko'chirib saqlang!**

---

## 🚀 TO'LIQ BUYRUQLAR (COPY-PASTE)

```bash
# 1. Directory'ga kirish
cd /Users/macbookpro/Downloads/buxoro-maktab-main

# 2. Remote fayllarni pull qilish
git pull origin main --allow-unrelated-histories

# 3. Status tekshirish
git status

# 4. Agar conflict bo'lmasa, push qiling
git push origin main
```

---

## ❓ TANLASH

### Option A: GitHub fayllarini saqlab qolish
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Option B: Faqat local fayllarni yuklash (GitHub fayllarini o'chirish)
```bash
git push origin main --force
```

---

## ✅ MUVAFFAQIYATLI PUSH

Muvaffaqiyatli push qilinganda ko'rasiz:

```
To https://github.com/Bahriddin2005/buxoro-maktab
   1234567..89abcdef  main -> main
```

---

## 🌐 GitHub Repository

```
https://github.com/Bahriddin2005/buxoro-maktab
```

---

**Omad!** 🚀

