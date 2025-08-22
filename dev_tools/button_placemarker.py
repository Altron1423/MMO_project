import pygame as pg
pg.init()
import graphics.battons as battons
import json



class Main:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.TPS = 20
        self.tick = 0

        self.screenSize = self.WIDTH, self.HEIGHT = 800, 900
        self.centr = self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.K_Mushtub = 1
        self.centrovka = True
        self.screenOSN = pg.display.set_mode(self.screenSize, pg.RESIZABLE)
        self.screen = pg.Surface(self.screenSize)
        self.mousePos = (-1, -1)


        self.bat = None
        self.mouseStart = (0, 0)
        self.start_data = (0, 0)
        self.mode_of_change = 0


        self.WORK = True
        self.style = battons.ColorT((125, 125, 125))
        self.style.append("buttonFonAc", {"rgb": (100, 100, 100)})
        self.styleM = battons.ColorT((255, 0, 0))
        self.styleM.append("buttonFonAc", {"rgb": (100, 100, 100)})
        # self.menu = battons.Menu()
        # self.menu.append_option("qwerty", lambda x: print(123), [100, 100, 50, 50], self.style)
        # self.menu.append_option("2", lambda x: game.detect_saves(), [175, 100, 50, 50], self.styles[0])

    def run(self):
        self.load()
        while self.WORK:
            self.screen.fill((200, 200, 200))
            self.screenOSN.fill((0, 0, 0))
            # print(self.but)
            for event in pg.event.get():
                # print(event.type, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN)
                if event.type == pg.QUIT:
                    self.WORK = False
                elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                    self.menu.keyPress(event.key, event.type)
                elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    self.menu.select(but=event.button, up=event.type)
                elif event.type == pg.VIDEORESIZE:
                    self.screenSize = event.size
                    k1 = self.screenSize[0] / self.WIDTH
                    k2 = self.screenSize[1] / self.HEIGHT
                    if k1 < k2:
                        self.K_Mushtub = k1
                        self.centrovka = True
                    else:
                        self.K_Mushtub = k2
                        self.centrovka = False

            # self.window_manager.draw()
            self.menu.draw(self.screen, self.mousePos)


            if self.bat != None:
                move = [self.mousePos[0] - self.mouseStart[0], self.mousePos[1] - self.mouseStart[1]]
                if self.mode_of_change == 0:
                    pos = [
                        self.key_batton[self.bat][3][0] + move[0],
                        self.key_batton[self.bat][3][1] + move[1],
                        self.key_batton[self.bat][3][2],
                        self.key_batton[self.bat][3][3]
                    ]
                elif self.mode_of_change == 1:
                    pos = [
                        self.key_batton[self.bat][3][0],
                        self.key_batton[self.bat][3][1],
                        max(self.key_batton[self.bat][3][2] + move[0], 0),
                        max(self.key_batton[self.bat][3][3] + move[1], 0)
                    ]
                self.key_batton[self.bat][0].moweButton(pos)
                self.key_batton[self.bat][1].moweButton([pos[0]-10, pos[1]-10, 20, 20])
                self.key_batton[self.bat][2].moweButton([pos[0]-10+pos[2],
                                                         pos[1]-10+pos[3], 20, 20])




            if self.centrovka:
                dx = 0
                dy = (self.screenSize[1] - self.HEIGHT * self.K_Mushtub) // 2
            else:
                dx = (self.screenSize[0] - self.WIDTH * self.K_Mushtub) // 2
                dy = 0

            self.mousePos2 = ((self.mousePos[0] - dx) // self.K_Mushtub, (self.mousePos[1] - dy) // self.K_Mushtub)
            screen2 = pg.transform.scale(self.screen, (self.WIDTH * self.K_Mushtub, self.HEIGHT * self.K_Mushtub))
            self.screenOSN.blit(screen2, (dx, dy))
            if pg.mouse.get_focused():
                self.mousePos = pg.mouse.get_pos()
            else:
                self.mousePos = (-1, -1)

            pg.display.update()

    def save(self, bat):
        for i in range(len(self.buttons_config[self.window])):
            self.buttons_config[self.window][i][3] = self.key_batton[i][3]
        print(self.buttons_config)
        # pass

    def load(self):
        self.but = None
        self.menu = battons.Menu()
        self.path = input("Enter the path: ")
        self.count_batton = 0
        self.key_batton = {}
        with open(self.path, "r", encoding="utf-8") as f:
            self.buttons_config = json.load(f)
        print("Select Window:\n  ", end="")
        print(*self.buttons_config.keys(), sep="\n  ")
        self.window = input()
        while self.window not in self.buttons_config.keys():
            self.window = input("Incorrect enter again")

        self.generate_buttons(self.buttons_config[self.window])

        self.menu.append_option("save", self.save, [35, 35, 50, 50], self.style)

    def set_but(self, bat):
        self.bat = int(bat.description.split(":")[0])
        self.mode_of_change = int(bat.description.split(":")[1])
        # if self.mode_of_change == 0:
        #     self.start_data = (0, 0)
        self.mouseStart = self.mousePos

    def reset_but(self, bat):
        self.key_batton[self.bat][3] = self.key_batton[self.bat][0].buttonCord
        self.bat = None

    def generate_buttons(self, data):
        for button in data:
            self.key_batton[self.count_batton] = [self.menu.append_option(button[1], lambda x: 0, button[3], self.style)]
            self.key_batton[self.count_batton].append(self.menu.append_option("", self.reset_but,
                                                                              [button[3][0]-10, button[3][1]-10, 20, 20],
                                                                              self.styleM, descr=f"{self.count_batton}:0"))
            self.key_batton[self.count_batton].append(self.menu.append_option("", self.reset_but,
                                                                              [button[3][0]+button[3][2]-10,
                                                                               button[3][1]+button[3][3]-10,
                                                                               20, 20], self.styleM, descr=f"{self.count_batton}:1"))
            self.key_batton[self.count_batton][1].addDef(self.set_but, 0)
            self.key_batton[self.count_batton][2].addDef(self.set_but, 0)
            self.key_batton[self.count_batton].append(button[3])
            self.count_batton += 1



if __name__ == "__main__":
    main = Main()
    main.run()
