class Veslac:
    def __init__(self, oib, ime, grod, vr = 0):
        if len(str(oib)) != 11:
            raise TypeError("OIB must be length of 11")
        self.oib = oib
        self.ime = ime
        self.grod = grod
        self.vr = round(vr, 2)
    

    def __str__(self):
        return f"{self.ime}, {self.oib}, rođen {self.grod} i vrijeme {self.vr}"
    
    def promijenivrijeme(self, vrijeme):
        if vrijeme < self.vr:
            self.vr = round(vrijeme, 2)

    def __lt__ (self, other):
        return self.vr < other.vr
    
    def __gt__ (self, other):
        return self.vr > other.vr
    
    def __le__ (self, other):
        return self.vr <= other.vr
    
    def __ge__ (self, other):
        return self.vr >= other.vr
    
    def __eq__ (self, other):
        return self.vr == other.vr
    
    
    def __ne__ (self, other):
        return self.vr!= other.vr