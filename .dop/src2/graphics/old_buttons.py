import time

import pygame as pg
import math

if __name__ == "__main__":
    pg.init()

ARIAL_25 = pg.font.SysFont('arial', 25)
KeysTransf = {
    pg.K_q: "q", pg.K_w: "w", pg.K_e: "e", pg.K_r: "r", pg.K_t: "t", pg.K_y: "y",
    pg.K_u: "u", pg.K_i: "i", pg.K_o: "o", pg.K_p: "p", pg.K_a: "a", pg.K_s: "s",
    pg.K_d: "d", pg.K_f: "f", pg.K_g: "g", pg.K_h: "h", pg.K_j: "j", pg.K_k: "k",
    pg.K_l: "l", pg.K_z: "z", pg.K_x: "x", pg.K_c: "c", pg.K_v: "v", pg.K_b: "b",
    pg.K_n: "n", pg.K_m: "m", pg.K_0: "0", pg.K_1: "1", pg.K_2: "2", pg.K_3: "3",
    pg.K_4: "4", pg.K_5: "5", pg.K_6: "6", pg.K_7: "7", pg.K_8: "8", pg.K_9: "9",
    pg.K_SPACE: " ", pg.K_COMMA: ",", pg.K_PERIOD: ".", pg.K_SLASH: "/", pg.K_MINUS: "-"
}

class ColorT:
    def __init__(self, col=False, r=None, g=None, b=None):
        self.countCol = 1
        self.dopCol = {"text": {"rgb": (255, 255, 255), "font": ARIAL_25}}
        if col == None:
            self.r = self.g = self.b = None
        elif col == False:
            self.r, self.g, self.b = r, g, b
        elif type(col) == tuple or type(col) == list:
            self.r, self.g, self.b = col
        elif isinstance(col, ColorT):
            self.r, self.g, self.b = col.r, col.g, col.b

    def append(self, name, dat):
        # self.countCol += 1
        if isinstance(dat, ColorT):
            self.dopCol[name] = {"rgb": (dat.r, dat.g, dat.b)}
        else:
            # dtk = dat.keys()
            # print(dtk)
            # if "rgb" in dtk or "textF" in dtk or "cord" in dtk or "size" in dtk:# or "font" in dtk:
            self.dopCol[name] = dat
        # print(self.__dict__)

    def dop(self, name):
        if name in self.dopCol.keys():
            return self.dopCol[name]
        else:
            return None


class Menu:
    class butClass():
        def __init__(self, option, callback, cord=(-1000, -1000, 10, 10), style=None, form="rect", zaj:bool=False, typeBut="but", descr:str=None, png=None, i=0, menu=None):
            self.menu = menu
            self.option_surfaces = style.dop("text")["font"].render(option, True, (255, 255, 255))
            self.text = option
            self.buttonCord = cord
            self.style = style
            # self.callbacks = callback
            # self.callbacks = [callback, None, None, None, None, None]
            self.callbacks = [None] * 10
            # print(__name__, __class__)
            # print(self.callbacks)
            self.callbacks[1] = callback
            # print(self.callbacks)

            self.form = form
            self.zaj = zaj
            self.type = typeBut
            if typeBut == "textInput":
                self.surface = blit_text(pg.Surface((cord[2], cord[3]), pg.SRCALPHA, 32), option, self.style.dop("text")["font"], color=pg.Color('black'))
            self.description = descr
            self.png = png
            if typeBut == "png" and png != None:
                # print(png, (cord[2], cord[3]))
                self.pngTr = pg.transform.scale(png, (cord[2], cord[3]))
                self.pngRect = png.get_rect(topleft=(cord[0], cord[1]))
            else:
                self.pngTr = None
                self.pngRect = None
            self.i = i
            self.shiftOn = False
            self.dinamX = False
            self.dinamY = False
            self.preCol = self.col_rend("buttonFon")

        def col_rend(self, type):
            # buttonFon = buttonFonAc = False

            color = None
            if self.style != None:
                if type == "buttonFonAc":
                    color = self.style.dop("buttonFonAc")["rgb"]

                if type == "buttonFon" or color == None:
                    if [self.style.r, self.style.g, self.style.b] != [None] * 3:
                        color = [self.style.r, self.style.g, self.style.b]

                if self.text != "":
                    txtFont = self.style.dop("text")
                    if txtFont != None:

                        if txtFont["font"] != None:
                            font = txtFont["font"]
                        else:
                            font = self.style.dop("font")

                        if txtFont["rgb"] != (None, None, None):
                            col = txtFont["rgb"]
                        else:
                            col = (255, 255, 255)

                        if self.type == "textInput":
                            self.surface = blit_text(pg.Surface((self.buttonCord[2], self.buttonCord[3]), pg.SRCALPHA, 32), self.text, font, color=col)
                        else:
                            self.option_surfaces = font.render(self.text, True, col)


            return color

            # print(208, buttonFonAc)
            # return buttonFon, buttonFonAc

        def draw(self, surf, mouseCord):
            ram = 60
            rec = surf.get_rect()
            option_rect = self.option_surfaces.get_rect()
            # cord = butt.buttonCord
            size = self.preRasm(rec)
            button_acktive_zero_tf = True
            if size == None:
                pass
            else:
                button = pg.Surface((size[2], size[3]))
                optionFon_rect = button.get_rect(topleft=(size[0], size[1]))
                if self.if_act(mouseCord, size):
                    col = self.col_rend("buttonFon")
                    button_acktive_zero_tf = False
                    self.menu._buttonAcktive = self.i
                else:
                    col = self.col_rend("buttonFonAc")
                drM = self.type == "mower"
                if drM:
                    if self.mvX != None:
                        if self.mvX.getFull()[1] <= 0:
                            drM = False
                    if self.mvY != None:
                        if self.mvY.getFull()[1] <= 0:
                            drM = False
                            col = None

                optSurf = self.option_surfaces
                if col != None:
                    if self.form == "rect":
                        pg.draw.rect(surf, col, optionFon_rect)
                        pg.draw.rect(surf, [max(0, g - ram) for g in col], optionFon_rect, 5)
                    elif self.form == "circle":
                        pg.draw.ellipse(surf, self.preCol[1], optionFon_rect)
                        pg.draw.ellipse(surf, [max(0, g - ram) for g in col], optionFon_rect, 5)
                if self.type == "png":
                    if self.png != None:
                        surf.blit(self.pngTr, self.pngRect)
                elif drM:
                    rect = [size[0], size[1], 0, 0]
                    col = (255, 255, 255)
                    width = None
                    if self.style != None:
                        n = self.style.dop("miniRect")
                        if n != None:
                            col = n["rgb"]
                            if "ram" in n.keys():
                                colRam = n["ram"]
                                width = n["width"]
                    if self.mvX != None:
                        vl, lm = self.mvX.getFull()
                        rect[0] += (size[2] - self.size[0]) * (vl / lm)
                        rect[2] = self.size[0]
                    else:
                        rect[2] = size[2]

                    if self.mvY != None:
                        vl, lm = self.mvY.getFull()
                        rect[1] += (size[3] - self.size[1]) * (vl / lm)
                        rect[3] = self.size[1]
                    else:
                        rect[3] = size[3]
                    self.miniRect = rect
                    pg.draw.rect(surf, col, rect)
                    if width != None:
                        pg.draw.rect(surf, colRam, rect, width)
                    # self.mwRect = rect
                    # print(size)

                elif self.type == "textInput":
                    # option_rect = self.buttonCord
                    optSurf = self.surface

                if self.textCord == None:
                    option_rect.center = optionFon_rect.center
                else:
                    option_rect = self.textCord
                # cordTxt = self.style.__dop("txtCord")
                # if cordTxt != None:
                #     print(cordTxt)
                #     cordTxt = cordTxt["cord"]
                #     option_rect = (cordTxt[0] + optionFon_rect[0], cordTxt[1] + optionFon_rect[1], 0, 0)
                #     # option_rect = cordTxt["cord"]
                # else:
                #     option_rect.center = optionFon_rect.center
                # option_rect = self.textCord
                # else:
                # stTxt
                # print(option_rect)
                surf.blit(optSurf, option_rect)
            return button_acktive_zero_tf, option_rect, size

        def if_act(self, mousePos, cord):
            # cord = self.buttonCord
            if self.callbacks == None:
                return False
            optionFon_rect = self.option_surfaces.get_rect()
            kordC = [cord[0] + cord[2] // 2 - mousePos[0], cord[1] + cord[3] // 2 - mousePos[1]]
            return (self.form == "rect" and 0 <= mousePos[0] - cord[0] <= cord[2] and
                    0 <= mousePos[1] - cord[1] <= cord[3]) or (self.form == "circle" and
                                                                kordC[0] ** 2 + kordC[1] ** 2 <= (cord[2] // 2) ** 2)

        def textInput(self, dat):
            if dat == "backspace":
                self.text = self.text[:-1]
            elif dat == "shift":
                self.shiftOn = not(self.shiftOn)
            else:
                if self.shiftOn:
                    self.text += dat.upper()
                else:
                    self.text += dat
            self.text = self.callbacks(self.text)
            self.surface = blit_text(pg.Surface((self.buttonCord[2], self.buttonCord[3]), pg.SRCALPHA, 32), self.text, self.style.dop("text")["font"], color=pg.Color('black'))
            # self.option_surfaces = ARIAL_50.render(self.text, True, (255, 255, 255))
            # if dat["text"] == None:
            #     if dat["deyst"] == "backspace":
            #         self.text = self.text[:-1]
            #         self.option_surfaces = ARIAL_50.render(self.text, True, (255, 255, 255))
            #     if dat["deyst"] == "shift":
            #         self.text = self.text[:-1]
            #         self.option_surfaces = ARIAL_50.render(self.text, True, (255, 255, 255))
            # else:
            #     self.text += dat["text"]
            #     self.option_surfaces = ARIAL_50.render(self.text, True, (255, 255, 255))

        def moweButton(self, cord):
            if len(cord) == 4:
                self.buttonCord = cord
            elif len(cord) == 2:
                self.buttonCord = cord + self.buttonCord[2:]

        def setPng(self, png):
            if png == None:
                self.png = None
                self.pngTr = None
                self.pngRect = None
            else:
                self.png = png
                self.pngTr = pg.transform.scale(png, (self.buttonCord[2], self.buttonCord[3]))
                self.pngRect = png.get_rect(topleft=(self.buttonCord[0], self.buttonCord[1]))

        def reText(self, text):
            self.text = text
            self.col_rend("buttonFon")
            # self.option_surfaces = ARIAL_50.render(, True, (255, 255, 255))

        def preRasm(self, rec):
            cord = self.buttonCord
            size = [
                rec[2] * cord[0] if 0 < cord[0] <= 1 else cord[0],
                rec[3] * cord[1] if 0 < cord[1] <= 1 else cord[1],
                rec[2] * cord[2] if 0 < cord[2] <= 1 else cord[2],
                rec[3] * cord[3] if 0 < cord[3] <= 1 else cord[3]
            ]
            if self.dinamX:
                size[0] -= self.menu.dinamX.value
            # print(f"<{self.description}>", self.dinamY, self.menu.dinamY.value)
            if self.dinamY:
                size[1] -= self.menu.dinamY.value
            self.sizeRect = size
            if self.style != None:
                n = self.style.dop("drawInREct")
                if n != None:
                    rct = n["rect"]
                    if not (
                        rct[0] <= size[0] <= rct[0] + rct[2] - size[2] and rct[1] <= size[1] <= rct[1] + rct[3] - size[3]
                    ):
                        size = None

                cordTxt = self.style.dop("txtCord")
                if cordTxt != None:
                    # st = st[cord]
                    # print(size)
                    sz = [
                        size[2] * cordTxt["cord"][0] if 0 < cordTxt["cord"][0] <= 1 else cordTxt["cord"][0],
                        size[3] * cordTxt["cord"][1] if 0 < cordTxt["cord"][1] <= 1 else cordTxt["cord"][1],
                        size[2] * cordTxt["size"][0] if 0 < cordTxt["size"][0] <= 1 else cordTxt["size"][0],
                        size[3] * cordTxt["size"][1] if 0 < cordTxt["size"][1] <= 1 else cordTxt["size"][1]
                    ]
                    sz[0] = size[0] + sz[0]
                    sz[1] = size[1] + sz[1]
                    # print(sz)
                    self.textCord = sz
                    # self.pngTr = pg.transform.scale(self.png, (sz[2], sz[3]))
                    # self.pngRect = self.png.get_rect(topleft=(size[0] + sz[0], size[1] + sz[1]))
                else:
                    self.textCord = None
                    # self.pngTr = pg.transform.scale(self.png, (size[2], size[3]))
                    # self.pngRect = self.png.get_rect(topleft=(size[0], size[1]))


            if self.type == "png":
                if self.png != None:
                    # self.styleT.append("pngCord", {"cord": (20, 20), "size": (40, 40)})
                    st = self.style.dop("pngCord")
                    # print(self.style.__dict__)
                    if st != None:
                        # st = st[cord]

                        sz = [
                            size[2] * st["cord"][0] if 0 < st["cord"][0] <= 1 else st["cord"][0],
                            size[3] * st["cord"][1] if 0 < st["cord"][1] <= 1 else st["cord"][1],
                            size[2] * st["size"][0] if 0 < st["size"][0] <= 1 else st["size"][0],
                            size[3] * st["size"][1] if 0 < st["size"][1] <= 1 else st["size"][1]
                        ]
                        # print(sz)
                        self.pngTr = pg.transform.scale(self.png, (sz[2], sz[3]))
                        self.pngRect = self.png.get_rect(topleft=(size[0] + sz[0], size[1] + sz[1]))
                    else:
                        self.pngTr = pg.transform.scale(self.png, (size[2], size[3]))
                        self.pngRect = self.png.get_rect(topleft=(size[0], size[1]))
            else:
                self.pngTr = None
                self.pngRect = None

            return size

        def select(self, but):
            # print(409, but, self.callbacks)
            if but == None:
                pass
            elif self.callbacks[but] != None:
                self.callbacks[but](self)
            else:
                # print(f"{but=} undefined")
                pass

        def set_dinam(self, dinX=False, dinY=False):
            self.dinamX = dinX
            self.dinamY = dinY
            return self

            """
            Сам починил до крутой цифры, сам же и сломаю хех. Гагася давайте уже игру, хочу сыграть про ктулхыча, ну и посмотреть игры на стриме кроме доты, сам дотер ломает дневной вайб после доты смотреть доту
            """

        def mower(self, size, dats={"moveX": None, "moveY": None}):
            self.type = "mower"
            self.size = size
            self.zaj = True
            # self.callbacks[0] = lambda x: print("WIP")
            # self.lastMP = None

            if "moveX" in dats.keys():
                self.mvX = dats["moveX"]
                self.callbacks[7] = lambda x: dats["moveX"].add(-0.05 * dats["moveX"].getFull()[1])
                self.callbacks[9] = lambda x: dats["moveX"].add(0.05 * dats["moveX"].getFull()[1])
            else:
                self.mvX = None
            if "moveY" in dats.keys():
                self.mvY = dats["moveY"]
                self.callbacks[7] = lambda x: dats["moveY"].add(-0.05 * dats["moveY"].getFull()[1])
                self.callbacks[9] = lambda x: dats["moveY"].add(0.05 * dats["moveY"].getFull()[1])
            else:
                self.mvY = None

            return self

        def addDef(self, callback, butt):
            if 0 <= butt < len(self.callbacks):
                if type(callback) == int:
                    self.callbacks[butt] = self.callbacks[callback]
                else:
                    self.callbacks[butt] = callback
            elif butt in KeysTransf:
                pass
            else:
                print(f"undefinde button {butt}")
                pass


    def __init__(self):
        self._buttons = []
        self.button_triggers = {}
        self._buttonAcktive = None
        self._current_option_index = 0
        self.naj = False
        self.najSens = False
        self.openText = None
        self.dinamX = Bars(0, 100, 0)
        self.dinamY = Bars(0, 1000, 0)
        self.mouseBut = None


    def setDinamLimit(self, din, lim):
        if din == "x":
            self.dinamX.setLimit(lim)
        elif din == "y":
            self.dinamY.setLimit(lim)


    def append_option(self, option, callback, cord=(-1000, -1000, 10, 10), style=None, form="rect", zaj:bool=False, tp="but", descr:str=None):
        self._buttons.append(self.butClass(option, callback, cord, style, form, zaj, tp, descr, i=len(self._buttons), menu=self))
        return self._buttons[-1]

        # self._option_surfaces.append(ARIAL_50.render(option, True, (255, 255, 255)))
        # self._buttonCord.append(cord)
        # self._buttonFon.append(color1)
        # self._buttonFonAc.append(color2)
        # self._callbacks.append(callback)


    def append_text(self, option, cord=(-1000, -1000, 10, 10), style=None, form="rect", descr:str=None):
        self._buttons.append(self.butClass(option, None, cord, style, form, False, "text", descr, i=len(self._buttons), menu=self))

        return self._buttons[-1]


    def append_png(self, option, callback, cord=(-1000, -1000, 10, 10), png=None, style=None, form="rect", zaj:bool=False, descr:str=None):
        # pg.image.load("test.png")
        # playerFon = pg.image.load("test.png").convert_alpha()
        if png != None:
            png = png.convert_alpha()
            size = png.get_size()
            # print(cord)
            if cord[2] != None and cord[3] != None:
                size = (cord[2], cord[3])
            elif cord[3] != None:
                size = (size[1] * cord[3] / size[0], cord[3])
                cord = (cord[0], cord[1], size[0], cord[3])
            elif cord[2] != None:
                size = (cord[2], size[0] * cord[3] / size[1])
                cord = (cord[0], cord[1], cord[2], size[1])
            cord = (cord[0], cord[1], size[0], size[1])
        # else:
        #     cord = (cord[0], cord[1], size[0], size[1])
        # png = pg.transform.scale(png, size)
        # pngRect = png.get_rect(topleft=(cord[0], cord[1]))
        # print(cord)
        # app.screen.blit(png, pngRect)
        self._buttons.append(self.butClass(option, callback, cord, style, False, False, form, zaj, "png", descr, png, i=len(self._buttons), menu=self))

        return self._buttons[-1]


    def get_button(self, ind=-1):
        return self._buttons(ind)


    def updateOption(self, i, option):
        self._buttons[i].option_surfaces = self.style.dop("text")["font"].render(option, True, (255, 255, 255))

    # def switch(self, direction):
    #     self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def deliteButton(self, idel):
        if type(idel) == int:
            self._buttons.pop(idel)
            for i in range(idel, len(self._buttons)):
                self._buttons[i].i = i
        elif type(idel) == list or type(idel) == tuple:
            ir = 0
            for i in idel:
                print(i)
                self.deliteButton(i-ir)
                ir += 1


    def select(self, but=1, up=None):
        if self.openText != None:
            self.openText = None
        if up != None:
            up -= pg.MOUSEBUTTONUP
        else:
            up = 0
        self.mouseBut = (but) * 2 + up - 1
        # print(self.mouseBut)
        if self.mouseBut > 9:
            self.mouseBut = None
        else:
            # print(self.mouseBut, self.mouseBut % 2 == 0)
            self.naj = self.mouseBut % 2 == 0


    def unselect(self):
        pass


    def keyPress(self, dat, type_press):
        if self.openText != None:
            if dat in KeysTransf.keys():
                self.openText.textInput(KeysTransf[dat])
            elif dat == pg.K_BACKSPACE:
                self.openText.textInput("backspace")
            elif dat == pg.K_RSHIFT or dat == pg.K_LSHIFT:
                self.openText.textInput("shift")
            elif dat == pg.K_RETURN:
                self.openText = None
                # self.openText.textInput("\n")
        else:
            print(dat, type_press)
            pass


    def butAct(self):
        return self._buttonAcktive


    def draw(self, surf, mousePos):
        button_acktive_zero_tf = True
        # ram = 60
        # rec = surf.get_rect()
        for i, butt in enumerate(self._buttons):

            BAZTF, option_rect, size = butt.draw(surf, mousePos)
            if BAZTF == False:
                button_acktive_zero_tf = False
            if size == None:
                pass
            elif butt.type == "textInput":
                surf.blit(butt.surface, butt.buttonCord)
            else:
                surf.blit(butt.option_surfaces, option_rect)
        if button_acktive_zero_tf:
            self._buttonAcktive = None
            butt = None
        else:
            butt = self._buttons[self._buttonAcktive]
        if self.naj != None:
            self.najSens = self.naj
        # if butt != None:
        #     print(f"   {self.najSens=}   {butt.zaj=}   {self.naj=}")
        if butt != None and (self.najSens or self.naj != None) and (butt.zaj or self.naj != None):
            # print()
            if butt.type == "but":
                butt.select(self.mouseBut)

            elif butt.type == "textInput":
                if self.openText == butt:
                    self.openText = None
                elif self.openText == None:
                    self.openText = butt
                else:
                    self.openText = butt

            elif butt.type == "png":
                butt.select(self.mouseBut)

            elif butt.type == "mower":
                butt.select(self.mouseBut)
                if self.mouseBut == 0:
                    if butt.mvX != None:
                        _, ml = butt.mvX.getFull()
                        if ml > 0:
                            butt.mvX.setValue((mousePos[0] - butt.sizeRect[0] - butt.miniRect[2] // 2) / (
                                        butt.sizeRect[2] - butt.miniRect[2]) * (ml) + butt.mvX.minL)
                    if butt.mvY != None:
                        _, ml = butt.mvY.getFull()
                        if ml > 0:
                            butt.mvY.setValue((mousePos[1] - butt.sizeRect[1] - butt.miniRect[3] // 2) / (
                                        butt.sizeRect[3] - butt.miniRect[3]) * (ml) + butt.mvY.minL)

        self.naj = None


    def normal(mouse, sdv):
        return (mouse[0] - sdv[0], mouse[1] - sdv[1])


class MiniMenu:
    def __init__(self):
        self.battons_menu = Menu()
        self.battons = []
        self.radius = 70
        self.bat_size = 40
        self.last_close = False
        self.buttonAcktive = False
        self.center = [-100, -100]
        c45 = math.acos(math.pi/4)
        self.bat_cord = [[0, -1], [c45, -c45], [1, 0], [c45, c45], [0, 1], [-c45, c45], [-1, 0], [-c45, -c45]]
        for i in range(8):
            self.bat_cord[i] = [self.radius * self.bat_cord[i][0], self.radius * self.bat_cord[i][1]]
        self.style = ColorT((125, 125, 125))
        self.style.append("buttonFonAc", {"rgb": (100, 100, 100)})
        # self.bat_cord = [[1, 0], [-c45, c45], [0, 1], [c45, c45], [1, 0], [-]]
        # self.bat_cord = [[-60, -60], [60, -60], [60, 60], [-60, 60]]

    def draw(self, surf, mousePos):
        if self.buttonAcktive or self.last_close:
            # print(12345634567)
            pg.draw.circle(surf, (60, 60, 60), self.center, self.radius)
            self.battons_menu.draw(surf, mousePos)
            if (self.center[0] - mousePos[0]) ** 2 + (self.center[1] - mousePos[1]) ** 2 >= (self.radius + 15) ** 2:
                self.close()
            if self.last_close:
                self.center = [-1000, -1000]
                for iBat in self.battons:
                    iBat.moweButton(self.center)
                self.last_close = False

    def add_options(self, option, callback):
        self.battons.append(self.battons_menu.append_option(option, lambda x: self.bat_select(callback, x), [-1000, -1000, self.bat_size, self.bat_size], self.style, form="rect", descr=None))

    def open(self, mouse_pos):
        self.buttonAcktive = True
        self.center = mouse_pos
        for i in range(len(self.battons)):
            self.battons[i].moweButton([
                self.center[0] + self.bat_cord[i][0] - self.bat_size//2,
                self.center[1] + self.bat_cord[i][1] - self.bat_size//2,
            ])

    def close(self):
        self.buttonAcktive = False
        self.last_close = True

    def mouse_clic(self, but, up):
        self.battons_menu.select(but, up)

    def bat_select(self, callback, bat):
        callback(bat)
        self.close()


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


def blit_text(surface, text, font, color=pg.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    max_width, max_height = max_width-10, max_height-10
    # x, y = pos
    x, y = [10, 10]
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                # x = pos[0]  # Reset the x.
                x = 10
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        # x = pos[0]  # Reset the x.
        x = 10
        y += word_height  # Start on new row.
    return surface





class Styler_test:
    def __init__(self):
        self.color = (255, 0, 0)
        self.color_select = (0, 255, 0)
        self.color_clicked = (0, 0, 255)
        self.color_off = (0, 0, 0)
        self.font_color = (255, 255, 255)

        self.font_name = 'Comic Sans MS'
        self.font_size = 30
        self.font = pg.font.SysFont(self.font_name, self.font_size)

    def set_color(self, param, color):
        """
        0: color
        1: color_select
        2: color_clicked
        3: color_off
        4: font_color
        :param param:
        :param color:
        :return:
        """
        if param == 0:
            self.color = color
        elif param == 1:
            self.color_select = color
        elif param == 2:
            self.color_clicked = color
        elif param == 3:
            self.color_off = color
        elif param == 4:
            self.font_color = color

    def set_font(self, name: str | None = None, size: int | None = None):
        if name is not None:
            self.font_name = name
        if size is not None:
            self.font_size = size
        if name is not None or size is not None:
            self.font = pg.font.SysFont(self.font_name, self.font_size)

    def text_render(self, text):
        if text:
            return self.font.render(text, True, self.font_color)
        return None

class TriggerGen_test:
    def __init__(self):
        self.triggers = {}
        self.last = None

    def LMD(self, function):
        self.triggers[(1, True)] = function
        return self

    def LMU(self, function):
        self.triggers[(1, False)] = function
        return self

    def RMD(self, function):
        self.triggers[(3, True)] = function
        return self

    def RMU(self, function):
        self.triggers[(3, False)] = function
        return self

    def MWD(self, function):
        self.triggers[(4, True)] = function
        return self

    def MWU(self, function):
        self.triggers[(5, False)] = function
        return self

    def HoldD(self, function):
        self.triggers[('hold', True)] = function
        return self

    def HoldU(self, function):
        self.triggers[('hold', False)] = function
        return self

    def key_down(self, key, function):
        self.triggers[(key, True)] = function
        return self

    def key_up(self, key, function):
        self.triggers[(key, False)] = function
        return self

    def __iadd__(self, other):
        if type(other) == dict:
            for k, f in other.items():
                self.triggers[k] = f
        elif isinstance(other, self.__class__):
            for k, f in other.triggers.items():
                self.triggers[k] = f
        return self

    def __getitem__(self, key):
        if key in self.triggers:
            self.last = key
            return self.triggers[key]
        return None

class ButtonManager_test:
    class Button:
        def __init__(self, manager, button_id):
            self.manager = manager
            self.id = button_id
            self.style: Styler_test = manager.baseStyle
            self.surface_size = None

            self.percent_use = [False, False, False, False]
            self.position = (-1000, -1000)
            self.size = (10, 10)
            self.percent_position = [-1.0, -1.0]
            self.percent_size = [1.0, 1.0]

            self.form = "rect"

            self.text = ""
            self.option_surfaces = None
            self.type = None
            self.triggers = None

            self.visible = True
            self.on = True
            self.hold = False
            self.holding = False
            self.active = False
            self.active_time = False
            self.active_delta = 0.1


        def _recalculation_positions(self):
            if self.surface_size:
                if self.percent_use[0]:
                    self.position[0] = int(self.surface_size[0] * self.percent_position[0])
                if self.percent_use[1]:
                    self.position[1] = int(self.surface_size[1] * self.percent_position[1])

        def _recalculation_size(self):
            if self.surface_size:
                if self.percent_use[2]:
                    self.size[0] = int(self.surface_size[0] * self.percent_size[0])
                if self.percent_use[3]:
                    self.size[1] = int(self.surface_size[1] * self.percent_size[1])

        def set_surface_size(self, surface_size):
            self.surface_size = surface_size
            self._recalculation_size()
            self._recalculation_positions()

        def set_percent_position(self, percent_position_x:float | None = None, percent_position_y:float | None = None):
            if percent_position_x:
                self.percent_position[0] = percent_position_x
                self.percent_use[0] = True
            if percent_position_y:
                self.percent_position[1] = percent_position_y
                self.percent_use[1] = True
            self._recalculation_positions()

        def set_percent_size(self, percent_size_x:float | None = None, percent_size_y:float | None = None):
            if percent_size_x:
                self.percent_size[0] = percent_size_x
                self.percent_use[2] = True
            if percent_size_y:
                self.percent_size[1] = percent_size_y
                self.percent_use[3] = True
            self._recalculation_size()


        def set_style(self, style:Styler_test):
            self.style = style

        def set_text(self, text:str):
            self.text = text
            self.option_surfaces = self.style.text_render(self.text)

        def set_type(self, type_but:str):
            self.type = type_but

        def set_triggers(self, triggers):
            self.triggers = triggers

        def set_holding(self, holding):
            self.holding = holding

        def move_to(self, position):
            self.position = position

        def move_on(self, d_position):
            position = (
                self.position[0] + d_position[0],
                self.position[1] + d_position[1]
            )
            self.move_to(position)

        def resize(self, new_size):
            self.size = new_size

        def test_active(self, mouse_position):
            active = False
            mouse_position_on_button = (
                mouse_position[0] - self.position[0],
                mouse_position[1] - self.position[1]
            )
            if self.on:
                if self.form == "rect":
                    active = (
                        0 <= mouse_position_on_button[0] <= self.size[0] and
                        0 <= mouse_position_on_button[1] <= self.size[1]
                    )
                elif self.form == "circle":
                    center_coordinate = [
                        mouse_position_on_button[0] + self.size[0] // 2,
                        mouse_position_on_button[1] + self.size[1] // 2
                    ]
                    active = center_coordinate[0] ** 2 + center_coordinate[1] ** 2 <= (self.size[0] // 2) ** 2

                if active and self.hold:
                    self.active = True
                    self.active_time = time.time() + self.active_delta
                    # if self.active_time - time.time() > self.active_delta:
                    #     self.active_time = time.time() + self.active_delta

            return active

        def select(self, trigger):
            if trigger[1] != self.hold:
                function = self.triggers[trigger]
                if function is not None:
                    function(self)
            self.hold = trigger[1]

        def un_hold(self):
            # function = self.triggers[('hold', False)]
            # if function is not None:
            #     function(self)
            self.hold = False

        def draw(self, surface, activ):
            if self.visible:
                if self.active:
                    color = self.style.color_clicked
                    if self.active_time <= time.time():
                        self.active = False
                elif activ:
                    color = self.style.color_select
                else:
                    color = self.style.color

                option_rect = (*self.position, *self.size)
                pg.draw.rect(surface, color, option_rect)

                optSurf = self.option_surfaces

                surface.blit(optSurf, option_rect)

            if self.on:
                if self.holding and self.hold and self.active:
                    function = self.triggers[('hold', True)]
                    if function is not None:
                        function(self)



    def __init__(self, mouse):
        self._buttons = []
        self.baseStyle = Styler_test()
        self.mouse = mouse
        self.last_style = None
        self.address = "main"
        self.surface = None
        self.active_button = None

    def set_surface(self, surface):
        self.surface = surface
        for button in self._buttons:
            button.set_surface_size(surface.get_size())

    def set_address(self, new_address):
        self.address = new_address

    def set_style(self, style:Styler_test):
        self.last_style = style

    def _create_button(self):
        button = self.Button(self, len(self._buttons))
        if self.last_style is not None:
            button.set_style(self.last_style)
        if self.surface is not None:
            button.set_surface_size(self.surface.get_size())
        self._buttons.append(
            button
        )
        return button

    def add_button(self, text, position, triggers):
        button = self._create_button()
        button.set_type("button")
        button.set_text(text)
        button.move_to(position[:2])
        button.resize(position[2:])
        button.set_triggers(triggers)
        return button

    def add_text(self, text, position):
        button = self._create_button()
        button.set_type("txt")
        button.set_text(text)
        button.move_to(position[:2])
        button.resize(position[2:])
        return button

    def add_png(self, text, position):
        button = self._create_button()
        button.set_type("png")
        button.set_text(text)
        button.move_to(position[:2])
        button.resize(position[2:])
        return button

    def add_png_but(self, text, position, triggers):
        button = self._create_button()
        button.set_type("png_but")
        button.set_text(text)
        button.move_to(position[:2])
        button.resize(position[2:])
        button.set_triggers(triggers)
        return button


    def get_button(self, index):
        if index is not None:
            return self._buttons[index]
        return None

    def select(self, event):
        but = event.button
        up = event.type == pg.MOUSEBUTTONDOWN
        button: ButtonManager_test.Button = self.get_button(self.active_button)
        if button is not None:
            button.select((but, up))

    def testing_activ(self, mouse_pos):
        last = None
        for i, butt in enumerate(self._buttons):
            if butt.test_active(mouse_pos):
                last = i
        return last


    def draw(self):
        if self.surface is not None:
            mouse_pos = self.mouse.get_position(self.address)
            self.active_button = self.testing_activ(mouse_pos)
            self.mouse.add_button(self.get_button(self.active_button))
            for i, butt in enumerate(self._buttons):
                butt.draw(self.surface, self.active_button==i)


if __name__ == "__main__":
    BM = ButtonManager_test()
    t = ButtonManager_test.TriggerGen_test().LMD(lambda: print("LMD"))
    t2 = ButtonManager_test.TriggerGen_test().LMU(lambda: print("LMU"))
    print(t.__dict__)
    print(t2.__dict__)
    # t3 = t + t2
    t += t2
    # print(t.__dict__)

    print(t[(0, True)])
    # t.__get__(12,345)
