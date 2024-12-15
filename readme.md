# Метрики системы и приложений (Яндекс.Браузер, Telegram)

Данная программа предоставляет метрики о загрузке CPU, использовании памяти и дисков для вашей системы, а также мониторит ресурсы, потребляемые **Яндекс.Браузером** и **Telegram**

## Запуск

1. Установите зависимости:
   Для установки всех зависимостей используйте команду:
   ```bash
   pip install -r requirements.txt
2. Или установите библиотеки вручную с помощью pip:

   ```bash
   pip install psutil prometheus_client python-dotenv
   
3. Установите переменные окружения в файле .env: Создайте файл .env в корневой папке проекта и укажите переменные для хоста и порта экспортеров:

   ```ini
   EXPORTER_HOST=0.0.0.0
   EXPORTER_PORT=8000
4. Запустите код:

   ```bash
   python main.py
   ```
   Экспортер будет доступен по адресу: http://<EXPORTER_HOST>:<EXPORTER_PORT>/metrics.

5. Метрики

1) Общие метрики системы:
   a)cpu_usage_percent: Процент использования CPU.
   Пример запроса PromQL:
   cpu_usage_percent

   b)memory_total_bytes: Общий объем оперативной памяти в байтах.
   Пример запроса PromQL:
   memory_total_bytes
   
   c)memory_used_bytes: Объем используемой оперативной памяти в байтах.
   Пример запроса PromQL:
   memory_used_bytes

   d)disk_total_bytes: Общий объем доступных дисков в байтах. 
   Пример запроса PromQL:
   disk_total_bytes
   
   e)disk_used_bytes: Объем используемого пространства на дисках в байтах.
   Пример запроса PromQL:
   disk_used_bytes
2) Метрики для Яндекс.Браузера:
   a)yandex_browser_cpu_percent: Процент использования CPU Яндекс.Браузером.
   
   Пример запроса PromQL:
   yandex_browser_cpu_percent

   b)yandex_browser_memory_used_bytes: Объем памяти, используемый Яндекс.Браузером в байтах.
   
   Пример запроса PromQL:
   yandex_browser_memory_used_bytes
3) Метрики для Telegram:
   a)telegram_cpu_percent: Процент использования CPU Telegram.
   Пример запроса PromQL:
   telegram_cpu_percent
   b) telegram_memory_used_bytes: Объем памяти, используемый Telegram в байтах.
   Пример запроса PromQL:
   telegram_memory_used_bytes
6. Настройка Prometheus
   Добавление экспортеров в prometheus.yml
   Вам нужно настроить Prometheus на сбор метрик с вашего экспортеров. Для этого обновите файл конфигурации Prometheus (prometheus.yml) и добавьте новый источник метрик.
   
   Откройте файл prometheus.yml и добавьте следующее в раздел scrape_configs:
   
   yaml
   Копировать код
   scrape_configs:
     - job_name: 'prometheus'
       static_configs:
         - targets: ['localhost:9090']
   
       - job_name: 'system_metrics'
         static_configs:
           - targets: ['localhost:8000']
   Это обеспечит сбор данных с порта 8000, на котором работает ваш экспортер.