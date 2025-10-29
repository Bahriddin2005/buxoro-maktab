#!/bin/bash

echo "=================================================="
echo "🚀 GITHUB'GA PUSH QILISH SCRIPTI"
echo "=================================================="
echo ""

# GitHub repository URL'ni so'rash
echo "📝 GitHub repository URL'ingizni kiriting:"
echo "   Misol: https://github.com/username/buxoro-maktab.git"
read -p "URL: " GITHUB_URL

if [ -z "$GITHUB_URL" ]; then
    echo "❌ URL kiritilmadi!"
    exit 1
fi

echo ""
echo "🔄 Remote qo'shilmoqda..."

# Eski remote'ni o'chirish (agar mavjud bo'lsa)
git remote remove origin 2>/dev/null

# Yangi remote qo'shish
git remote add origin "$GITHUB_URL"

echo "✅ Remote qo'shildi: $GITHUB_URL"
echo ""

# Remote tekshirish
echo "📍 Remote tekshirilmoqda..."
git remote -v
echo ""

# Branch tekshirish
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📌 Joriy branch: $CURRENT_BRANCH"
echo ""

# Push qilish
echo "🚀 GitHub'ga push qilinmoqda..."
echo "   (Username va Personal Access Token so'ralishi mumkin)"
echo ""

git push -u origin "$CURRENT_BRANCH"

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ MUVAFFAQIYATLI PUSH QILINDI!"
    echo "=================================================="
    echo ""
    echo "🌐 Repository manzilingiz:"
    echo "   ${GITHUB_URL%.git}"
    echo ""
else
    echo ""
    echo "❌ Push qilishda xatolik yuz berdi!"
    echo ""
    echo "Yordam:"
    echo "  1. GitHub'da repository yaratilganligini tekshiring"
    echo "  2. Personal Access Token (PAT) to'g'ri kiritilganligini tekshiring"
    echo "  3. GITHUB_PUSH_QOLLANMA.md faylini o'qing"
fi
