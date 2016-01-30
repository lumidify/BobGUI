"""See class docstring"""
class TextWrap():
    """Splits a string into lines according to the max_width specified"""
    def __init__(self, text, max_width, font):
        """See description above"""
        self.text = text
        self.max_width = max_width
        self.font = font
        self.calculate_lines()
    def calculate_lines(self):
        """Calculates the lines"""
        self.lines = []
        temp_list = []
        temp_width = 0
        words = self.text.split()
        for word in words:
            if len(temp_list) == 0:
                space = ""
            else:
                space = " "
            word_width = self.font.size(space + word)[0]
            if word_width + temp_width > self.max_width:
                self.lines.append(" ".join(temp_list))
                temp_list = [word]
                temp_width = word_width
            else:
                temp_list.append(word)
                temp_width += word_width
        self.lines.append(" ".join(temp_list))
    def update_text(self, text):
        self.text = text
        self.calculate_lines()
    def update_width(self, max_width):
        """Lets you change the max_width"""
        self.max_width = max_width
        self.calculate_lines()
        