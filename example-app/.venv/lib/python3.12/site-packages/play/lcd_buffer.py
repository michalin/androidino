class Play:
    def __init__(self):
        self.rs = 0
        self.rw = 0
        self.E = 0
        self.Led = 1
        self.data = 72

    def GetLowData(self, e):
        buffer = self.rs
        buffer |= self.rw << 1
        buffer |= e << 2
        buffer |= self.Led << 3
        buffer |= (self.data & 0x0F) << 4

        print(buffer)

    def GetHighData(self, e):
        buffer = self.rs
        buffer |= self.rw << 1
        buffer |= e << 2
        buffer |= self.Led << 3
        buffer |= (self.data & 0x0F)

        print(buffer)


z = Play()
z.GetHighData(1)
z.GetHighData(0)

z.GetLowData(1)
z.GetLowData(0)
