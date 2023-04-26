import re


class Capture():
    PATTERN_BILL = re.compile(
        r".*\b(SPECIAL NOTICE)\b|^\b.*FORUM\b", flags=re.M)
    PATTERN_VENDOR = re.compile(
        r'(\bFORUM\b)?.*?\bCOMPANY\b', flags=re.M | re.S)
    PATTERN_ADDRESS = re.compile(
        r'((?<=STO:).*SHIPMENT|(?<=TO:).*SHIPMENT)', flags=re.S)
    PATTERN_LINE_ITEMS = re.compile(
        r'(?=QUANTITY).*(?:ACCOUNTING)', flags=re.I | re.S)

    def __init__(self, company_name: str, raw_text: str = '', pattern_bill=PATTERN_BILL, pattern_vendor=PATTERN_VENDOR, pattern_address=PATTERN_ADDRESS, pattern_line_items=PATTERN_LINE_ITEMS):
        self.company_name = company_name.title()
        self.raw_text = raw_text.strip()
        self.pattern_bill = pattern_bill
        self.pattern_vendor = pattern_vendor
        self.pattern_address = pattern_address
        self.pattern_line_items = pattern_line_items
        self.__num_invoice = 0
        self.__list_text_to_process = []
        self.__invoice = []
        self.__ship_to_name = ''
        self.__structure_text()

    def __structure_text(self, filter_pattern: str = '') -> list:
        """Method to organize the processed documents into a List that can be iterated in the extraction step.

        Args:
            filter_pattern: Future improvement to facilitate a modular match-making conditional.
        Returns:
            list: The invoice list in which contains the raw_text for each of them.
        """
        invoice_list = self.pattern_bill.split(self.raw_text)

        def find_bill(elem) -> int:
            return elem and len(elem) > 100

        self.__list_text_to_process = list(filter(find_bill, invoice_list))
        return self.__list_text_to_process

    def get_total_docs_process(self):
        finder = self.pattern_vendor.findall(self.raw_text)
        if finder:
            self.__num_invoice = len(finder)
        return self.__num_invoice

    def extract_data(self):
        """Loop through the documents identified and extract all variables as needed.
        And it will fill the protected List called __invoice
        """
        if self.__list_text_to_process:
            for bill in self.__list_text_to_process:
                result = {}
                result['vendor_raw_name'] = self.get_raw_title(bill)
                result['vendor_name'] = self.get_title(
                    result['vendor_raw_name'])

                result['ship_to_address'] = self.get_ship_to_address(bill)
                result['ship_to_name'] = self.__ship_to_name
                result['line_items'] = self.get_line_items(bill)
                # print(result['ship_to_address'])
                self.__invoice.append(result)

        return self.__invoice

    def get_raw_title(self, raw_text):
        raw_title = self.pattern_vendor.search(raw_text)
        if not raw_title:
            return None
        return raw_title.group(0)

    def get_title(self, raw_title):
        if not raw_title:
            return None
        title_result = self.company_name.strip()
        reg_replacement = re.compile(r'\s+')

        regex_find_title = reg_replacement.sub(
            r'\\b|\\b', self.company_name.strip())
        regex_find_title = re.compile(f'(^{regex_find_title})', re.M | re.I)
        match = regex_find_title.findall(raw_title)

        if not match:
            return title_result

        title_result = ' '.join(match).title()
        return title_result

    def get_ship_to_address(self, raw_text: str):
        """This method extract the block that indicates the address from supplier y customer,
        and then process it with a regex in which separates the strings by continuos whitespaces and tabs.
        Finally it cleans the result list with the desire parameters.

        Args:
            raw_text (str): _description_

        Returns:
            str: Returns the raw block of shipment section if do not exist the matching regex.
            Otherwise, it will create a comprehensive address according with the raw_text.
        """
        result = ''
        self.__ship_to_name = ''

        raw_ship_address = self.pattern_address.search(raw_text)
        if not raw_ship_address:
            return None

        reg_ship_address = re.compile(
            r"(?:\s{3,}|\t{2}).*", re.M | re.I | re.X)

        result = raw_ship_address.group(0)
        extracted_ship_address = reg_ship_address.findall(result)

        if not extracted_ship_address:
            return result

        """Loop through each element of the extracted_ship_address and compare if the word ATTN
        do not exists in the given string.

        What would happened if the list has an empty value?
        """
        ship_name = list(
            filter(lambda elem: 'ATTN' in elem, extracted_ship_address))
        if ship_name:
            self.__ship_to_name = ', '.join(ship_name)
        filtered_list = list(
            filter(lambda elem: 'ATTN' not in elem, extracted_ship_address))
        clean_ship_address = [re.sub(r'[^\w\s]+', '', element).strip()
                              for element in filtered_list]

        result = ', '.join(clean_ship_address).strip()

        return result

    def get_line_items(
        self,
        raw_text,
        # pattern_quantity=r'^\d+(?:\s+)',
        pattern_quantity=r'^\d+(?:[\.,]\d+)?\s{2,}',
        pattern_price=r'\$\d+.*',
        pattern_description=r'^\d+.*\b[a-zA-Z]+.*'
    ):
        """Method to extract the portion of the detail invoice.


        Args:
            raw_text (str): general text to inspect 
            pattern_quantity (regexp, optional): To be modular and useful this regex detects numbers at the start of the line that its follows by 2 whitespaces (Based on invoice analysis)
            . Defaults to r'^\d+(?:[\.,]\d+)?\s{2,}'.
            pattern_price (regexp, optional): _description_. Defaults to r'$\d+.*'.
            pattern_description (regexp, optional): _description_. Defaults to r'^\d+.*\b[a-zA-Z]+.*'.

        Returns:
            _type_: _description_
        """
        line_items = []
        raw_line_items = self.pattern_line_items.search(raw_text)
        if not raw_line_items:
            return None

        raw_line_items = raw_line_items.group(0)

        pattern_quantity = re.compile(pattern_quantity, re.M)
        quantity = pattern_quantity.findall(raw_line_items)

        pattern_price = re.compile(pattern_price, re.I | re.M)
        price = pattern_price.findall(raw_line_items)

        pattern_description = re.compile(
            pattern_description, re.I | re.S | re.M)
        description = pattern_quantity.split(raw_line_items)

        filter_desc = list(
            filter(lambda item: 'QUANTITY' not in item, description))

        if quantity:
            for index in range(min(len(quantity), len(price), len(filter_desc))):
                product = {}
                product['quantity'] = quantity[index].strip()
                product['price'] = price[index].strip()
                product['description'] = filter_desc[index]

                line_items.append(product)
        elif price:
            for index, item in enumerate(price):
                product = {}
                product['price'] = item.strip()
                try:
                    if len(filter_desc) - 1 <= index:
                        product['description'] = filter_desc[index]
                except IndexError:
                    pass
                line_items.append(product)

        print(f'the result:\n')
        print(line_items)
        return line_items
