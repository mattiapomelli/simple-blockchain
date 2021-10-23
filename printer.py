class Printer:
    @staticmethod
    def colored(r, g, b, text):
        return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

    @staticmethod
    def error(text):
        colored_text = Printer.colored(247, 64, 54, text)
        print(colored_text)

    @staticmethod
    def success(text):
        colored_text = Printer.colored(49, 235, 102, text)
        print(colored_text)

    @staticmethod
    def info(text):
        colored_text = Printer.colored(252, 250, 174, text)
        print(colored_text)
