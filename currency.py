import random

class Currency:

    def __init__(self):
        crypto_ex_rt = round(random.uniform(0,100), 2)
        self.crypto_ex_rt = crypto_ex_rt
        

    def __str__(self):
        return "current exchange rate: " + str(self.crypto_ex_rt) + " $ = 1 €"