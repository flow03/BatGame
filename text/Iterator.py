class BidirectionalIterator:
    def __init__(self, data : list):
        self.data = data
        self.index = 0

    def set_index(self, item):
        self.index = self.data.index(item)
        return self.data[self.index]

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


class ButtonsHandler:
    def __init__(self, buttons):
        self.buttons = buttons
        self.active_color = "Red"

        self.active = None
        self.key_pressed = False
        self.active_iterator()

    def active_iterator(self):
        if self.buttons:
            # if self.active:
            #     self.buttons[self.active].change_color("Black")
            self.active = BidirectionalIterator(list(self.buttons.keys()))
            self.buttons[self.active.current].change_color(self.active_color)
    
    def get_active(self):
        return self.active.current

    def set_active(self, key):
        if key != self.active.current:
            self.buttons[self.active.current].change_color("Black")
            self.active.set_index(key)
            self.buttons[self.active.current].change_color(self.active_color)

    def up(self):
        self.key_pressed = True
        self.buttons[self.active.current].change_color("Black")
        self.buttons[self.active.prev].change_color(self.active_color)

    def down(self):
        self.key_pressed = True
        self.buttons[self.active.current].change_color("Black")
        self.buttons[self.active.next].change_color(self.active_color)

    @property
    def pressed(self):
        return self.key_pressed
    # @property_name.getter призначений для зміни існуючого getter-а, 
    # раніше визначеного з допомогою @property 

    # @pressed.getter
    # def pressed(self, value : bool):
    #     self.key_pressed = value
