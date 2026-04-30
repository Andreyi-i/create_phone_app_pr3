#!/usr/bin/env python3
"""
APK Reassembly Script v1.0.2
Об'єднує розділені частини APK файлу версії 1.0.2
Просто запустіть цей скрипт в папці з частинами
"""

import os
import sys
from pathlib import Path

def format_size(bytes_size):
    """Форматує розмір файлу в читаний вигляд"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def main():
    print("🔄 Розпочинаємо об'єднання APK файлу v1.0.2...")
    print()
    
    # Імена файлів для v1.0.2
    part_aa = "ai-learning-app-v1_0_2.apk.partaa"
    part_ab = "ai-learning-app-v1_0_2.apk.partab"
    output = "ai-learning-app-v1_0_2.apk"
    
    # Перевіримо наявність частин
    if not Path(part_aa).exists() or not Path(part_ab).exists():
        print("❌ Помилка: Не знайдені файли частин")
        print("Переконайтесь, що обидва файли знаходяться в поточній директорії:")
        print(f"  - {part_aa}")
        print(f"  - {part_ab}")
        print()
        print("Натисніть Enter для завершення...")
        input()
        sys.exit(1)
    
    # Перевіримо розміри
    size_aa = Path(part_aa).stat().st_size
    size_ab = Path(part_ab).stat().st_size
    
    print(f"📦 Розмір частини 1: {format_size(size_aa)}")
    print(f"📦 Розмір частини 2: {format_size(size_ab)}")
    print()
    print("⏳ Об'єднання файлів...")
    
    try:
        # Об'єднуємо файли
        with open(output, 'wb') as outfile:
            with open(part_aa, 'rb') as infile:
                outfile.write(infile.read())
            with open(part_ab, 'rb') as infile:
                outfile.write(infile.read())
        
        # Перевіримо цілісність
        if Path(output).exists():
            final_size = Path(output).stat().st_size
            print("✅ APK файл успішно об'єднано!")
            print(f"📊 Фінальний розмір: {format_size(final_size)}")
            
            # Перевіримо, що це валідний ZIP/APK
            with open(output, 'rb') as f:
                header = f.read(4)
                if header == b'PK\x03\x04':  # ZIP file signature
                    print("✔️ Файл є валідним ZIP архівом (APK)")
                else:
                    print("⚠️ Попередження: Файл може бути пошкоджений")
            
            print()
            print("🎉 Готово! Ви можете встановити APK на Android пристрій:")
            print(f"   adb install {output}")
            print()
        else:
            print("❌ Помилка при об'єднанні файлів")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Помилка: {e}")
        sys.exit(1)
    
    print("Натисніть Enter для завершення...")
    input()

if __name__ == "__main__":
    main()
