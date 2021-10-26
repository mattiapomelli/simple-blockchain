import random

class Currency:
    """
    This class represents a currency. It simply stores the exchange rate
    between the currency and euros.
    """

    def __init__(self):
        """
        In this application, the exchange rate is determined randomly, and
        is a number between 5 and 100. 
        """
        crypto_ex_rt = round(random.uniform(5,100), 2)
        self.crypto_ex_rt = crypto_ex_rt  

    def __str__(self):
        return "Current exchange rate: " + str(self.crypto_ex_rt) + " $ = 1 €"