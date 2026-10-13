import re
import os
import requests
from bs4 import BeautifulSoup

# --- НАСТРОЙКИ ---
CHANNEL_NAME = "free_sc4russ"  # Имя вашего канала без @
OUTPUT_FILE = "configs.txt"     # Имя файла, в который будем сохранять конфиги
# -----------------

def get_configs_from_telegram():
    """Загружает веб-версию канала и извлекает VLESS ссылки."""
    url = f"https://t.me/s/{CHANNEL_NAME}"
    print(f"Загрузка страницы: {url}")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем все блоки с сообщениями
    messages = soup.find_all('div', class_='tgme_widget_message_text')
    
    configs = []
    # Регулярное выражение для поиска ссылок vless://
    vless_pattern = re.compile(r'(vless://[^\s<>"]+)')
    
    for msg in messages:
        text = msg.get_text(separator=' ')
        found = vless_pattern.findall(text)
        configs.extend(found)
    
    print(f"Найдено сырых ссылок: {len(configs)}")
    return configs

def clean_and_deduplicate(configs):
    """Очищает ссылки от мусора и удаляет дубликаты."""
    cleaned = []
    seen = set()
    
    for link in configs:
        # Убираем возможные лишние символы на конце
        link = link.strip().rstrip('.,;:!?')
        
        if link not in seen:
            seen.add(link)
            cleaned.append(link)
    
    print(f"Уникальных ссылок после очистки: {len(cleaned)}")
    return cleaned

def save_to_file(configs, filename):
    """Сохраняет список ссылок в файл."""
    with open(filename, 'w', encoding='utf-8') as f:
        for config in configs:
            f.write(config + '\n')
    print(f"Сохранено в {filename}")

if __name__ == "__main__":
    raw_configs = get_configs_from_telegram()
    
    if raw_configs:
        final_configs = clean_and_deduplicate(raw_configs)
        save_to_file(final_configs, OUTPUT_FILE)
    else:
        print("Конфиги не найдены. Файл не обновлен.")
