import asyncio
from pathlib import Path
from Loger import log, log_step
from googletrans import Translator as GTr
from time import sleep
# from translator import translator as TR



languages = {"RU_ru": "ru", "EN_en": "en"}

class Translator:
    dictionary: dict

    def __init__(self):
        self.dictionary = {}
        self.now_language = None
        self.now_dictionary = None
        self.AuTranslator = None

    @staticmethod
    def _get_struct_() -> dict[str: dict]:
        return {
            "sistem": Translator._get_module_struct_()
        }

    @staticmethod
    def _get_module_struct_() -> dict[str: dict]:
        return {
            "item": {},
            "block": {},
            "gui": {},
            "text": {}
        }

    @staticmethod
    def _to_dict_path(path:str):
        return path.split(".")

    @staticmethod
    def _set_translate(language_dictionary:dict, path: list, translate:str):
        if path[0] not in language_dictionary:
            language_dictionary[path[0]] = Translator._get_module_struct_()
        i = 0
        while i < len(path)-1:
            if path[i] not in language_dictionary:
                language_dictionary[path[i]] = {}
            language_dictionary = language_dictionary[path[i]]
            i += 1
        language_dictionary[path[i]] = translate

    def _get_translate(self, path: list) -> dict[str: bool, str]:
        i = 0
        dictionary = self.now_dictionary
        while i < len(path):
            if path[i] not in dictionary:
                return {"find": False, "text": path}
            dictionary = dictionary[path[i]]
            i += 1
        return {"find": True, "text": dictionary}

    def _add_dict(self, name: str, dictionary: dict):
        self.dictionary[name] = dictionary

    def _auto_translate_rec(self, dictionary:dict, language:str) -> dict:
        new_dictionary = {}
        for key, value in dictionary.items():
            if type(value) == dict:
                new_dictionary[key] = self._auto_translate_rec(value, language)
            else:
                new_dictionary[key] = self._web_translate(value, language)
        return new_dictionary

    def _web_translate(self, word, language):
        # print(word)
        try:#, src=languages[self.now_language]
            gtr = GTr()
            text = asyncio.run(gtr.translate(word, dest=languages[language])).text
            sleep(1)
            return text
        # except AttributeError as e:
        #     print(e)
        #     return self._web_translate(word, language)
        except Exception as e:
            print(e)
            return f"Error Tr3 {word}_{language}"

    def _to_properties_rec(self, dictionary):
        strings = []
        for key, value in dictionary.items():
            if type(value) == dict:
                elements = self._to_properties_rec(value)
                if elements:
                    strings += [
                        f"{key}.{ps}" for ps in elements
                    ]
            else:
                strings.append(f"{key} = {value}")
        return strings


    def load_from(self, path: Path, name_dict: str):
        dictionary = {}
        with path.open("r") as file:
            for line in file:
                line = line.strip().split("#")[0]
                if line:
                    if line.count("=") == 1:
                        key, value = [l.strip() for l in line.split("=")]
                        dictionary[key] = value
                    # print(line)
        self._add_dict(name_dict, dictionary)

    def set_language(self, language: str):
        self.now_language = language
        if language in self.dictionary:
            self.now_dictionary = self.dictionary[language]
        else:
            self.now_dictionary = None

    def load_language(self, path: Path, name_dict: str):
        language_dictionary = self._get_struct_()
        with path.open("r", encoding="utf8") as file:
            for line in file:
                line = line.strip().split("#")[0]
                if line:
                    if line.count("=") == 1:
                        key, value = [l.strip() for l in line.split("=")]
                        self._set_translate(language_dictionary, self._to_dict_path(key), value)
        self._add_dict(name_dict, language_dictionary)

    def translation(self, content: str, return_in:bool=True) -> str | None:
        if self.now_dictionary != None:
            translate = self._get_translate(self._to_dict_path(content))
            # if dict_name == None:
            #     for name, dictionary in self.dictionary.items():
            #         for key_word, translation in dictionary.items():
            #             if key_word == word:
            #                 return translation
            # else:
            #     for key_word, translation in self.dictionary[dict_name].items():
            #         if key_word == word:
            #             return translation
            if translate["find"]:
                return translate["text"]
        if return_in:
            return content
        return None

    def auto_translate_to(self, language: str):
        if language not in self.dictionary and self.now_language in languages and language in languages:
            log("Start auto translate")
            self.dictionary[language] = self._auto_translate_rec(self.now_dictionary, language)
            translator.save_language("EN_en", r"C:\Users\Altron\PycharmProjects\MMO_project\src\langs")

    def save_language(self, language, path):
        path = Path(path).joinpath(f"{language}.lang")
        with path.open("w+", encoding="utf8") as file:
            file.write("\n".join(self._to_properties_rec(self.dictionary[language])))

    def load_langs_directory(self, path: str):
        path = Path.cwd().joinpath(path)
        for i in path.iterdir():
            lang = i.name.split(".")[0]
            # lang = i.split("\\")[-1]
            self.load_language(
                Path.cwd().joinpath(i),
                lang
            )



if __name__ == "__main__":
    translator = Translator()


    translator.load_langs_directory(r"C:\Users\Altron\PycharmProjects\MMO_project\src\langs")
    log(translator.dictionary)
    translator.set_language("RU_ru")
    log(translator.translation("minecraft.item.lola"))
    log(translator.translation("sistem.item.lola"))
    log(translator.translation("sistem.item2.lola2"))

    log_step(2)

    translator.auto_translate_to("EN_en")
    translator.set_language("EN_en")
    log(translator.translation("minecraft.item.lola"))
    log(translator.translation("sistem.item.lola"))
    log(translator.translation("sistem.item2.lola2"))
