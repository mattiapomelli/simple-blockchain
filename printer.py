class Printer:
    @staticmethod
    def colored(r, g, b, text):
        return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

    @staticmethod
    def error(text):
        colored_text = Printer.colored(227, 67, 27, text)
        print(colored_text)

    @staticmethod
    def success(text):
        colored_text = Printer.colored(49, 235, 102, text)
        print(colored_text)

    @staticmethod
    def info(text):
        colored_text = Printer.colored(245, 245, 66, text)
        print(colored_text)
