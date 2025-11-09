"""
Утилиты для работы с сессиями и определения уникальных пользователей
"""
import hashlib


def get_client_ip(request):
    """
    Получение IP адреса клиента с учетом прокси
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Получение User Agent браузера
    """
    return request.META.get('HTTP_USER_AGENT', '')


def generate_session_id(ip_address, user_agent, browser_fingerprint=''):
    """
    Генерация уникального идентификатора сессии
    на основе IP, User Agent и browser fingerprint
    """
    # Комбинируем все данные
    data = f"{ip_address}|{user_agent}|{browser_fingerprint}"
    
    # Создаем hash
    session_hash = hashlib.sha256(data.encode()).hexdigest()
    
    return session_hash
