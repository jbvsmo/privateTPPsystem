import random
import threading
import time
import controller

import config
from log import logger


class User(object):
    users = {}
    callback = lambda _: None
    _require_callback = False

    def __new__(cls, name, *args, **kwargs):
        user = super().__new__(cls)
        user._require_callback = True
        return user

    def __init__(self, name):
        self._name = None
        self.name = name

        if self._require_callback:
            self._require_callback = False
            User.callback(self.name)

    @classmethod
    def get(cls, name, *args, **kw):
        user = User.users.get(name)
        if user is not None:
            return user
        # noinspection PyCallingNonCallable
        return cls(name, *args, **kw)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.users[name] = self

    def __repr__(self):
        return '<User: {}>'.format(self.name)


class PersonUser(User):
    def __init__(self, name, ip):
        self.ip = ip
        if name is None:
            name = ip
        super().__init__(name)


class PCUser(User):
    deviation = 2

    def __init__(self, name, period, command):
        self.period = period
        self.command = command
        self.stop = False
        super().__init__(name)
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            if self.stop:
                return
            d = self.deviation
            t = self.period + random.random() * d - d / 2
            if t < 0:
                t = self.period
            time.sleep(t)
            cmd = random.choice(controller.cmds)
            logger.debug(type='bot', action='play', name=self.name,
                         content={'sleep': t, 'command': cmd})
            controller.controller_instance.send_command(
                (cmd, controller.CommandType.button_press), user=self.name
            )

            if not config.hold_click:
                # Send button release if the "Click Buttons" feature is disabled
                controller.controller_instance.send_command(
                    (cmd, controller.CommandType.button_release), user=self.name
                )

