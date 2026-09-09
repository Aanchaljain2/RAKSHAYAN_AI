from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
EMERGENCY_PHONE_NUMBER = os.getenv("EMERGENCY_PHONE_NUMBER")

twilio_client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)

import joblib
import speech
import json
from datetime import datetime

app = Flask(__name__)

# LOAD ML MODEL
model = joblib.load("model/emergency_model.pkl")

# LOAD CONTACTS
with open("contacts.json", "r") as file:
    contacts = json.load(file)

rider = contacts["rider"]
emergency_contact = contacts["emergency_contact"]
# SEND SOS SMS
def send_sos_sms(sos_data):

    message_body = (
        "🚨 RAKSHAYAN AI SOS 🚨\n\n"
        f"Emergency: {sos_data['emergency_type']}\n"
        f"Rider: {sos_data['rider_name']}\n"
        f"Phone: {sos_data['rider_phone']}\n"
        f"Location: {sos_data['location']}\n"
        f"Time: {sos_data['time']}"
    )

    message = twilio_client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=EMERGENCY_PHONE_NUMBER
    )

    print()
    print("📱 SOS SMS SENT")
    print("Message SID:", message.sid)

    return message.sid

# Store the latest detected emergency
current_emergency = {
    "intent": None,
    "text": None,
    "confidence": None
}


# Store latest GPS location
current_location = {
    "latitude": None,
    "longitude": None
}


@app.route("/")
def home():
    return render_template("index.html")


# AI RESPONSE
def create_response(intent):
    intent = intent.lower()

    if intent == "accident":
        return "I detected an accident. Do you want me to send an SOS?"

    elif intent == "medical":
        return "I detected a medical emergency. Do you want me to send an SOS?"

    elif intent == "police":
        return "I detected a police emergency. Do you want me to send an SOS?"

    elif intent == "fatigue":
        return "I detected rider fatigue. Do you want me to send an SOS?"

    elif intent == "helmet_issue":
        return "I detected a helmet issue. Do you want me to send an SOS?"

    elif intent == "bike_issue":
        return "I detected a bike issue. Do you want me to send an SOS?"

    else:
        return "I understand. I am still monitoring your safety."


# UPDATE GPS LOCATION
@app.route("/update_location", methods=["POST"])
def update_location():

    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({
            "success": False,
            "message": "GPS coordinates not received."
        })

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid GPS coordinates."
        })

    current_location["latitude"] = latitude
    current_location["longitude"] = longitude

    print()
    print("📍 GPS LOCATION UPDATED")
    print("Latitude:", latitude)
    print("Longitude:", longitude)

    map_link = (
        f"https://www.google.com/maps?q={latitude},{longitude}"
    )

    print("🗺️ Google Maps:", map_link)

    return jsonify({
        "success": True,
        "latitude": latitude,
        "longitude": longitude,
        "map_link": map_link
    })


# CREATE SOS DATA
def create_sos_data():

    emergency_type = current_emergency["intent"]

    current_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    latitude = current_location["latitude"]
    longitude = current_location["longitude"]

    if latitude is not None and longitude is not None:

        location = (
            f"https://www.google.com/maps?q="
            f"{latitude},{longitude}"
        )

    else:

        location = "Location not available"

    sos_data = {
        "emergency_type": emergency_type,
        "rider_name": rider["name"],
        "rider_phone": rider["phone"],
        "emergency_contact_name": emergency_contact["name"],
        "emergency_contact_phone": emergency_contact["phone"],
        "latitude": latitude,
        "longitude": longitude,
        "location": location,
        "time": current_time
    }

    return sos_data


# TEXT DETECTION
@app.route("/detect", methods=["POST"])
def detect():

    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "success": False,
            "message": "No input received."
        })

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    response = create_response(prediction)

    current_emergency["intent"] = prediction
    current_emergency["text"] = text
    current_emergency["confidence"] = round(confidence, 2)

    print()
    print("👤 Rider said:", text)
    print("🧠 AI detected:", prediction)
    print(f"📊 Confidence: {confidence:.2f}%")
    print("🤖 Rakshayan AI:", response)

    return jsonify({
        "success": True,
        "text": text,
        "intent": prediction,
        "confidence": round(confidence, 2),
        "response": response
    })


# VOICE INPUT
@app.route("/voice", methods=["GET"])
def voice():

    print()
    print("=" * 55)
    print("🎤 RAKSHAYAN AI - VOICE INPUT")
    print("=" * 55)
    print("🎤 Microphone is ready.")
    print("🎤 Listening for rider...")

    text = speech.listen()

    if not text:

        print("❌ Could not understand.")

        return jsonify({
            "success": False,
            "message": "I could not understand you. Please try again."
        })

    print()
    print(f"👤 Rider said: {text}")

    prediction = model.predict([text])[0]

    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    response = create_response(prediction)

    current_emergency["intent"] = prediction
    current_emergency["text"] = text
    current_emergency["confidence"] = round(confidence, 2)

    print(f"🧠 AI detected: {prediction}")
    print(f"📊 Confidence: {confidence:.2f}%")
    print(f"🤖 Rakshayan AI: {response}")

    return jsonify({
        "success": True,
        "text": text,
        "intent": prediction,
        "confidence": round(confidence, 2),
        "response": response
    })


# VOICE SOS CONFIRMATION
@app.route("/confirm_voice", methods=["GET"])
def confirm_voice():

    print()
    print("=" * 55)
    print("🆘 RAKSHAYAN AI - VOICE SOS CONFIRMATION")
    print("=" * 55)
    print("🎤 Listening for YES or NO...")

    text = speech.listen()

    if not text:

        print("❌ No confirmation heard.")

        return jsonify({
            "success": False,
            "decision": "unknown",
            "message": "I could not hear your answer."
        })

    text_lower = text.lower().strip()

    print()
    print("👤 Rider confirmation:", text)

    yes_phrases = [
        "yes",
        "yeah",
        "yep",
        "yup",
        "sure",
        "okay",
        "ok",
        "send it",
        "send sos",
        "send the sos",
        "send sms",
        "send an sms",
        "send the message",
        "go ahead",
        "do it",
        "please send",
        "yes send",
        "yes send it",
        "yes please",
        "yes send an sms"
    ]

    no_phrases = [
        "no",
        "nope",
        "nah",
        "cancel",
        "cancel it",
        "stop",
        "don't send",
        "do not send",
        "don't send it",
        "do not send it",
        "don't send sos",
        "do not send sos",
        "no don't send",
        "no do not send",
        "no cancel"
    ]

    is_no = any(
        phrase in text_lower
        for phrase in no_phrases
    )

    is_yes = any(
        phrase in text_lower
        for phrase in yes_phrases
    )

    if is_yes and not is_no:

        print()
        print("🆘 VOICE SOS CONFIRMED")

        sos_data = create_sos_data()

        print_sos_information(sos_data)

        response = (
            f"SOS confirmed. Emergency information prepared "
            f"for {emergency_contact['name']}."
        )

        return jsonify({
            "success": True,
            "text": text,
            "decision": "yes",
            "confidence": 100,
            "response": response,
            "sos": sos_data
        })

    if is_no:

        print()
        print("❌ VOICE SOS CANCELLED")

        response = (
            "SOS cancelled. I am still monitoring your safety."
        )

        return jsonify({
            "success": True,
            "text": text,
            "decision": "no",
            "confidence": 100,
            "response": response
        })

    print("❓ Could not determine YES or NO.")

    response = (
        "I could not determine your answer. "
        "Please say yes or no."
    )

    return jsonify({
        "success": False,
        "text": text,
        "decision": "unknown",
        "confidence": 0,
        "message": response
    })


# BUTTON SOS CONFIRMATION
@app.route("/confirm_sos", methods=["POST"])
def confirm_sos():

    print()
    print("=" * 55)
    print("🆘 RAKSHAYAN AI - BUTTON SOS CONFIRMATION")
    print("=" * 55)

    if current_emergency["intent"] is None:

        return jsonify({
            "success": False,
            "message": "No emergency has been detected yet."
        })

    print("🆘 SOS CONFIRMED USING DASHBOARD BUTTON")

    sos_data = create_sos_data()

    print_sos_information(sos_data)
    sms_sid = send_sos_sms(sos_data)
    response = (
        f"SOS confirmed. Emergency information prepared "
        f"for {emergency_contact['name']}."
    )

    return jsonify({
        "success": True,
        "decision": "yes",
        "confidence": 100,
        "response": response,
        "sos": sos_data
    })


# PRINT SOS INFORMATION
def print_sos_information(sos_data):

    print()
    print("=" * 55)
    print("🆘 SOS INFORMATION")
    print("=" * 55)
    print("🚨 Emergency Type:",
          sos_data["emergency_type"])
    print("👤 Rider:",
          sos_data["rider_name"])
    print("📞 Rider Phone:",
          sos_data["rider_phone"])
    print("👤 Emergency Contact:",
          sos_data["emergency_contact_name"])
    print("📱 Emergency Contact Phone:",
          sos_data["emergency_contact_phone"])
    print("📍 Latitude:",
          sos_data["latitude"])
    print("📍 Longitude:",
          sos_data["longitude"])
    print("🗺️ Location:",
          sos_data["location"])
    print("🕐 Time:",
          sos_data["time"])
    print("=" * 55)


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("🏍️ RAKSHAYAN AI")
    print("Emergency Assistance System")
    print("=" * 60)
    print()

    print("🌐 Dashboard:")
    print("http://127.0.0.1:5000")
    print()

    print("🧠 AI Model: LOADED")
    print("🎤 Voice Input: READY")
    print("🆘 SOS Voice Confirmation: READY")
    print("🆘 SOS Button Confirmation: READY")
    print("📍 GPS Backend: READY")
    print("📱 Emergency Contacts: LOADED")
    print()

    app.run(debug=True)