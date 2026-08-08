def calculate_total(price, quantity):
    total = price * quantity
    return total


def apply_discount(total, discount):
    return total - discount


price = 100
quantity = 2
discount = "10%"

total = calculate_total(price, quantity)
final_price = apply_discount(total, discount)

print("Final Price:", final_price)
