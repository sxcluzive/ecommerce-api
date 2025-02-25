from celery import Celery

celery = Celery(
    "ecommerce",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    broker_connection_retry_on_startup=True,
)

celery.conf.update(
    task_routes={"app.tasks.process_order": {"queue": "orders"}}
)
