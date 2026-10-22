import traceback
import uuid
from datetime import datetime
from pathlib import Path


class LogLevel:
    DEBUG, INFO, WARN, ERROR, FATAL = "DEBUG", "INFO", "WARN", "ERROR", "FATAL"
    ORDER = (DEBUG, INFO, WARN, ERROR, FATAL)


class LogEntry:
    def __init__(self, level, message, source, user, extra=None):
        self.timestamp = datetime.now()                   # дата и точное время события
        self.level = level                                          # уровень серьёзности
        self.source = source                                        # источник
        self.message = message                                      # сообщение о событии
        self.event_id = uuid.uuid4()                          # уникальный код события
        self.user = user                                            # пользователь / сессия
        self.extra = dict(extra or {})      # дополнительная информация

    def __str__(self):
        line = (f"[{self.timestamp:%Y-%m-%d %H:%M:%S.%f}] {self.level:<5} "
                f"id={self.event_id} src={self.source} "
                f"user={self.user} :: {self.message}")
        for key, value in self.extra.items():
            line += f"\n    {key}: " + str(value).replace("\n", "\n      ")
        return line


class LogManager:
    def __init__(self, path="Log.txt", user=None, min_level=LogLevel.DEBUG):
        self.path = Path(path)
        self.user = user or f"Session_{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}"
        self.min_level = min_level

    def log(self, level, message, source="App", exc=None, **extra):
        if LogLevel.ORDER.index(level) < LogLevel.ORDER.index(self.min_level):
            return None
        entry = LogEntry(level, message, source, self.user, extra)
        if exc is not None:
            entry.extra["stack"] = "".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)).strip()
        with open(self.path, "a", encoding="utf-8") as logfile:
            logfile.write(str(entry) + "\n")
        return entry.event_id

    def debug(self, msg, source="App", **extra): return self.log(LogLevel.DEBUG, msg, source, **extra)
    def info(self, msg, source="App", **extra):  return self.log(LogLevel.INFO,  msg, source, **extra)
    def warn(self, msg, source="App", **extra):  return self.log(LogLevel.WARN,  msg, source, **extra)
    def error(self, msg, source="App", **extra): return self.log(LogLevel.ERROR, msg, source, **extra)
    def fatal(self, msg, source="App", **extra): return self.log(LogLevel.FATAL, msg, source, **extra)