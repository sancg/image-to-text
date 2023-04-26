class Invoice:

    def __init__(self, vendor_name: str, bill_to_address: str, ship_to_name: str, ship_to_address: str, line_items: dict):
        self.vendor_name = vendor_name
        self.bill_to_address = bill_to_address
        self.ship_to_name = ship_to_name
        self.ship_to_address = ship_to_address
        self.line_items = line_items


class Items:

    def __init__(self, quantity, description, price):
        self.quantity = quantity
        self.description = description
        self.price = price
