from tabulate import tabulate


# Shoe object
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product_name = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        shoe_details = f"{self.code}:\t{self.product_name}\t£{self.cost}\t{self.quantity} in {self.country}"
        return shoe_details


# data file location
shoe_data = "inventory.txt"
image = "image.txt"

# list of shoe objects
shoe_inventory = []


# ***Functions***

# load data from file and store in list of shoe objects
def read_shoes_data():
    try:
        with open(shoe_data, 'r') as data:
            for index, line in enumerate(data):
                if index == 0:
                    continue
                temp_list = line.split(',')
                shoe = Shoe(temp_list[0], temp_list[1], temp_list[2], float(temp_list[3]), int(temp_list[4]))
                shoe_inventory.append(shoe)
    except FileNotFoundError or FileExistsError as error:
        print(error)


# add new shoe object
def add_shoe_data(shoe):
    with open(shoe_data, 'a') as file:
        file.write(f"{shoe.country},{shoe.code},{shoe.product_name},{shoe.cost},{shoe.quantity}\n")


# save all shoe objects (overwrites current data)
def save_all_shoe_data(inventory):
    with open(shoe_data, 'w') as data:
        for shoe in inventory:
            data.write(f"{shoe.country},{shoe.code},{shoe.product_name},{shoe.cost},{shoe.quantity}\n")


# add new shoe details and save to list and to file
def capture_shoes():
    print("\nPlease enter the details of the new shoe.")
    new_code = input("Product Code: ")
    new_name = input("Product Name: ")
    new_cost = float(input("Product Cost: £"))
    new_quantity = int(input("Product Quantity: "))
    new_country = input("Product Location: ")

    new_shoe = Shoe(new_country, new_code, new_name, new_cost, new_quantity)
    shoe_inventory.append(new_shoe)

    add_shoe_data(new_shoe)

    print(f"\nNew shoe '{new_name}' added to inventory.")


# formats data to be displayed neatly
def create_data_table():
    data_row = []
    for shoe in shoe_inventory:
        data_column = [shoe.code, shoe.product_name, shoe.cost, shoe.country, shoe.quantity]
        data_row.append(data_column)

    table_headers = ["Code", "Product Name", "Cost", "Location", "Quantity"]

    return data_row, table_headers


# prints out all data in a formatted table
def view_all():
    table, headers = create_data_table()
    print(tabulate(table, headers=headers, showindex=True))


# finds shoe with the lowest stock, gives option to restock
def re_stock():
    current_lowest = shoe_inventory[0]
    for shoe in shoe_inventory:
        if shoe.quantity < current_lowest.quantity:
            current_lowest = shoe

    try:
        command = input(f"Do you want to restock the {current_lowest.product_name}? Quantity = {current_lowest.quantity}. Y/N ").lower()
        if command == 'y':
            amount = int(input("How many do you want to add to the stock? "))

            current_lowest.quantity += amount
            index = shoe_inventory.index(current_lowest)
            shoe_inventory[index].quantity = current_lowest.quantity
            save_all_shoe_data(shoe_inventory)

    except ValueError as error:
        print(error)


# search by shoe code
def search_shoe():
    search_successful = False
    while not search_successful:
        shoe_code = input("Please enter the code of the item you're searching for: ")
        for shoe in shoe_inventory:
            if shoe.code == shoe_code:
                search_successful = True
                print(shoe.__str__())
                return

        if not search_successful:
            print("I'm sorry, that product code wasn't recognised. Please try again.")


# prints out total value of all items
def value_per_item():
    value_list = []
    for shoe in shoe_inventory:
        value_list.append([shoe.product_name, shoe.cost * shoe.quantity])

    print(tabulate(value_list, headers=["Product Name", "Total Value"]))


# displays the shoes with the highest quantity
def highest_qty():

    current_highest = shoe_inventory[0]
    for shoe in shoe_inventory:
        if shoe.quantity > current_highest.quantity:
            current_highest = shoe

    print(f"{current_highest.product_name} on sale now!")


# display image
def display_image():
    with open(image, 'r') as image_file:
        for line in image_file:
            print(line, end="")
    print("               WELCOME TO YOUR INVENTORY MANAGER")


# Main program
read_shoes_data()
display_image()
# Menu
while True:
    user_command = input("\nWhat would you like to do?\n"
                         "A > Add a new shoe\n"
                         "I > View Inventory\n"
                         "R > Restock an item\n"
                         "S > Search for an item using its product code\n"
                         "V > View the total value for each item\n"
                         "H > View product with the highest quantity\n"
                         "Q > Quit\n"
                         ": ").lower()

    match user_command:
        case 'a':
            capture_shoes()
        case 'i':
            view_all()
        case 'r':
            re_stock()
        case 's':
            search_shoe()
        case 'v':
            value_per_item()
        case 'h':
            highest_qty()
        case 'q':
            break
        case _:
            print("I'm sorry, I didn't recognise that command. Please try again")
