from flask import redirect, url_for

from . import bp


@bp.route("/legacy/index", endpoint="index")
def legacy_index():
    return redirect(url_for("main.index"))


@bp.route("/legacy/about", endpoint="about")
def legacy_about():
    return redirect(url_for("main.about"))


@bp.route("/legacy/services", endpoint="services")
def legacy_services():
    return redirect(url_for("main.services"))


@bp.route("/legacy/services/software-development", endpoint="software_development")
def legacy_software_development():
    return redirect(url_for("main.software_development"))


@bp.route("/legacy/services/web-development", endpoint="web_development")
def legacy_web_development():
    return redirect(url_for("main.web_development"))


@bp.route("/legacy/services/web-designing", endpoint="web_designing")
def legacy_web_designing():
    return redirect(url_for("main.web_designing"))


@bp.route("/legacy/services/mobile-application-development", endpoint="mobile_application_development")
def legacy_mobile_application_development():
    return redirect(url_for("main.mobile_application_development"))


@bp.route("/legacy/services/digital-marketing-seo", endpoint="digital_marketing")
def legacy_digital_marketing():
    return redirect(url_for("main.digital_marketing"))


@bp.route("/legacy/services/ecommerce-development", endpoint="ecommerce_development")
def legacy_ecommerce_development():
    return redirect(url_for("main.ecommerce_development"))


@bp.route("/legacy/products", endpoint="products")
def legacy_products():
    return redirect(url_for("main.products"))


@bp.route("/legacy/products/hms", endpoint="hms")
def legacy_hms():
    return redirect(url_for("main.hms"))


@bp.route("/legacy/products/cms", endpoint="cms")
def legacy_cms():
    return redirect(url_for("main.cms"))


@bp.route("/legacy/products/crm", endpoint="crm")
def legacy_crm():
    return redirect(url_for("main.crm"))


@bp.route("/legacy/products/lms", endpoint="lms")
def legacy_lms():
    return redirect(url_for("main.lms"))


@bp.route("/legacy/products/sm", endpoint="sm")
def legacy_sm():
    return redirect(url_for("main.sm"))


@bp.route("/legacy/contact", endpoint="contact")
def legacy_contact():
    return redirect(url_for("main.contact"))


@bp.route("/legacy/portfolio", endpoint="portfolio")
def legacy_portfolio():
    return redirect(url_for("main.portfolio"))


@bp.route("/legacy/login", endpoint="client_login")
def legacy_login():
    return redirect(url_for("auth.client_login"))
