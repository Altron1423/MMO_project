import graphics.battons as battons
import pygame as pg
import json

class MainScreen:
    def __init__(self, game):
        self.GAME = game
        self.screenSize = self.WIDTH, self.HEIGHT = 800, 900
        self.centr = self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.K_Mushtub = 1
        self.centrovka = True
        self.screenOSN = pg.display.set_mode(self.screenSize, pg.RESIZABLE)
        self.screen = pg.Surface(self.screenSize)
        self.menu = battons.Menu()
        self.window_manager = WindowManager(self)
        self.mousePos = (-1, -1)

    def draw(self):
        self.screen.fill((200, 200, 200))
        self.screenOSN.fill((0, 0, 0))
        for event in pg.event.get():
            # print(event.type, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN)
            if event.type == pg.QUIT:
                self.GAME.exit()
            elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                self.window_manager.keyPress(event.key, event.type)
                # self.menu.keyPress(event.key, event.type)
            elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                self.window_manager.select(event.button, event.type)
                # self.menu.select(but=event.button, up=event.type)
                # self.invman.select(but=event.button, up=event.type)
                # if self.shop.open:
                #     self.shop.menu[self.shop.selectMenu].select(but=event.button, up=event.type)
                # else:
                #     self.menu.select(but=event.button, up=event.type)
                #     if self.capsyls[self.selectCaps] != None:
                #         self.capsyls[self.selectCaps].menu.select(but=event.button, up=event.type)
                #         pass
            # elif event.type == pg.MOUSEBUTTONDOWN:
            #     # print(event.button)
            #     self.menu.select(but=event.button, up=event.type)
            #     if self.shop.open:
            #         self.shop.menu[self.shop.selectMenu].select()
            #     else:
            #         self.menu.select()
            #         if self.capsyls[self.selectCaps] != None:
            #             self.capsyls[self.selectCaps].menu.select()
            #     if event.button == 1:
            #         if self.shop.open:
            #             self.shop.menu[self.shop.selectMenu].select()
            #         else:
            #             self.menu.select()
            #             if self.capsyls[self.selectCaps] != None:
            #                 self.capsyls[self.selectCaps].menu.select()
            # elif event.type == pg.MOUSEBUTTONUP:
            #     self.menu.select(but=event.button, up=event.type)
            #     if event.button == 1:
            #         if self.shop.open:
            #             self.shop.menu[self.shop.selectMenu].unselect()
            #         else:
            #             self.menu.unselect()
            #             if self.capsyls[self.selectCaps] != None:
            #                 self.capsyls[self.selectCaps].menu.unselect()
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


        self.window_manager.draw()
        # self.menu.draw(self.screen, self.mousePos)


        if self.centrovka:
            dx = 0
            dy = (self.screenSize[1] - self.HEIGHT * self.K_Mushtub) // 2
        else:
            dx = (self.screenSize[0] - self.WIDTH * self.K_Mushtub) // 2
            dy = 0

        self.mousePos2 = ((self.mousePos[0] - dx) // self.K_Mushtub, (self.mousePos[1] - dy) // self.K_Mushtub)
        # for icaps in range(len(self.capsyls)):
        #     if self.capsyls[icaps] != None:
        #         self.capsyls[icaps].update()
        #         if self.capsyls[icaps].inProgres:
        #             col = (255, 255, 0)
        #         elif self.capsyls[icaps].inCompl:
        #             col = (0, 255, 0)
        #         else:
        #             col = (255, 0, 0)
        #         # if self.selectCaps == 10 - self.capsyls.count(None):
        #         #     print("+")
        #     else:
        #         col = (125, 125, 125)
        #     pg.draw.circle(self.screen, col,
        #                    (self.WIDTH * 1 / 3 + 50 * (icaps % 5), self.HEIGHT * 3.2 / 4 + 50 * (icaps // 5)), 20)
        # # print(self.capsyls[self.selectCaps], self.selectCaps)
        # if self.capsyls[self.selectCaps] != None:
        #     self.capsyls[self.selectCaps].draw(self.screen)
        #     pass
        # self.invman.draw(self.screen, self.mousePos2)

        # pg.draw.circle(self.screen, (0, 0, 255),
        #                (self.WIDTH * 1 / 3 + 50 * (self.selectCaps % 5), self.HEIGHT * 3.2 / 4 + 50 * (self.selectCaps // 5)),
        #                10)
        # for i in range(len(self.hrlabs)):
        #     lab = self.hrlabs[i]
        #     if lab == None:
        #         break
        #     lab.update()

        # if self.shop.open:
        #     self.shop.draw(self.screen)
        # else:
        #     self.menu.draw(self.screen, self.mousePos2)

        # screen2 = pg.transform.scale(screenDop, (250, radRadar))
        # pg.draw.circle(screenDop, (0, 255, 0), (80, 80), 30)
        # screenDop.set_alpha(100)
        # pg.draw.circle(screenDop, (0, 255, 0), (150, 80), 30)
        # screen.blit(screenDop, (350, 450))

        # pg.draw.rect(screen, (83, 83, 83), (0, 0, WIDTH_WD, HEIGHT_WD), 5)

        screen2 = pg.transform.scale(self.screen, (self.WIDTH * self.K_Mushtub, self.HEIGHT * self.K_Mushtub))
        self.screenOSN.blit(screen2, (dx, dy))
        if pg.mouse.get_focused():
            self.mousePos = pg.mouse.get_pos()
        else:
            self.mousePos = (-1, -1)

        pg.display.update()


class WindowManager:
    def __init__(self, main_screen):
        self.main_screen = main_screen
        self.styles = [battons.ColorT((200, 200, 200))]
        self.styles[0].append("buttonFonAc", {"rgb": (100, 100, 100)})
        self.windows = []
        self.windows_keys = {}
        self.load_windows()
        self.mainWindow = self.windows[0]

    def load_windows(self):
        with open(r"data\buttons_config.json", "r", encoding="utf-8") as f:
            buttons_config = json.load(f)
        for window in buttons_config:
            self.windows.append(Window(self, window, buttons_config[window]))
            self.windows_keys[window] = len(self.windows) - 1

    def draw(self):
        self.mainWindow.menu.draw(self.main_screen.screen, self.main_screen.mousePos)

    def keyPress(self, key, type):
        self.mainWindow.menu.keyPress(key, type)
        pass

    def select(self, button, type):
        self.mainWindow.menu.select(button, type)
        pass

    def genegate_function(self, data):
        data = data.split(":")
        if data[0] == "move_window":
            return lambda x: self.set_main_window(data[1])

    def set_main_window(self, window):
        # print(window)
        self.mainWindow = self.windows[self.windows_keys[window]]


class Window:
    def __init__(self, manager:WindowManager, name, config):
        self.manager = manager
        self.name = name
        self.mowing = False
        self.menu = battons.Menu()
        self.menu_load(config)

    def menu_load(self, config):
        # game = self.manager.game
        # print(config)
        for i_button in config:
            if i_button[0] == "button":
                # print("  ", i_button, i_button[2])
                f = self.manager.genegate_function(i_button[2])
                self.menu.append_option(i_button[1], f, i_button[3], self.manager.styles[i_button[4]])

