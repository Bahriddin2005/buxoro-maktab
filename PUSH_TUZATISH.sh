#!/bin/bash

echo "=================================================="
echo "🔧 GITHUB PUSH XATOSINI TUZATISH"
echo "=================================================="
echo ""

cd /Users/macbookpro/Downloads/buxoro-maktab-main

echo "📥 GitHub'dan fayllarni tortib olish..."
echo ""

# Pull with allow-unrelated-histories
git pull origin main --allow-unrelated-histories --no-edit

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Pull muvaffaqiyatli!"
    echo ""
    echo "📤 GitHub'ga push qilish..."
    echo ""
    
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=================================================="
        echo "✅ MUVAFFAQIYAT! PUSH QILINDI!"
        echo "=================================================="
        echo ""
        echo "🌐 Repository:"
        echo "   https://github.com/Bahriddin2005/buxoro-maktab"
        echo ""
    else
        echo ""
        echo "❌ Push xatosi!"
    fi
else
    echo ""
    echo "❌ Pull xatosi!"
    echo ""
    echo "QOLDA BAJARING:"
    echo "  git pull origin main --allow-unrelated-histories"
    echo "  git push origin main"
fi

echo "=================================================="

