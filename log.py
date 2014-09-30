import threading
import time
import datetime
import queue
import json

import config


class LogLevel:
    debug = 0
    info = 1
    error = 2

    _vdic = None
    _ndic = None

    @classmethod
    def names(cls):
        if cls._ndic is None:
            cls._ndic = {
                k: v for k, v in cls.__dict__.items()
                if isinstance(v, int)
            }
        return cls._ndic

    @classmethod
    def name(cls, val):
        if cls._vdic is None:
            cls._vdic = {v: k for k, v in cls.names().items()}
        return cls._vdic[val]


class Loggable:
    def __init__(self, content, level, show):
        self.timestamp = time.time()
        self.content = content
        self.type = content.pop('type', '')
        self.show = show
        self.level = getattr(LogLevel, level)

    @property
    def level_name(self):
        return LogLevel.name(self.level)

    def __repr__(self):
        timestamp = datetime.datetime.fromtimestamp(self.timestamp)
        try:
            data = json.dumps(self.content)
        except Exception:
            data = repr(self.content)
        return ','.join([
            str(timestamp),
            self.level_name,
            self.type,
            self.content.get('action', ''),
            json.dumps(data)
        ])

    def __str__(self):
        content = self.content.copy()
        return '[{}] '.format(self.level_name) + \
               self.type.capitalize() + ': ' +  \
               ', '.join(x.capitalize().replace('_', ' ')
                         if isinstance(x, str) else str(x)
                         for x in content.values())


class MetaLogger(type):
    def __init__(cls, *args):
        super().__init__(*args)

        def maker(name):
            def loglevel(self, *args, **kw):
                return self.log(name, *args, **kw)
            return loglevel

        for name in LogLevel.names():
            setattr(cls, name, maker(name))


class Logger(threading.Thread, metaclass=MetaLogger):
    def __init__(self, file, open_mode):
        super().__init__(daemon=False)
        self._run = True
        self.file_name = file
        self.file = None
        self.open_mode = open_mode
        self.queue = queue.Queue()
        self.level = LogLevel.debug

    def print_level(self, level=None):
        if level is not None:
            if isinstance(level, int):
                self.level = level
            else:
                self.level = getattr(LogLevel, level)
        else:
            return level

    def log(self, level='info', show=True, **kw):
        self.queue.put(Loggable(kw, level, show))

    def run(self):
        with open(self.file_name, self.open_mode) as self.file:
            self.write_log()

    def write_log(self):
        while True:
            obj = self.queue.get()
            if obj is None or not self._run:
                break
            self.file.write(repr(obj) + '\n')
            if obj.show and obj.level > self.level:
                print(obj)

    def stop(self):
        self._run = False
        self.queue.put(None)

logger = Logger(config.local_file(config.g('log', 'file')),
                config.g('log', 'open_mode'))
logger.start()