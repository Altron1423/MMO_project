class Bars:
    TFupdate = True

    """
    triggers = {"minL": None, "zero": None, "aZero": None, "limit": None, "upValue": None, "downValue": None}
    """

    def __init__(self, value=1, limit=100, minL=0, triggers={}):
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.minL = minL
        self.triggers = triggers
        self.belowZero = False

    def triggerActiv(self, dat):
        if self.TFupdate:
            if dat < 0:
                if self.value <= self.minL:
                    self.value = self.minL
                    if self.value == 0 and "zero" in self.triggers.keys():
                        self.triggers["zero"]()
                    if "minL" in self.triggers.keys():
                        self.triggers["minL"]()
                elif self.value <= 0 and self.belowZero == False:
                    self.belowZero = True
                    if "zero" in self.triggers.keys():
                        self.triggers["zero"]()
                if "downValue" in self.triggers.keys():
                    self.triggers["downValue"]()

            elif dat > 0:
                if self.value >= self.limit:
                    self.value = self.limit
                    if "limit" in self.triggers.keys():
                        self.triggers["limit"]()
                elif self.value >= 0 and self.belowZero:
                    self.belowZero = False
                    if "aZero" in self.triggers.keys():
                        self.triggers["aZero"]()
                if "upValue" in self.triggers.keys():
                    self.triggers["upValue"]()
        # print("   ", self.value, self.minL, self.value <= self.minL)

    def update(self, value=0, limit=100):
        before = self.value
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.triggerActiv(self.value - before)

    def getFull(self, fromZero=False):
        if fromZero:
            return self.value, self.limit
        else:
            return self.value - self.minL, self.limit - self.minL

    def add(self, dat):
        dat = int(dat)
        self.value += dat
        self.triggerActiv(dat)

    def setValue(self, dat):
        dat = int(dat)
        olV = self.value
        self.value = dat
        self.triggerActiv(self.value - olV)

    def addLimit(self, dat):
        self.limit += dat
        self.triggerActiv(dat)

    def setLimit(self, dat):
        self.limit = dat
        self.triggerActiv(dat)

    def addMinLimit(self, dat):
        self.minL += dat
        self.triggerActiv(dat)

    def setMinLimit(self, dat):
        self.minL = dat
        self.triggerActiv(dat)

    def __str__(self):
        return f"{self.value}/{self.limit}"
