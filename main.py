import speech_recognition as sr
import pyttsx3
from cart import Product, ShoppingCart

# setting up the voice assistant
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()


def set_budget():
    with sr.Microphone() as source:
        print("Please state your budget:")
        engine.say("Please state your budget.")
        engine.runAndWait()
        audio = r.listen(source)

    # Use speech recognition to convert the user's response to text
    try:
        budget = int(r.recognize_google(audio))
        print(f"Your budget is {budget}")
        engine.say(f"Your budget is {budget}.")
        engine.runAndWait()
        my_cart = ShoppingCart(budget)
        print(my_cart.budget)
        return budget
    
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        engine.say("Sorry, I didn't understand that. Please try again.")
        engine.runAndWait()
        return set_budget()
    
def go_shopping():
    pass

if __name__ == "__main__":
    set_budget()