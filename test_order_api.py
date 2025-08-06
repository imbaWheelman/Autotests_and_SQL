# Сергей Колембет, 33-я когорта, ФИНАЛЬНЫЙ СПРИНТ, Инженер по тестированию расширенный
import requests
import pytest
import random
import string
from datetime import datetime, timedelta
import time

# Конфигурация - убедитесь, что ваш ID сервера правильный
BASE_URL = "https://e4532b0a-d811-4b80-98fb-07a9e60ddac2.serverhub.praktikum-services.ru"

def generate_random_string(length=10):
    """Генерация случайной строки для тестовых данных"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_tomorrow_date():
    """Получение завтрашней даты в формате YYYY-MM-DD"""
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")

def create_order():
    """Создание заказа и возврат его трек-номера"""
    url = f"{BASE_URL}/api/v1/orders"
    
    # Подготовка данных для заказа
    order_data = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": f"Москва, ул. {generate_random_string(5)}, д. {random.randint(1, 100)}",
        "metroStation": "Черкизовская",
        "phone": f"+7{random.randint(1000000000, 9999999999)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": get_tomorrow_date(),
        "comment": f"Тестовый заказ {generate_random_string(5)}",
        "color": ["BLACK"] if random.choice([True, False]) else ["GREY"]
    }
    
    response = requests.post(url, json=order_data)
    assert response.status_code == 201, f"Ошибка при создании заказа: {response.text}"
    
    return response.json()["track"]

def test_order_creation_and_retrieval():
    """
    Шаги автотеста:
    1. Выполнить запрос на создание заказа.
    2. Сохранить номер трека заказа.
    3. Выполнить запрос на получение заказа по треку заказа.
    4. Проверить, что код ответа равен 200.
    """
    # Шаг 1: Выполнить запрос на создание заказа
    track_number = create_order()
    
    # Даем время системе сохранить заказ
    time.sleep(1)
    
    # Шаг 3: Выполнить запрос на получение заказа по треку заказа
    url = f"{BASE_URL}/api/v1/orders?track={track_number}"
    response = requests.get(url)
    
    # Шаг 4: Проверить, что код ответа равен 200
    assert response.status_code == 200, f"Ошибка при получении заказа: {response.text}"