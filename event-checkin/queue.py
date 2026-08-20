import json
import os
import pika


QUEUE_NAME = "badge_print_requests"


def get_rabbitmq_connection():
    """
    Create a connection to the RabbitMQ container.
    """

    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "solstice"),
        os.getenv("RABBITMQ_PASSWORD", "solstice123")
    )

    parameters = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        credentials=credentials
    )

    return pika.BlockingConnection(parameters)


def publish_print_request(job_id, attendee_id, qr_code, full_name):
    """
    Publish a badge-print request to RabbitMQ.

    The API does not wait for the printer to finish.
    It only publishes the request and returns.
    """

    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    message = {
        "job_id": job_id,
        "attendee_id": attendee_id,
        "qr_code": qr_code,
        "full_name": full_name
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json"
        )
    )

    connection.close()

    return message