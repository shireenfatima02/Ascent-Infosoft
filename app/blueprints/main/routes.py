from flask import render_template, request, jsonify

from . import bp
from ...services.email import send_email


@bp.route("/", methods=["GET", "POST"], endpoint="index")
def index():
    if request.method == "POST":
        full_name = request.form.get("full-name", "").strip()
        email = request.form.get("email", "").strip()
        mobile_number = request.form.get("mobile-number", "").strip()
        message_text = request.form.get("message", "").strip()

        errors = {}
        if not full_name:
            errors["full-name"] = "Name is required"
        if not email or "@" not in email:
            errors["email"] = "Valid email is required"
        if not mobile_number or not mobile_number.isdigit() or len(mobile_number) < 10:
            errors["mobile-number"] = "Valid mobile number is required"
        if errors:
            return jsonify(success=False, errors=errors)

        try:
            email_message = (
                f"A New Form Was Submitted:\n"
                f"Name: {full_name}\n"
                f"Email: {email}\n"
                f"Mobile: {mobile_number}\n"
                f"Message: {message_text}"
            )
            send_email(email_message, subject="Inquiry for Ascent Infosoft")
            return jsonify(success=True)
        except Exception as e:  # pragma: no cover
            print(f"Email sending failed: {e}")
            return jsonify(success=False, message="Error submitting form")

    return render_template("index.html")


@bp.route("/about-us/", endpoint="about")
def about():
    return render_template("about-us.html")


@bp.route("/services/", endpoint="services")
def services():
    return render_template("services/services.html")


@bp.route("/services/software-development/", endpoint="software_development")
def software_development():
    return render_template("services/software-development.html")


@bp.route("/services/web-development/", endpoint="web_development")
def web_development():
    return render_template("services/web-development.html")


@bp.route("/services/web-designing/", endpoint="web_designing")
def web_designing():
    return render_template("services/web-design.html")


@bp.route("/services/mobile-application-development/", endpoint="mobile_application_development")
def mobile_application_development():
    return render_template("services/android-development.html")


@bp.route("/services/digital-marketing-seo/", endpoint="digital_marketing")
def digital_marketing():
    return render_template("services/digital-marketing-seo.html")


@bp.route("/services/ecommerce-development/", endpoint="ecommerce_development")
def ecommerce_development():
    return render_template("services/ecommerce-development.html")


@bp.route("/products/", endpoint="products")
def products():
    return render_template("products/products.html")


@bp.route("/products/hospital-management-software/", endpoint="hms")
def hms():
    return render_template("products/hms.html")


@bp.route("/products/college-management-software/", endpoint="cms")
def cms():
    return render_template("products/cms.html")


@bp.route("/products/customer-relationship--management-software/", endpoint="crm")
def crm():
    return render_template("products/crm.html")


@bp.route("/products/leave-management-software/", endpoint="lms")
def lms():
    return render_template("products/lms.html")


@bp.route("/products/store-management-software/", endpoint="sm")
def sm():
    return render_template("products/sm.html")


@bp.route("/portfolio/", endpoint="portfolio")
def portfolio():
    return render_template("portfolio.html")


@bp.route("/contact-us/", methods=["GET", "POST"], endpoint="contact")
def contact():
    if request.method == "POST":
        full_name = request.form.get("full-name", "").strip()
        email = request.form.get("email", "").strip()
        mobile_number = request.form.get("mobile-number", "").strip()
        country = request.form.get("country", "").strip()
        state = request.form.get("state", "").strip()
        city = request.form.get("city", "").strip()
        message_text = request.form.get("message", "").strip()

        errors = {}
        if not full_name:
            errors["full-name"] = "Name is required"
        if not email or "@" not in email:
            errors["email"] = "Valid email is required"
        if not mobile_number or not mobile_number.isdigit() or len(mobile_number) < 10:
            errors["mobile-number"] = "Valid mobile number is required"
        if not country:
            errors["country"] = "Country is required"
        if not state:
            errors["state"] = "State is required"
        if not city:
            errors["city"] = "City is required"

        if errors:
            return jsonify(success=False, errors=errors)

        try:
            email_message = (
                f"A New Contact Form Was Submitted:\n"
                f"Name: {full_name}\n"
                f"Email: {email}\n"
                f"Mobile: {mobile_number}\n"
                f"Country: {country}\n"
                f"State: {state}\n"
                f"City: {city}\n"
                f"Message: {message_text}"
            )
            send_email(email_message, subject="Contact Form: Ascent Infosoft")
            return jsonify(success=True)
        except Exception as e:  # pragma: no cover
            print(f"Email sending failed: {e}")
            return jsonify(success=False, message="Error submitting form")

    return render_template("contact-us.html")

