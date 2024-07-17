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
