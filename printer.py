from colorama import init, Fore, Style
init(convert=True)

class Printer:
    @staticmethod
    def error(text, end = '\n'):
        print(Fore.LIGHTRED_EX + text + Style.RESET_ALL, end = end)

    @staticmethod
    def success(text, end = '\n'):
        print(Fore.LIGHTGREEN_EX + text + Style.RESET_ALL, end = end)

    @staticmethod
    def info(text, end = '\n'):
        print(Fore.LIGHTYELLOW_EX + text + Style.RESET_ALL, end = end)
    
    @staticmethod
    def cyan(text, end = '\n'):
        print(Fore.LIGHTCYAN_EX + text + Style.RESET_ALL, end = end)
    
    @staticmethod
    def get_info(text):
        return Fore.LIGHTYELLOW_EX + text + Style.RESET_ALL

    @staticmethod
    def get_cyan(text):
        return Fore.LIGHTCYAN_EX + text + Style.RESET_ALL
