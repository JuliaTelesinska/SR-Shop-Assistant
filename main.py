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

def greet():
    print("Welcome to the SR-Shop-Assistant.")
    engine.say("Welcome to the Ladybug Shop")
    engine.runAndWait()
    print(f"Currently there are {len(Product.all_products)} different items in stock.")
    print("-"*40)

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
            if budget <= 0:
                print("Specified budget doesn't allow for spending.")
                return set_budget()
            # budget = int(r.recognize_google(audio))
        except:
            print("The budget must be a number!")
            print("-"*40)
            engine.say("The budget must be a number!")
            engine.runAndWait()
            return set_budget()
        print(f"Your budget is ${budget}")
        print("-"*40)
        engine.say(f"Your budget is ${budget}.")
        engine.runAndWait()
        my_cart = ShoppingCart(budget)
        return my_cart
    
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        engine.say("Sorry, I didn't understand that. Please try again.")
        engine.runAndWait()
        return set_budget()
    
def show_product_shelf():
    for product in Product.all_products:
        print(f"{product.name.capitalize()}, price: ${product.price}")
    
def go_shopping(my_cart):
    print("Products avalaible in shop:")
    print(Product.all_products)
    print(("-"*40))
    # with sr.Microphone() as source:
    #     print("Choose product you would like to buy:")
    #     engine.say("Choose product you would like to buy")
    #     engine.runAndWait()
    #     audio = r.listen(source)
    try:
        # product = r.recognize_google(audio)
        print("Choose product. If you would like to stop adding products say: 'FINISH'")
        engine.say("Choose product. If you would like to stop adding products say: finish")
        show_product_shelf()
        engine.runAndWait()
        product = input()
        if product == "finish":
            return get_command(my_cart)
        product_added = None
        for item in Product.all_products:
            if item.name == product:
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

def remove_from_cart(my_cart):
    print("Which item to remove from cart:")
    engine.say("Which item to remove from cart:")
    my_cart.show_cart()

def get_command(my_cart):
    try:
        print("""
-----------------------------------------------------------------
| If you would like to check your current balance say 'BUDGET'. |
| If you want to add a product say 'ADD'.                       |
| If you want to delete a product from cart say 'DELETE'.       |
| To check your cart say 'SHOW CART'.                           |
| To finish all your shopping say 'FINISH'.                     |
-----------------------------------------------------------------
    """)
        engine.say("Choose command: budget, add, delete, show cart or finish")
        engine.runAndWait()
        command = input()
        if command == "budget":
            print(f"Your budget is: ${my_cart.budget}")
            engine.say(f"Your budget is: ${my_cart.budget}")
            return get_command(my_cart)
        elif command =="add":
            return go_shopping(my_cart)
        elif command =="show cart":
            my_cart.show_cart()
            return get_command(my_cart)
        elif command =="delete":
            pass
        elif command =="finish":
            return checkout(my_cart)
        else:
            print("Command not recognized")
            engine.say("Command not recognized")
            return get_command()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        engine.say("Sorry, I didn't understand that. Please try again.")
        engine.runAndWait()
        return get_command(my_cart)  

def checkout(my_cart):
    print(f"Your total is: ${my_cart.checkout_cart()}. Thank you for shopping with us.")
    engine.say(f"Your total is: ${my_cart.checkout_cart()}. Thank you for shopping with us.")
    engine.runAndWait()
    return

if __name__ == "__main__":
    while True:
        greet()
        cart = set_budget()
        get_command(cart)
        break
    #TO DO - dodac remove artykulow, w przypadku przekroczenia kwoty pod koniec zakupow wyswietlanie karty i wzkazanie produktow do usuniecia,
    #ale tez zeby mozna bylo usunac podczas zakupow