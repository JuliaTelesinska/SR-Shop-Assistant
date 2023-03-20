import speech_recognition as sr
import pyttsx3
import sys
from cart import Product, ShoppingCart

# setting up the voice assistant
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()

milk = Product("milk", 5, 20)
eggs = Product("eggs", 10, 12)
shrimp = Product("shrimp", 20, 5)
spinach = Product("spinach", 3, 10)
cat_food = Product("cat food", 2, 8)
bread = Product("bread", 3, 2)
beef = Product("beef", 9, 6)


def set_budget():
    # with sr.Microphone() as source:
    #     print("Please state your budget:")
    #     engine.say("Please state your budget.")
    #     engine.runAndWait()
    #     audio = r.listen(source)

    # Use speech recognition to convert the user's response to text
    try:
        print("Please enter your budget:")
        engine.say("Please enter your budget:")
        engine.runAndWait()
        budget=input()
        try:
            budget=int(budget)
            # budget = int(r.recognize_google(audio))
        except:
            print("The budget must be a number!")
            engine.say("The budget must be a number!")
            engine.runAndWait()
            return set_budget()
        print(f"Your budget is {budget}")
        engine.say(f"Your budget is {budget}.")
        engine.runAndWait()
        my_cart = ShoppingCart(budget)
        print(my_cart.budget)
        return my_cart
    
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        engine.say("Sorry, I didn't understand that. Please try again.")
        engine.runAndWait()
        return set_budget()
    
def go_shopping(my_cart):
    # print("Products avalaible in shop:")
    # print(Product.all_products)

    # with sr.Microphone() as source:
    #     print("Choose product you would like to buy:")
    #     engine.say("Choose product you would like to buy")
    #     engine.runAndWait()
    #     audio = r.listen(source)
    try:
        # product = r.recognize_google(audio)
        print("Choose product. If you would like to finish your shopping, say: 'finish'")
        engine.say("Choose product. If you would like to finish your shopping, say: finish")
        engine.runAndWait()
        product = input()
        if product == "finish":
            return
        product_added = None
        for item in Product.all_products:
            if item.name == str(product):
                print("Enter the amount")
                engine.say("Enter the amount")
                engine.runAndWait()
                amount = input()
                amount = int(amount) #obsluga bledu jesli amount nie da sie przekonwertowac na int                
                product_added = Product(item.name, item.price, item.amount)
                my_cart.add_to_cart(product_added, amount)
                break
            
        if product_added == None:
            print(f"There is no {product} in the shop.")
            engine.say(f"There is no {product} in the shop.")
            engine.runAndWait()
            return go_shopping(my_cart)
        my_cart.show_cart()
            
        return go_shopping(my_cart)

    
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        engine.say("Sorry, I didn't understand that. Please try again.")
        engine.runAndWait()
        return go_shopping(my_cart)  



if __name__ == "__main__":
    print("Products avalaible in shop:")
    print(Product.all_products)
    cart = set_budget()
    go_shopping(cart)
    print("Your shopping is finished")
    engine.say("Your shopping is finished")
    cart.show_cart()
    cart.calculate_budget()
    #TO DO - dodac remove artykulow, w przypadku przekroczenia kwoty pod koniec zakupow wyswietlanie karty i wzkazanie produktow do usuniecia,
    #ale tez zeby mozna bylo usunac podczas zakupow