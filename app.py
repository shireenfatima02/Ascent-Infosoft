from flask import Flask, render_template, url_for, redirect, request, jsonify
import smtplib, ssl
import json
from pathlib import Path

app = Flask(__name__)


# LOCATION_DATA = None
LOCATION_DATA_PATH = Path(__file__).parent / 'data' / 'countries+states+cities.json'

def get_location_data():
    try:
        with open(LOCATION_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        app.logger.error(f"Failed to load location data: {str(e)}")
        return []


@app.route('/api/countries')
def get_countries():
    countries = get_location_data()
    return jsonify([{'id': country['id'], 'name': country['name']} for country in countries])


@app.route('/api/states/<int:country_id>')
def get_states(country_id):
    countries = get_location_data()
    country = next((c for c in countries if c['id'] == country_id), None)
    if not country:
        return jsonify([])
    return jsonify([{'id': state['id'], 'name': state['name']} for state in country.get('states', [])])


@app.route('/api/cities/<int:state_id>')
def get_cities(state_id):
    countries = get_location_data()
    for country in countries:
        for state in country.get('states', []):
            if state['id'] == state_id:
                return jsonify([{'id': city['id'], 'name': city['name']} for city in state.get('cities', [])])
    return jsonify([])


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    username = "shireeenfatima@gmail.com"
    password = "qwzg tkqf spla vizg "
    receiver = "shireeenfatima@gmail.com"
    context = ssl.create_default_context()

    subject = "Inquiry for Ascent Infosoft"
    mail = f"Subject: {subject}\n\n{message}"

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, mail)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_name = request.form.get('full-name', '').strip()
        email = request.form.get('email', '').strip()
        mobile_number = request.form.get('mobile-number', '').strip()
        message_text = request.form.get('message', '').strip()
        
        errors = {}
        if not full_name:
            errors['full-name'] = 'Name is required'
        if not email or '@' not in email:
            errors['email'] = 'Valid email is required'
        if not mobile_number or not mobile_number.isdigit() or len(mobile_number) < 10:
            errors['mobile-number'] = 'Valid mobile number is required'
        
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
            send_email(email_message)
            return jsonify(success=True)
        except Exception as e:
            print(f"Email sending failed: {e}")
            return jsonify(success=False, message='Error submitting form')
    
    return render_template('index.html')


@app.route('/about-us/')
def about():
    return render_template('about-us.html')


@app.route('/services/')
def services():
    return render_template('services/services.html')


@app.route('/services/software-development/')
def software_development():
    return render_template('services/software-development.html')


@app.route('/services/web-development/')
def web_development():
    return render_template('services/web-development.html')


@app.route('/services/web-designing/')
def web_designing():
    return render_template('services/web-design.html')


@app.route('/services/mobile-application-development/')
def mobile_application_development():
    return render_template('services/android-development.html')


@app.route('/services/digital-marketing-seo/')
def digital_marketing():
    return render_template('services/digital-marketing-seo.html')


@app.route('/services/ecommerce-development/')
def ecommerce_development():
    return render_template('services/ecommerce-development.html')


@app.route('/products/')
def products():
    return render_template('products/products.html')


@app.route('/products/hospital-management-software/')
def hms():
    return render_template('products/hms.html')


@app.route('/products/college-management-software/')
def cms():
    return render_template('products/cms.html')


@app.route('/products/customer-relationship--management-software/')
def crm():
    return render_template('products/crm.html')


@app.route('/products/leave-management-software/')
def lms():
    return render_template('products/lms.html')


@app.route('/products/store-management-software/')
def sm():
    return render_template('products/sm.html')


@app.route('/portfolio/')
def portfolio():
    return render_template('portfolio.html')


@app.route('/contact-us/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        full_name = request.form.get('full-name', '').strip()
        email = request.form.get('email', '').strip()
        mobile_number = request.form.get('mobile-number', '').strip()
        country = request.form.get('country', '').strip()
        state = request.form.get('state', '').strip()
        city = request.form.get('city', '').strip()
        message_text = request.form.get('message', '').strip()
        
        errors = {}
        if not full_name:
            errors['full-name'] = 'Name is required'
        if not email or '@' not in email:
            errors['email'] = 'Valid email is required'
        if not mobile_number or not mobile_number.isdigit() or len(mobile_number) < 10:
            errors['mobile-number'] = 'Valid mobile number is required'
        if not country:
            errors['country'] = 'Country is required'
        if not state:
            errors['state'] = 'State is required'
        if not city:
            errors['city'] = 'City is required'
        
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
            send_email(email_message)
            return jsonify(success=True)
        except Exception as e:
            print(f"Email sending failed: {e}")
            return jsonify(success=False, message='Error submitting form')
    
    return render_template('contact-us.html')


if __name__ == '__main__':
    app.run(debug=True, port=5002)