import json
import os
import time

import pika
import requests


QUEUE_NAME = "badge_print_requests"
WEBHOOK_URL = os.getenv(
    "WEBHOOK_URL",
    "http://localhost:5000/webhook/print-complete"
)


def get_rabbitmq_connection():
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


def handle_print_request(ch, method, properties, body):
    """
    Process one badge-print request from RabbitMQ.
    """

    request = json.loads(body)

    job_id = request["job_id"]
    attendee_id = request["attendee_id"]
    qr_code = request["qr_code"]
    full_name = request["full_name"]

    print()
    print("===================================")
    print("BADGE PRINT REQUEST RECEIVED")
    print("===================================")
    print(f"Job ID:       {job_id}")
    print(f"Attendee ID:  {attendee_id}")
    print(f"QR Code:      {qr_code}")
    print(f"Name:         {full_name}")
    print("===================================")

    # Simulate the time required to print the badge.
    print("Printing badge...")
    time.sleep(3)

    webhook_payload = {
        "job_id": job_id,
        "attendee_id": attendee_id,
        "status": "COMPLETED"
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=webhook_payload,
            timeout=10
        )

        print(f"Webhook response: {response.status_code}")

        if response.ok:
            print(f"Badge successfully printed for {full_name}")
            print()

            # Tell RabbitMQ the message was successfully processed.
            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            print("Webhook failed. Message will be returned to the queue.")
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True
            )

    except requests.RequestException as error:
        print(f"Webhook request failed: {error}")
        print("Message will be returned to the queue.")

        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )


def start_printer():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=handle_print_request,
        auto_ack=False
    )

    print("===================================")
    print("SOLSTICE BADGE PRINTER")
    print("===================================")
    print(f"Listening on: {QUEUE_NAME}")
    print(f"Webhook:      {WEBHOOK_URL}")
    print("Waiting for print requests...")
    print()

    try:
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nStopping badge printer...")
        channel.stop_consuming()

    finally:
        connection.close()


if __name__ == "__main__":
    start_printer()