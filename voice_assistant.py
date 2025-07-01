import speech_recognition as sr
import pyttsx3
import datetime
import json
import os

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.donor_data = {}
        self.blood_groups = {"a+", "a-", "b+", "b-", "ab+", "ab-", "o+", "o-"}
        os.makedirs("donors", exist_ok=True)

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, prompt=""):
        if prompt:
            self.speak(prompt)

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language='en-IN')
                print(f"User: {text}")
                return text.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Let's try again.")
                return self.listen(prompt)
            except sr.RequestError:
                self.speak("Speech service is currently unavailable.")
                return ""

    def ask_and_validate(self, prompt, field, validator=None):
        while True:
            response = self.listen(prompt)
            if not response:
                continue
            if validator:
                valid, result = validator(response)
                if valid:
                    self.donor_data[field] = result
                    break
                else:
                    self.speak(result)
            else:
                self.donor_data[field] = response
                break

    def validate_age(self, response):
        try:
            age = int(response)
            if 18 <= age <= 65:
                return True, age
            return False, "Age must be between 18 and 65."
        except ValueError:
            return False, "Please say a valid number for age."

    def validate_phone(self, response):
        digits = ''.join(filter(str.isdigit, response))
        if len(digits) == 10:
            return True, digits
        return False, "Please provide a 10-digit phone number."

    def validate_blood_group(self, response):
        spoken_map = {
            "a positive": "A+",
            "a negative": "A-",
            "b positive": "B+",
            "b negative": "B-",
            "ab positive": "AB+",
            "ab negative": "AB-",
            "o positive": "O+",
            "o negative": "O-",
            "i positive": "A+", 
            "i negative": "A-"
        }

        cleaned = response.lower().replace(" ", "")
        spoken_form = response.lower().strip()

        if spoken_form in spoken_map:
            return True, spoken_map[spoken_form]

        blood_group = cleaned.upper()
        if blood_group in {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}:
            return True, blood_group

        return False, "That blood group is not recognized. Please try again."

    def collect_info(self):
        self.donor_data = {
            "registrationMethod": "voice",
            "timestamp": datetime.datetime.now().isoformat()
        }

        self.ask_and_validate("Please say your full name", "name")
        self.ask_and_validate("Please say your age", "age", self.validate_age)
        self.ask_and_validate("Please say your blood group", "bloodGroup", self.validate_blood_group)
        self.ask_and_validate("Please say your 10-digit phone number", "phone", self.validate_phone)
        self.ask_and_validate("Please say your location", "location")

        self.confirm_data()

    def confirm_data(self):
        self.speak("Please confirm your details.")
        for field, value in self.donor_data.items():
            if field not in ['registrationMethod', 'timestamp']:
                self.speak(f"{field}: {value}")

        confirmation = self.listen("Are these details correct? Please say yes or no.")
        if "yes" in confirmation:
            self.save_data()
            self.speak("Thank you! You are now registered as a blood donor.")
        else:
            self.speak("Let's try again.")
            self.collect_info()

    def save_data(self):
        filename = f"donors/donor_voice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(self.donor_data, f, indent=2)

    def run(self):
        self.speak("Welcome to the Voice-Based Blood Donor Registration System.")
        self.collect_info()


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

    
