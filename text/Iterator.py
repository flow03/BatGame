class BidirectionalIterator:
    def __init__(self, data : list):
        self.data = data
        self.index = 0

    def set_index(self, value):
        self.index = self.data.index(value)

    @property
    def current(self):
        return self.data[self.index]

    @property
    def next(self):
        if self.index < len(self.data) - 1:
            self.index += 1
        else:
            # raise StopIteration
            self.index = 0

        return self.data[self.index]
    
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
        self.active_color = "Red"
        self.iterator = BidirectionalIterator(list(self.buttons.values()))
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
