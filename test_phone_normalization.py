#!/usr/bin/env python3
"""
Тестовый скрипт для проверки нормализации номеров телефонов
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main.services import normalize_phone_number

def test_phone_normalization():
    """Тестирует функцию нормализации номеров телефонов"""
    
    test_cases = [
        # Правильный формат
        ("+77712641298", "+77712641298"),
        # С 8 вместо +7
        ("87712641298", "+77712641298"),
        # Без кода страны
        ("77712641298", "+77712641298"),
        # С пробелами и скобками
        ("+7 771 264 12 98", "+77712641298"),
        ("8 (771) 264-12-98", "+77712641298"),
        # С дефисами
        ("+7-771-264-12-98", "+77712641298"),
        # С пробелами
        ("+7 771 264 12 98", "+77712641298"),
        # Короткий номер (не должен измениться)
        ("7712641298", "7712641298"),
        # Неправильный формат (не должен измениться)
        ("123456789", "123456789"),
    ]
    
    print("🧪 Тестирование нормализации номеров телефонов")
    print("=" * 50)
    
    all_passed = True
    
    for input_phone, expected_output in test_cases:
        result = normalize_phone_number(input_phone)
        status = "✅" if result == expected_output else "❌"
        
        print(f"{status} Вход: {input_phone:20} -> Выход: {result:15} (ожидалось: {expected_output})")
        
        if result != expected_output:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 Все тесты прошли успешно!")
    else:
        print("💥 Некоторые тесты не прошли!")
    
    return all_passed

if __name__ == "__main__":
    test_phone_normalization()
