import uuid

from flask import Flask, jsonify, request

from db import (
    create_print_job,
    get_attendee_by_qr,
    complete_print_job
)

from queue import publish_print_request


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "solstice-event-checkin"
    })


@app.route("/check-in", methods=["POST"])
def check_in():
    data = request.get_json(silent=True) or {}

    qr_code = data.get("qr_code")

    if not qr_code:
        return jsonify({
            "status": "ERROR",
            "message": "qr_code is required"
        }), 400

    attendee = get_attendee_by_qr(qr_code)

    if attendee is None:
        return jsonify({
            "status": "ERROR",
            "message": "Attendee not found"
        }), 404

    # Duplicate-scan protection.
    if attendee["status"] == "CHECKED_IN":
        return jsonify({
            "status": "CHECKED_IN",
            "message": "Attendee is already checked in",
            "attendee": attendee["full_name"],
            "print_requested": False
        }), 200

    # The attendee may already have a pending print job.
    if attendee["status"] == "PENDING":
        # Try to create the job. The database UNIQUE constraint
        # prevents a second job for the same attendee.
        job_id = str(uuid.uuid4())

        created = create_print_job(
            job_id,
            attendee["attendee_id"]
        )

        if not created:
            return jsonify({
                "status": "PENDING",
                "message": "Badge printing is already pending",
                "attendee": attendee["full_name"],
                "print_requested": False
            }), 200

        try:
            publish_print_request(
                job_id,
                attendee["attendee_id"],
                attendee["qr_code"],
                attendee["full_name"]
            )

        except Exception as error:
            return jsonify({
                "status": "ERROR",
                "message": f"Could not publish print request: {error}"
            }), 500

        return jsonify({
            "status": "PENDING",
            "message": "Badge printing in progress",
            "attendee": attendee["full_name"],
            "job_id": job_id,
            "print_requested": True
        }), 202

    return jsonify({
        "status": "ERROR",
        "message": "Unknown attendee status"
    }), 500


@app.route("/webhook/print-complete", methods=["POST"])
def print_complete():
    data = request.get_json(silent=True) or {}

    job_id = data.get("job_id")
    attendee_id = data.get("attendee_id")
    status = data.get("status")

    if not job_id or not attendee_id or not status:
        return jsonify({
            "status": "ERROR",
            "message": "job_id, attendee_id and status are required"
        }), 400

    if status != "COMPLETED":
        return jsonify({
            "status": "ERROR",
            "message": "Unsupported print status"
        }), 400

    result = complete_print_job(job_id)

    if not result["success"]:
        return jsonify({
            "status": "ERROR",
            "message": result["message"]
        }), 404

    return jsonify({
        "status": "CHECKED_IN",
        "message": result["message"],
        "job_id": job_id,
        "attendee_id": attendee_id
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )