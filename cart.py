class Product:
    all_products = []

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
        for product in Product.all_products:
            if product.name == name:
                return
        Product.all_products.append(self)
    
    def __str__(self):
        return f"Product name: {self.name},\
            \nProduct price: ${self.price}"
    
    def __repr__(self):
        return self.name

class ShoppingCart:
    def __init__(self, budget: int):
        self.budget = budget
        self.items_in_cart = {}
    
    def add_to_cart(self, item: Product, amount: int):
        if item.name not in self.items_in_cart:
            self.items_in_cart[item.name] = (amount, amount*item.price)
        else:
            current_amount, current_total_price = self.items_in_cart[item.name]
            new_amount = current_amount + amount
            new_total_price = current_total_price + item.price * amount
            self.items_in_cart[item.name] = (new_amount, new_total_price)
          
    def remove_item(self, item: Product, amount: int):
        if item.name in self.items_in_cart:
            current_amount, current_total_price = self.items_in_cart[item.name]
            if amount > current_amount:
                amount = current_amount
            if amount == current_amount:
                self.items_in_cart.pop(item.name)
            else:
                new_amount = current_amount - amount
                new_total_price = current_total_price - item.price * amount
                self.items_in_cart[item.name] = (new_amount, new_total_price)
        else:
            print(f"There is no {item.name} in your cart.")
    
    def show_cart(self):
        for item, amount_price in self.items_in_cart.items():
            print(f"> {amount_price[0]} * {item} = ${amount_price[1]}")
        if not self.items_in_cart:
            print("Your shopping cart is empty")

    def calculate_total(self):
        total_price = 0
        for item, amount_price in self.items_in_cart.items():
            total_price += amount_price[1]
        return total_price
    
    def inform_on_total(self, total_price):
        if total_price > self.budget:
            print(f"You're ${total_price-self.budget} over the original budget of {self.budget}! Your current total is ${total_price}.")
        else:
            print(f"Your budget is ${self.budget}. Your current total is ${total_price}.")

    def checkout_cart(self):
        final_checkout = self.budget - self.calculate_total()
        return final_checkout


# milk = Product("milk", 5, 20)
# eggs = Product("eggs", 10, 12)
# shrimp = Product("shrimp", 20, 5)
# spinach = Product("spinach", 3, 10)
# cat_food = Product("cat food", 2, 8)
# bread = Product("bread", 3, 2)
# beef = Product("beef", 9, 6)

# if __name__ == "__main__":
#     print(Product.all_products)
#     cart = ShoppingCart(80)
#     cart.add_to_cart(milk, 15)
#     cart.add_to_cart(milk, 1)
#     cart.add_to_cart(eggs, 2)
#     cart.show_cart()
#     print(Product.all_products)
#     cart.calculate_budget()

# Wyprintowane bo przy wywoływaniu w mainie lista artykulow jest podwojona