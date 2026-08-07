from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from datetime import datetime
from flask_mail import Message
from config import mail
from app.services.pricing import (
    CHALET_PRICES,
    CONFERENCE_PRICE,
    SPA_PRICES
)

booking_bp = Blueprint("booking", __name__)
from datetime import datetime

@booking_bp.route("/booking-request", methods=["GET", "POST"])
def booking_request():

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        communication = request.form["preferred_communication"]

        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

        # Validate dates
        if check_out_date <= check_in_date:
            flash(
                "Check-out date must be after the check-in date.",
                "danger"
            )
            return redirect(url_for("booking.booking_request"))

        guests = request.form["guests"]
        special_requests = request.form.get("special_requests", "")

        services = request.form.getlist("services")

        services_text = ", ".join(services) if services else "None"

        resort_email = Message(
        subject="New Booking Request",
        recipients=["bonololekalakala16@gmail.com"]  # Replace with the real email
        )

        resort_email.body = f"""
        A new booking request has been 
        submitted.

        Customer:
        {first_name} {last_name}

        Email:
        {email}

        Phone:
        {phone}

        Preferred Communication:
        {communication}

        Check-in:
        {check_in}

        Check-out:
        {check_out}

        Guests:
        {guests}

        Services:
        {services_text}

        Special Requests:
        {special_requests}
        """

        mail.send(resort_email)

        customer_email = Message(
        subject="Booking Request Received",
        recipients=[email]
        )

        customer_email.body = f"""
    Dear {first_name},

    Thank you for choosing Oluhle Resort.

    We have successfully received your booking request.

    Booking Summary

    Check-in: {check_in}

    Check-out: {check_out}

    Guests: {guests}

    Services:
    {services_text}

    Our reservations team will contact you shortly.

    Kind regards,

    Oluhle Resort🌿
    """

        print("MAIL_SERVER:", current_app.config["MAIL_SERVER"])
        print("MAIL_PORT:", current_app.config["MAIL_PORT"])
        print("MAIL_USE_TLS:", current_app.config["MAIL_USE_TLS"])
        print("MAIL_USERNAME:", current_app.config["MAIL_USERNAME"])
        print("MAIL_DEFAULT_SENDER:", current_app.config["MAIL_DEFAULT_SENDER"])    

        mail.send(customer_email)

        return render_template("booking_success.html")

    return render_template("booking_request.html")