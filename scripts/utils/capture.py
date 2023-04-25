import re


class Capture():
    PATTERN_BILL = re.compile(r".*\b(SPECIAL NOTICE)\b|^\b.*FORUM\b", flags=re.M);
    ID_VENDOR = re.compile(r'(\bFORUM\b)?.*?\bCOMPANY\b', flags=re.M|re.S);
     
    def __init__(self, raw_text:str, pattern_bill = PATTERN_BILL, identifier_bill = ID_VENDOR):
        self.raw_text = raw_text.strip()
        self.pattern_bill = pattern_bill
        self.identifier_bill = identifier_bill
        self.__num_invoice = 0
     
    def structure_text(self, filter_pattern) -> list:
        """_summary_
        
        Args:
            filter_pattern: Future improvement to facilitate a modular method.
        Returns:
            list: The invoice list in which its data needs to be extracted.
        """
        invoice_list = self.pattern_bill.split(self.raw_text);
        def find_bill(elem) -> int:
            return elem and len(elem) > 100

        list_to_process = list(filter(find_bill, invoice_list))    
        print(list_to_process)
    
    def get_total_docs_process(self):
        finder = self.identifier_bill.findall(self.raw_text)
        if finder:
            self.__num_invoice = len(finder)
        return self.__num_invoice 
       
    def get_bill_to_address(self):
        pass
    
    def get_shipt_to_name(self):
        pass
    
    def get_ship_to_address(self):
        pass
    
    def get_line_item():
        pass