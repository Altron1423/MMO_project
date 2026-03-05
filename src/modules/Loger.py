from json import load, dump
import pathlib
from datetime import date as Date, datetime
from inspect import currentframe, getframeinfo


def get_linenumber():
    cf = currentframe().f_back.f_back.f_back.f_back
    filename = getframeinfo(cf).filename
    return cf.f_lineno, filename

project_name = "MiGame"

class Loger:
    def __init__(self, consol_loging=True, file_loging=True, loging=True):
        self.path = pathlib.Path.cwd()

        self.off_log_file = [
            # r'\data\GameSession.py'
        ]
        self.log_text = f"Log file for {project_name}\n\n"

        self.consol_loging = consol_loging
        self.file_loging = file_loging
        self.len_string_number = 3
        self.len_log_locate = 15
        self.loging = loging

        if self.file_loging:
            self._load()

        self.status("Loger init complete")
        if self.off_log_file:
            self.status(f"Bunnet log from\n\t{'\n\t'.join(self.off_log_file)}")
        self.pass_line()

    def _load(self):
        with self.path.joinpath("data/configs/logs_config.json").open("r") as file:
            data = load(file)

        if data["last_date"] == str(Date.today()):
            data['count'] += 1
        else:
            data['last_date'] = str(Date.today())
            data['count'] = 1
        self.name = f"log_{Date.today().strftime('%Y_%m_%d')}_{data['count']}.txt"

        with self.path.joinpath("data/configs/logs_config.json").open("w") as file:
            dump(data, file)

        self.path = self.path.joinpath("logs").joinpath(self.name)
        with self.path.open(mode="w+", encoding="utf-8") as f:
            pass

        self.status(f"Create log file to {self.path}")

    def set_loging(self, loging:bool):
        self.consol_loging = loging

    def _log_generate(self, *args, tp, time:bool, data:bool, sep:str, end:str):
        if tp == 1:
            st_tp = "[L]"
        elif tp == 2:
            st_tp = "[S]"
        elif tp == 3:
            st_tp = "[E]"
        else:
            st_tp = f"[?{tp}]"

        log = f"{sep.join(map(str, args))}{end}"

        if time:
            log_time = f"{datetime.now()} | "
        else:
            log_time = ""

        if data:
            number_str, nf = get_linenumber()
            name_file = nf.split('src')[1]
            if name_file in self.off_log_file:
                return
            log_data = f"{number_str: >{self.len_string_number}}, {name_file: <{self.len_log_locate}} | "
        else:
            log_data = ""

        log = f"{st_tp} {log_time}{log_data}>> {log}"
        return log

    def _save_log(self, log):
        if self.file_loging:
            self.log_text += log
            with self.path.open(mode="w", encoding="utf-8") as f:
                f.write(self.log_text)

    def _log_data(self, *args, tp, time=True, data=True, sep=" ", end="\n"):
        log = self._log_generate(*args, tp=tp, time=time, data=data, sep=sep, end=end)

        if log is not None:
            if self.consol_loging:
                print(log, end="")

            self._save_log(log)

    def log(self, *args, time=True, data=True, sep=" ", end="\n"):
        if self.loging:
            self._log_data(*args, tp=1, time=time, data=data, sep=sep, end=end)

    def status(self, *args, time=True, data=False, sep=" ", end="\n"):
        self._log_data(*args, tp=2, time=time, data=data, sep=sep, end=end)

    def log_error(self, *args, time=True, data=False, sep=" ", end="\n"):
        self._log_data(*args, tp=3, time=time, data=data, sep=sep, end=end)

    def pass_line(self, n=1):
        log = "\n" * n
        print(log, end="")
        self._save_log(log)

loger = Loger(file_loging=False)



