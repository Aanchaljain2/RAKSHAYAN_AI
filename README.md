# 🏍️ Rakshayan AI

### AI-Powered Smart Helmet Emergency Assistance System

Rakshayan AI is an intelligent emergency-assistance system designed for two-wheeler riders. It uses Natural Language Processing (NLP), Machine Learning, voice interaction, GPS location detection, and SOS communication to assist riders during emergency situations.

---

## 🚨 Problem Statement

Two-wheeler riders can face accidents, medical emergencies, fatigue, vehicle problems, helmet-related issues, or situations requiring police assistance.

During an emergency, communicating the problem and current location quickly can be difficult.

Rakshayan AI aims to provide an intelligent and simple interface where a rider can describe their situation naturally, allowing the system to identify the type of emergency and assist in initiating an SOS.

---

## 🎯 Objectives

- Detect different types of rider emergencies using Machine Learning.
- Understand natural-language descriptions rather than relying only on fixed keywords.
- Support voice-based interaction.
- Detect accident, medical, police, fatigue, helmet, and bike-related issues.
- Capture the rider's GPS location.
- Generate a Google Maps location link.
- Ask for explicit confirmation before initiating an SOS.
- Prepare emergency information containing the rider's details, emergency type, location, and time.
- Provide a foundation for future smart-helmet hardware integration.

---

## 🧠 AI Emergency Detection

Rakshayan AI currently supports the following intent categories:

| Intent | Description |
|---|---|
| `accident` | Accident/crash situations |
| `medical` | Medical or health emergencies |
| `police` | Situations requiring police assistance |
| `fatigue` | Rider tiredness or sleepiness |
| `helmet_issue` | Helmet-related problems |
| `bike_issue` | Two-wheeler or mechanical problems |
| `normal` | Ordinary non-emergency statements |

The system is trained to understand different ways of describing the same situation.

---

## ⚙️ How It Works

```text
                 Rider
                   │
                   ▼
          Voice / Text Input
                   │
                   ▼
          Speech-to-Text
          (Voice Input)
                   │
                   ▼
          TF-IDF Feature
             Extraction
                   │
                   ▼
       Logistic Regression
          Intent Classifier
                   │
                   ▼
          Emergency Detection
                   │
          ┌────────┴────────┐
          │                 │
       Normal           Emergency
          │                 │
          ▼                 ▼
      Continue       Ask for SOS
      Monitoring       Confirmation
                            │
                    ┌───────┴───────┐
                    │               │
                   YES              NO
                    │               │
                    ▼               ▼
              Generate SOS       Cancel SOS
                    │
                    ▼
              GPS Location
                    │
                    ▼
             Google Maps Link
                    │
                    ▼
             SMS / API Layer
---

## 🛠️ Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- Joblib
- TF-IDF Vectorization
- Logistic Regression
- SpeechRecognition
- PyAudio
- pyttsx3
- HTML / CSS / JavaScript
- Browser Geolocation API
- Google Maps
- Twilio SMS API

---

## 🤖 Machine Learning Methodology

The emergency detection module uses Natural Language Processing and supervised Machine Learning.

### Text Processing

The rider's sentence is converted into numerical features using **TF-IDF (Term Frequency-Inverse Document Frequency)**.

The system also considers word combinations using unigram and bigram features.

### Classification

A **Logistic Regression** classifier is trained to classify the input into one of the supported intent categories.

The trained model is saved using Joblib and loaded by the Flask application during runtime.

---

## 🎤 Voice Interaction

Rakshayan AI supports voice-based interaction.

The system:

1. Activates the microphone.
2. Captures the rider's speech.
3. Converts speech into text using SpeechRecognition.
4. Sends the text to the ML model.
5. Identifies the rider's intent.
6. Generates an appropriate response.
7. Requests explicit SOS confirmation when an emergency is detected.

---

## 📍 GPS Location Detection

The system uses GPS/location data to obtain the rider's current coordinates.

The latitude and longitude are converted into a Google Maps link:

```text
https://www.google.com/maps?q=latitude,longitude
This location can be included in the emergency information

🆘 SOS System

Rakshayan AI does not automatically send an SOS simply because an emergency is detected.

The system first asks the rider for confirmation.
Rider: I have met with an accident.

AI: I detected an accident. Do you want me to send an SOS?

Rider: Yes.

AI: SOS confirmed.
Emergency Information

The generated SOS information can contain:

* Emergency type
* Rider name
* Rider phone number
* Emergency contact
* Emergency contact number
* Latitude
* Longitude
* Google Maps location
* Date and time

The system is designed to communicate this information through an SMS/API layer.
RAKSHAYAN_AI/
│
├── dataset/
│   └── emergency_data.csv
│
├── model/
│   └── emergency_model.pkl
│
├── templates/
│   └── index.html
│
├── static/
│
├── logs/
│
├── .venv/
│
├── app.py
├── speech.py
├── train_model.py
├── config.py
├── contacts.json
├── requirements.txt
├── .env
└── README.md
🔐 Security

Sensitive credentials such as API keys, authentication tokens, and phone numbers are stored using environment variables.

The .env file is excluded from Git using .gitignore.

Never upload API credentials or authentication tokens to GitHub.
Current Prototype Status

The current Rakshayan AI prototype includes:

* ✅ Machine Learning emergency classification
* ✅ Multiple emergency categories
* ✅ Natural-language input
* ✅ Voice input
* ✅ AI response generation
* ✅ SOS confirmation
* ✅ Dashboard interface
* ✅ GPS location detection
* ✅ Google Maps location generation
* ✅ Emergency contact management
* 🔄 SMS/API communication integration
* 🔄 Improvement of normal/unknown input detection
🔮 Future Scope

Future versions of Rakshayan AI can integrate directly with smart-helmet hardware.

Possible additions include:

* ESP32/Arduino integration
* Alcohol detection sensor
* Drowsiness/sleep detection
* Helmet-wearing detection
* Engine ON/OFF detection
* Heart-rate monitoring
* Body-temperature monitoring
* Fall/impact detection
* GSM communication
* Real-time emergency alerts
* Cloud-based monitoring dashboard
* Direct emergency-service integration
Academic Relevance

Rakshayan AI combines concepts from multiple engineering domains:

* Machine Learning
* Natural Language Processing
* Embedded Systems
* Wireless Communication
* IoT
* Web Development
* GPS/GNSS
* Emergency Communication Systems

This makes the project particularly relevant to Electronics and Telecommunication engineering.
Disclaimer

Rakshayan AI is an academic prototype developed for demonstration and educational purposes.

It should not be considered a replacement for official emergency services or professional medical assistance.

Project Information

Project: Rakshayan AI
Type: Final Year Engineering Project
Branch: Electronics and Telecommunication Engineering
Platform: Python + Flask
