class Widget():
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.screen = self.parent.screen
    def update_screen(self, screen):
        self.screen = screen
    def resize(self):
        pass
    def calculate_pos(self):
        pass
    def grid(self, **kwargs):
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.rowspan = kwargs.get("rowspan", 1)
        self.columnspan = kwargs.get("columnspan", 1)
        self.sticky = kwargs.get("sticky", "").lower()
        self.parent.add_widget(self, row=self.row, column=self.column, rowspan=self.rowspan, columnspan=self.columnspan)
    def flow(self, **kwargs):
        self.parent.add_widget(self, **kwargs)
    def place(self, **kwargs):
        self.parent.add_widget(self, **kwargs)
"""
    def resize(self, **kwargs):
        row_change = kwargs.get("row_change", 0)
        column_change = kwargs.get("column_change", 0)
        abs_width = kwargs.get("width", None)
        abs_height = kwargs.get("height", None)
        if abs_width is not None:
            self.boundwidth = abs_width
        if abs_height is not None:
            self.boundheight = abs_height
        self.boundwidth += column_change
        self.boundheight += row_change
        self.bounding_rect.width = self.boundwidth
        self.bounding_rect.height = self.boundheight
        self.calculate_pos()
    def move_bounds(self, **kwargs):
        row_change = kwargs.get("row_change", 0)
        column_change = kwargs.get("column_change", 0)
        abs_x = kwargs.get("x", None)
        abs_y = kwargs.get("y", None)
        if abs_x is not None:
            self.boundx = abs_x
        if abs_y is not None:
            self.boundy = abs_y
        self.boundx += column_change
        self.boundy += row_change
        self.bounding_rect.x = self.boundx
        self.bounding_rect.y = self.boundy
        self.calculate_pos()
    def calculate_pos(self):
        if self.sticky:
            if "n" in self.sticky and "s" in self.sticky:
                self.rect.height = self.bounding_rect.height
            if "e" in self.sticky and "w" in self.sticky:
                self.rect.width = self.bounding_rect.width
            if "n" in self.sticky:
                self.rect.top = self.bounding_rect.top
            if "s" in self.sticky:
                self.rect.bottom = self.bounding_rect.bottom
            if "e" in self.sticky:
                self.rect.left = self.bounding_rect.left
            if "w" in self.sticky:
                self.rect.right = self.bounding_rect.right
            if not "n" in self.sticky and not "s" in self.sticky:
                self.rect.centery = self.bounding_rect.centery
            if not "w" in self.sticky and not "e" in self.sticky:
                self.rect.centerx = self.bounding_rect.centerx
        else:
            self.rect.center = self.bounding_rect.center
        if self.rect.left < self.bounding_rect.left:
            self.rect.left = self.bounding_rect.left
        if self.rect.top < self.bounding_rect.top:
            self.rect.top = self.bounding_rect.top
"""

