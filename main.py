import os
import psutil
from prometheus_client import start_http_server, Gauge
from time import sleep

# Основные метрики
cpu_usage = Gauge('cpu_usage_percent', 'Процент использования CPU')
memory_total = Gauge('memory_total_bytes', 'Общий объем оперативной памяти')
memory_used = Gauge('memory_used_bytes', 'Используемая оперативная память')
disk_total = Gauge('disk_total_bytes', 'Общий объем дисков')
disk_used = Gauge('disk_used_bytes', 'Используемый объем дисков')

# Метрики для яндекса
browser_cpu_usage = Gauge('yandex_browser_cpu_percent', 'Процент использования CPU Яндексом')
browser_memory_used = Gauge('yandex_browser_memory_used_bytes', 'Используемая память Яндекс.Браузером')

# Метрики для Telegram
telegram_cpu_usage = Gauge('telegram_cpu_percent', 'Процент использования CPU Telegram')
telegram_memory_used = Gauge('telegram_memory_used_bytes', 'Используемая память Telegram')


def collect_metrics():
    # Получение общих метрик системы
    cpu_usage.set(psutil.cpu_percent())
    memory_total.set(psutil.virtual_memory().total)
    memory_used.set(psutil.virtual_memory().used)
    disk_total.set(psutil.disk_usage('C:/').total)
    disk_used.set(psutil.disk_usage('C:/').used)

    # Определение метрик для яндекса
    total_browser_cpu = 0
    total_browser_memory = 0

    # Получение метрик для яндекса
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        # Пробуем получить запущенные процессы
        try:
            if 'yandex' in proc.info['name'].lower() or 'browser' in proc.info['name'].lower():
                total_browser_cpu += proc.info['cpu_percent']
                total_browser_memory += proc.info['memory_info'].rss
        # Игнорируем не рабочие процессы
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Установка метрик для яндекста
    browser_cpu_usage.set(total_browser_cpu)
    browser_memory_used.set(total_browser_memory)

    # Определение метрик для Telegram
    total_telegram_cpu = 0
    total_telegram_memory = 0

    # Получение метрик для Telegram
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        # Пробуем получить запущенные процессы
        try:
            if 'telegram' in proc.info['name'].lower():
                total_telegram_cpu += proc.info['cpu_percent']
                total_telegram_memory += proc.info['memory_info'].rss

        # Игнорируем не рабочие процессы
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Установка метрик для telegram
    telegram_cpu_usage.set(total_telegram_cpu)
    telegram_memory_used.set(total_telegram_memory)


def main():
    # Получаем переменные окружения для хоста и порта
    exporter_host = os.getenv("EXPORTER_HOST")
    exporter_port = int(os.getenv("EXPORTER_PORT"))

    # Запуск HTTP сервера для Prometheus
    start_http_server(exporter_port, addr=exporter_host)
    print(f"Получение метрик запущено по адресу {exporter_host}:{exporter_port}")

    # Сбор метрик и обновление каждые 10 секунд
    while True:
        collect_metrics()
        sleep(10)


if __name__ == '__main__':
    main()
