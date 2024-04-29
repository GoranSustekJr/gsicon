class Veslac:
    def __init__(self, oib, ime, grod, vr = 0):
        if len(str(oib)) != 11 or type(oib) != int:
            return TypeError
        self.oib = oib
        self.ime = ime
        self.grod = grod
        self.vr = vr

    def __str__(self):
        return self.oib, self.ime, self.grod, self.vr