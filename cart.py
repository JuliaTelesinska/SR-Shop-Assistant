class Product:
    all_products = []

    def __init__(self, name: str, price: int, amount: int):
        self.name = name
        self.price = price
        self.amount = amount
        Product.all_products.append(self)
    
    def __str__(self):
        return f"Product name: {self.name},\
            \nProduct price: ${self.price},\
            \nAmount available: {self.amount}."
    
    def __repr__(self):
        return self.name

class ShoppingCart:
    def __init__(self, budget: int):
        self.budget = budget
        self.items_in_cart = {}
    
    #TODO take amount declared inside Product class into account
    # when adding product to cart
    def add_to_cart(self, item: Product, amount: int):
        if item.name not in self.items_in_cart:
            self.items_in_cart[item.name] = (amount, amount*item.price)
        else:
            current_amount, current_total_price = self.items_in_cart[item.name]
            new_amount = current_amount + amount
            new_total_price = current_total_price + item.price * amount
            self.items_in_cart[item.name] = (new_amount, new_total_price)
    
    def show_cart(self):
        for item, amount_price in self.items_in_cart.items():
            print(f"> {amount_price[0]} * {item} = ${amount_price[1]}")

    def calculate_budget(self):
        total_price = 0
        for item, amount_price in self.items_in_cart.items():
            total_price += amount_price[1]
        if total_price > self.budget:
            print(f"You're ${total_price-self.budget} over budget! Your total is ${total_price}.")
        else:
            print(f"Your total is ${total_price}.")


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