import os
import json
import pygame
# from pygame import image, transform, init

pygame.init()
class ModLoad():
    def __init__(self, core):
        self.core = core
        self.paths = [f"{os.getcwd()}/{self.core['mod_pack']}/{self.core['behaviorPack']}",
                       f"{os.getcwd()}/{self.core['mod_pack']}/{self.core['resourcesPack']}"]
        self.mods = {}
        self.mobs = {}
        self.languages = {}
        self.fonMaineMenu = []
        self.language = None
        self.mobTs = {"standart:defalt": pygame.transform.scale(pygame.image.load(f"{self.paths[1]}/Standart/textures/mobs/defalt.png").convert_alpha(), (70, 70))}
        for ipack in os.listdir(self.paths[0]):
            # try:
                mod = Mod(f"{self.paths[0]}/{ipack}", self.core)
                self.mods[0] = mod
                for i in mod.mobs:
                    self.mobs[i] = mod.mobs[i]
            # except:
            #     print(24, f"Error #modLoad reason: {self.paths[1]}/{ipack}}")
        for ipack in os.listdir(self.paths[1]):
            # try:
                mod = Mod(f"{self.paths[1]}/{ipack}", self.core)
                if mod != None:
                    self.mods[0] = mod
                    for i in mod.mobs:
                        self.mobs[i] = mod.mobs[i]
                    for i in mod.mobTs:
                        self.mobTs[i] = mod.mobTs[i]
                    for i in mod.languages:
                        if i in self.languages:
                            for j in mod.languages[i]:
                                self.languages[i][j] = mod.languages[i][j]
                        else:
                            self.languages[i] = mod.languages[i]
                    if mod.fonMaineMenu != None:
                        self.fonMaineMenu.append(mod.fonMaineMenu)
            # except:
            #     print(43, f"Error #modLoad reason: {self.paths[1]}/{ipack}}")

    def languages_text(self, text):
        if self.language == None:
            return text
        elif text in self.languages[self.language]:
            return self.languages[self.language][text]
        else:
            return text


    def getObjectElement(self, obj, element):
        if type(obj) == dict:
            return obj[element]
        elif type(obj) == str:
            # print(59)
            # for g in self.mobs: print(g, self.mobs[g])
            if obj not in self.mobs:
                return None
            elif element not in self.mobs[obj]:
                return None
            else:
                return self.mobs[obj][element]

class Mod():
    def __init__(self, path, core):

        self.path = path
        files = os.listdir(self.path)
        self.mobs = {}
        self.mobTs = {}

        if "manifest.txt" in files:
            t = open(f"{self.path}/manifest.txt", "r")
            manifest = json.loads(t.read().replace("\n", " "))
            t.close()
            for i in manifest:
                self.__dict__[i] = manifest[i]
            if manifest["name"] == "none":
                return None
            if manifest["type"] == "BP":
                if core["mod_mobs"] in files:
                    t = open(f"{self.path}/{core['mod_mobs']}/mobList.txt", "r")
                    mobl = json.loads(t.read().replace("\n", " "))
                    t.close()
                    for i in mobl["mobs"]:
                        # print(49, f"{self.path}/{core['mod_mobs']}/{i}.txt")
                        t = open(f"{self.path}/{core['mod_mobs']}/{mobl['mobs'][i]}.txt", "r")
                        mob = json.loads(t.read().replace("\n", " "))["data"]
                        t.close()
                        # print(mob)
                        self.mobs[mob["type"]] = mob
            elif manifest["type"] == "RP":
                self.languages = {}
                self.fonMaineMenu = None

                if core["mod_mobs"] in files:
                    # t = open(f"{self.path}/{core['mod_mobs']}/mobList.txt", "r")
                    # mobl = json.loads(t.read().replace("\n", " "))
                    # t.close()
                    mobTs = []
                    for i in os.listdir(f"{self.path}/{core['mod_mobs']}"):
                        # print(f"{self.path}/{core['mod_mobs']}/{i}.txt")
                        t = open(f"{self.path}/{core['mod_mobs']}/{i}", "r")
                        mobt = json.loads(t.read().replace("\n", " "))
                        t.close()
                        mobTs.append(mobt)
                if core["mod_textures"] in files:
                    t = open(f"{self.path}/{core['mod_textures']}/{core['mod_textures_file']}", "r")
                    moblt = json.loads(t.read().replace("\n", " "))
                    t.close()
                    for i in mobTs:
                        path_of_text = moblt["texture_data"][i["textures"]]
                        im = pygame.image.load(f"{self.path}/{core['mod_textures']}/{path_of_text['textures']}").convert_alpha()
                        im = pygame.transform.scale(im, path_of_text["size"])
                        # print(81, im)
                        self.mobTs[i["type"]] = im

                        # playerFon = pygame.image.load("textures/player0.png").convert_alpha()
                        # playerFon = pygame.transform.scale(playerFon, (70, 70))
                        # playerFonRect = playerFon.get_rect(center=center)
                    if core["fonMaineMenu"] in os.listdir(f"{self.path}/{core['mod_textures']}"):
                        self.fonMaineMenu = pygame.image.load(f"{self.path}/{core['mod_textures']}/{core['fonMaineMenu']}")
                if core["mod_languages"] in files:
                    t = open(f"{self.path}/{core['mod_languages']}/{core['mob_languages_file']}", "r")
                    textLs = json.loads(t.read().replace("\n", " "))
                    t.close()
                    for ilang in textLs:
                        print(116, f"{self.path}/{core['mod_languages']}/{textLs[ilang]}")
                        t = open(f"{self.path}/{core['mod_languages']}/{textLs[ilang]}", "r", encoding='utf-8')
                        lang = json.loads(t.read().replace("\n", " "))
                        t.close()
                        self.languages[ilang] = lang

            else:
                return None
        else:
            return None



# screenOSN = pygame.display.set_mode((100, 100), pygame.RESIZABLE)
# t = open(f"{os.getcwd()}/coreGameC.txt", "r")
# core = json.loads(t.read().replace("\n", " "))
# t.close()
#
# modLoad = ModLoad(core)
# modLoad.language = "RU_ru"
# print(modLoad.languages)
# print(modLoad.languages_text("standart:slime"), modLoad.languages_text("standart:error"))

# a = {
#     "texture_data": {
#         "zombies": {
#             "textures": "mobs/zombi0.png",
#             "size": (70, 70)
#         },
#         "people": {
#             "textures": "mobs/player0.png",
#             "size": (70, 70)
#         },
#         "ADM": {
#             "textures": "mobs/player0.png",
#             "size": (70, 70)
#         },
#         "slime": {
#             "textures": "mobs/slime0.png",
#             "size": (70, 70)
#         },
#         "magObgeckt": {
#             "textures": "mobs/magObj0.png",
#             "size": (40, 40)
#         }
#     }
# }


# {"standart:slime": "Слизь",
# "standart:people": "Слизь",
# "standart:zombies": "Слизь",
#
# "lvl": "Уровень",
# "name": "Имя",
# "rass": "Расса",
# "xp": "Опыт",
# "up_point": "Очки прокачки",
# "stats_inv": "Статы",
#
# "leave": "Жизни",
# "mana": "Мана",
# "pow": "Сила",
# "intel": "Интелект",
#
# "stam": "Ловкость",
# "dif": "Защита",
# "reg_leave": "Регенерация здоровья",
# "reg_mana": "Востонавление маны"
# }

a = {"standart:slime": "Слизь",
"standart:people": "Человек",
"standart:zombies": "Зомби",

"password": "Пароль",
"multiPlayer": "Сетевая игра",
"singlePlayer": "Одиночная игра",
"goExit": "Выйти",

"lvl": "Уровень",
"name": "Имя",
"rass": "Расса",
"xp": "Опыт",
"up_point": "Очки прокачки",
"stats_inv": "Статы",
"leave": "Жизни",
"mana": "Мана",
"pow": "Сила",
"intel": "Интелект",
"stam": "Ловкость",
"dif": "Защита",
"reg_leave": "Регенерация здоровья",
"reg_mana": "Востонавление маны"
}