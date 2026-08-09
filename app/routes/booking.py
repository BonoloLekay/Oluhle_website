from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from datetime import datetime, date
from flask_mail import Message
from config import mail
from app.services.pricing import (
    CHALET_PRICES,
    CONFERENCE_PRICE,
    SPA_PRICES
)
import os


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

        try:
            mail.send(resort_email)
            print("Resort email sent successfully.")
        except Exception as e:
            print("Error sending resort email:", e)

        logo_url = url_for(
        "static",
        filename="images/logo.png",
        _external=True
        )
        #Customee email
        customer_email = Message(
        subject="Oluhle Resort - Booking Request Received",
        recipients=[email]
        )

        customer_email.html = render_template(
        "emails/booking_confirmation.html",
        first_name=first_name,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        services_text=services_text,
        logo_url=logo_url
        )

        print("MAIL_SERVER:", current_app.config["MAIL_SERVER"])
        print("MAIL_PORT:", current_app.config["MAIL_PORT"])
        print("MAIL_USE_TLS:", current_app.config["MAIL_USE_TLS"])
        print("MAIL_USERNAME:", current_app.config["MAIL_USERNAME"])
        print("MAIL_DEFAULT_SENDER:", current_app.config["MAIL_DEFAULT_SENDER"])    

        try:
            mail.send(customer_email)
            print("Customer email sent successfully.")
        except Exception as e:
            print("Error sending customer email:", e)

        return render_template("booking_success.html")

    return render_template("booking_request.html",
    today=date.today().isoformat()
    )