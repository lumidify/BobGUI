class Flow():
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.widgets = []
        self.lines = []
    def resize(self, screen_size):
        self.screen_size = screen_size
    def add(self, widget, **kwargs):
        if kwargs.get("newline", False):
            self.lines.append([widget])
