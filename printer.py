from colorama import init, Fore, Style
init(convert=True)

class Printer:
    @staticmethod
    def error(text, end = '\n'):
        print(Fore.RED + text + Style.RESET_ALL, end = end)

    @staticmethod
    def success(text, end = '\n'):
        print(Fore.GREEN + text + Style.RESET_ALL, end = end)

    @staticmethod
    def info(text, end = '\n'):
        print(Fore.YELLOW + text + Style.RESET_ALL, end = end)
    
    @staticmethod
    def cyan(text, end = '\n'):
        print(Fore.CYAN + text + Style.RESET_ALL, end = end)
