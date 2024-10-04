class BidirectionalIterator:
    # TODO прийматиме list з Buttons
    def __init__(self, data : list):
        self.data = data
        self.index = 0

    # TODO прийматиме Button
    def set_index(self, item):
        self.index = self.data.index(item)
        # return self.data[self.index]

    @property
    def current(self):
        return self.data[self.index]

    @property
    def next(self):
        if self.index < len(self.data) - 1:
            # result = self.data[self.index]
            self.index += 1
            # return result
        else:
            # raise StopIteration
            self.index = 0

        return self.data[self.index]
    
    @property
    def prev(self):
        if self.index > 0:
            # result = self.data[self.index]
            self.index -= 1
            # return result
        else:
            # raise StopIteration
            self.index = len(self.data) - 1

        return self.data[self.index]


class ActiveIterator:
    def __init__(self, buttons : dict):
        self.buttons = buttons
        self.active_color = "Red"
        self.iterator = BidirectionalIterator(list(self.buttons.keys()))
        self.buttons[self.iterator.current].change_color(self.active_color)
    
    def get_active(self):
        return self.iterator.current

    # TODO доведеться переробити, коли у buttons не буде ключів
    def set_active(self, key): # прийматиме Button
        if key != self.iterator.current:
            self.buttons[self.iterator.current].change_color("Black")
            self.iterator.set_index(key)
            self.buttons[self.iterator.current].change_color(self.active_color)

    def up(self):
        # self.key_pressed = True
        self.buttons[self.iterator.current].change_color("Black")
        self.buttons[self.iterator.prev].change_color(self.active_color)

    def down(self):
        # self.key_pressed = True
        self.buttons[self.iterator.current].change_color("Black")
        self.buttons[self.iterator.next].change_color(self.active_color)
