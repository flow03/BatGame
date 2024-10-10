class BidirectionalIterator:
    def __init__(self, data : list):
        self.data = data
        self.index = 0

    # встановлює індекс на переданий елемент
    def set_index(self, value):
        if value in self.data:
            self.index = self.data.index(value)

    # повертає поточний елемент
    @property
    def current(self):
        return self.data[self.index]

    # перемикає на наступний елемент і повертає цей елемент
    @property
    def next(self):
        if self.index < len(self.data) - 1:
            self.index += 1
        else:
            # raise StopIteration
            self.index = 0

        return self.data[self.index]
    
    # перемикає на попередній елемент і повертає цей елемент
    @property
    def prev(self):
        if self.index > 0:
            self.index -= 1
        else:
            # raise StopIteration
            self.index = len(self.data) - 1

        return self.data[self.index]


class ActiveIterator:
    def __init__(self, buttons : dict):
        self.buttons = buttons
        self.active_color = "white"
        self.iterator = BidirectionalIterator(list(self.buttons.values()))
        self.iterator.current.change_color(self.active_color)
    
    def change_color(self, color):
        self.active_color = color
        self.iterator.current.change_color(self.active_color)

    def get_active(self):
        return self.iterator.current

    def set_active(self, button):
        if button != self.iterator.current:
            self.iterator.current.change_color("Black")
            self.iterator.set_index(button)
            self.iterator.current.change_color(self.active_color)

    def up(self):
        self.iterator.current.change_color("Black")
        self.iterator.prev.change_color(self.active_color)

    def down(self):
        self.iterator.current.change_color("Black")
        self.iterator.next.change_color(self.active_color)
