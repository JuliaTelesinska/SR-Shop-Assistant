import speech_recognition as sr
import pyttsx3
from cart import Product, ShoppingCart

# setting up the voice assistant
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()

milk = Product("milk", 5)
eggs = Product("eggs", 10)
shrimp = Product("shrimp", 20)
spinach = Product("spinach", 3)
cat_food = Product("cat food", 2)
lollipop = Product("lollipop", 3)
beef = Product("beef", 9)
apple = Product("beef", 3)

def greet():
    print("Welcome to the SR-Shop-Assistant.")
    engine.say("Welcome to the SR-Shop-Assistant.")
    engine.runAndWait()
    print(f"Currently there are {len(Product.all_products)} different items in stock.")
    print("-"*40)

def set_budget():
    with sr.Microphone() as source:
        print("Please enter your budget:")
        engine.say("Please enter your budget:")
        engine.runAndWait()
        audio = r.listen(source,7,5)
    try:
        budget = r.recognize_google(audio)
        try:
            budget=int(budget)
            if budget <= 0:
                print("Specified budget doesn't allow for spending.")
                return set_budget()
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
    print(("-"*40))
    with sr.Microphone() as source:
        print("Choose product. If you would like to stop adding products say: 'FINISH'")
        show_product_shelf()
        engine.say("Choose product")
        engine.runAndWait()
        audio = r.listen(source, 7,5)

    try:
        # product = input()
        product = r.recognize_google(audio)
        print(product)
        if product == "finish":
            return get_command(my_cart)
        elif product in [item.name for item in Product.all_products]:
            matched_product = next((item for item in Product.all_products if item.name == product))
            # with sr.Microphone() as source:
            #     print("Enter amount: ")
            #     engine.say("Enter amount")
            #     engine.runAndWait()
            #     audio = r.listen(source)
            try:
                print("Enter amount in the console: ")
                engine.say("Enter amount in the console")
                engine.runAndWait()               
                amount = input()

                try:
                    amount = int(amount)
                    if amount <= 0:
                        print("Wrong amount. Try again.")
                        engine.say("Wrong amount. Try again.")
                        engine.runAndWait()
                        return go_shopping(my_cart)
                    my_cart.add_to_cart(matched_product, amount)
                except ValueError:
                    print("Amount must be a number. Try again.")
                    engine.say("Amount must be a number. Try again.")
                    engine.runAndWait()
                    return go_shopping(my_cart)
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that. Please try again.")
                engine.say("Sorry, I didn't understand that. Please try again.")
                engine.runAndWait()
                return go_shopping(my_cart)
            except sr.WaitTimeoutError:
                print("Timed out")
                return go_shopping(my_cart)
        else:
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
    try:
        if bool(my_cart.items_in_cart):
            with sr.Microphone() as source:
                print("Choose item to remove from cart. Say 'exit' if you want to finish removing.")
                engine.say("Choose item to remove from cart")
                engine.runAndWait()
                my_cart.show_cart()
                audio_product = r.listen(source,7,5)

            try:
            # product = input()
                product = r.recognize_google(audio_product)
                print(product)
                if product == "exit":
                    return get_command(my_cart)
                elif product in [item.name for item in Product.all_products]:
                    matched_product = next((item for item in Product.all_products if item.name == product))
                    try:
                        engine.say("Enter amount in console")
                        engine.runAndWait()
                        print("Enter amount in console:")
                        amount = input()

                        try:
                            amount =int(amount)
                            print(amount)
                            my_cart.remove_item(matched_product, amount)
                            my_cart.show_cart()
                            remove_from_cart(my_cart)
                        except:
                            print("Amount must be a number. Try again.")
                            engine.say("Amount must be a number. Try again.")
                            engine.runAndWait()
                            return remove_from_cart(my_cart)
                    except sr.UnknownValueError:
                        print("Sorry, I didn't understand that. Please try again.")
                        engine.say("Sorry, I didn't understand that. Please try again.")
                        engine.runAndWait()
                        return remove_from_cart(my_cart)

                else:
                    print(f"There is no {product} in your cart. Try again.")
                    engine.say(f"There is no {product} in your cart. Try again.")
                    engine.runAndWait()
                    return remove_from_cart(my_cart)
                
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that. Please try again.")
                engine.say("Sorry, I didn't understand that. Please try again.")
                engine.runAndWait()
                return remove_from_cart(my_cart)

            except sr.WaitTimeoutError:
                print("Timed out.")
                return remove_from_cart(my_cart)  
    
        else:
            print("Your cart is empty. Nothing to remove.")
            engine.say("Your cart is empty. Nothing to remove.")
            engine.runAndWait()
            return get_command(my_cart)
        
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        engine.say("Sorry, I didn't understand that. Please try again.")
        engine.runAndWait()
        return remove_from_cart(my_cart)

    except sr.WaitTimeoutError:
        print("Timed out.")
        return remove_from_cart(my_cart)  

def get_command(my_cart):
    with sr.Microphone() as source:
        print("""
-----------------------------------------------------------------
| If you would like to check your current balance say 'BUDGET'. |
| If you want to add a product say 'APPEND'.                    |
| To see all available products say 'SHELF'                     |
| If you want to delete a product from cart say 'DELETE'.       |
| To check your cart say 'SHOW CART'.                           |
| To finish all your shopping say 'FINISH'.                     |
-----------------------------------------------------------------
    """)
        engine.say("Choose command: budget, append, shelf, delete, show cart or finish")
        engine.runAndWait()
        audio = r.listen(source,5,5)            
    try:
        command = r.recognize_google(audio)
        command = command.lower()
        print(command)
        # command = input()
        if command == "budget":
            my_cart.inform_on_total(my_cart.calculate_total())
            return get_command(my_cart)
        elif command =="append":
            return go_shopping(my_cart)
        elif command =="shelf":
            show_product_shelf()
            return get_command(my_cart)
        elif command =="show cart":
            my_cart.show_cart()
            return get_command(my_cart)
        elif command =="delete":
            remove_from_cart(my_cart)
        elif command =="finish":
            return checkout(my_cart)
        else:
            print("Command not recognized")
            engine.say("Command not recognized")
            engine.runAndWait()
            return get_command(my_cart)
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Please try again.")
        engine.say("Sorry, I didn't understand that. Please try again.")
        engine.runAndWait()
        return get_command(my_cart)  

def checkout(my_cart):
    if my_cart.checkout_cart()<0:
        print(f"You can't afford your groceries. Your budget was exceeded by ${abs(my_cart.checkout_cart())}.")
        engine.say(f"You can't afford your groceries. Your budget was exceeded by ${abs(my_cart.checkout_cart())}.")
        engine.runAndWait()
        print("You should remove some products from your cart")
        engine.say("You should remove some products from your cart")
        engine.runAndWait()
        while my_cart.checkout_cart()<0:
            remove_from_cart(my_cart)
    else: 
        print(f"Your total is: ${my_cart.calculate_total()}. You receive ${my_cart.checkout_cart()} in change. Thank you for shopping with us.")
        engine.say(f"Your total is: ${my_cart.calculate_total()}. You receive ${my_cart.checkout_cart()} in change. Thank you for shopping with us.")
        engine.runAndWait()
    return

if __name__ == "__main__":
    while True:
        greet()
        cart = set_budget()
        get_command(cart)
        break