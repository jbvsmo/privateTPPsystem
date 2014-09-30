import random
import threading
import queue
import socket
import time
import collections
import config
from log import logger

class CommandType(object):
    button_press = b'a'
    button_release = b'b'
    text = b'c'


# Byte sent to denote a new command
command_header = b'\x00'


# Button pressed on Max Remote
original_map = {
    b'65': 'a',
    b'66': 'b',
    b'10': 'start',
    b'32': 'select',
    b'37': 'left',
    b'38': 'up',
    b'39': 'right',
    b'40': 'down',
    b'76': 'l',
    b'82': 'r',
    b'88': 'x',
    b'89': 'y',
}

# Button to be sent to Max Remote Server by default
# The choice is A, B, C, ... because it is
# less harmful than the original with control characters
button_hold = collections.OrderedDict([
    ('a', b'65'),       # A
    ('b', b'66'),       # B
    ('start', b'67'),   # C
    ('select', b'68'),  # D
    ('left', b'69'),    # E
    ('up', b'70'),      # F
    ('right', b'71'),   # G
    ('down', b'72'),    # H
    ('l', b'76'),       # L
    ('r', b'82'),       # R
    ('x', b'88'),       # X
    ('y', b'89'),       # Y
])

button_text = {
    'left': '\u2190',
    'up': '\u2191',
    'right': '\u2192',
    'down': '\u2193',
}

cmds = list(button_hold)
maxlen_cmd = max(len(i) for i in cmds)


def find_command(val):
    st = val[:1]
    val = val[1:]
    if st == CommandType.text:
        return val.decode('utf-8'), st
    val = original_map.get(bytes(val))
    if val is None:
        return None

    return val, st


def build_command(st, val):
    data = st + val
    return command_header + bytes([len(data)]) + data


class Controller(object):
    ADDR = config.parser.gete('origin', 'addr')
    PORT = config.parser.gete('origin', 'port')
    cmd_callback = lambda *args: None
    grab_callback = lambda *args: None

    def __init__(self):
        self.lock = threading.Lock()
        self.commands = queue.Queue()
        self.cmds_lock = threading.Lock()
        self.conn = None
        self.udp = None
        self.modes = {
            'anarchy': self._anarchy,
            'democracy': self._democracy,
            'raffle': self._raffle,
        }
        threading.Thread(target=self.run_queue, daemon=True).start()

    def connect(self):
        self.conn = socket.socket()
        self.conn.connect((self.ADDR, self.PORT))

    def _queue_get(self, *args, **kw):
        cmd = self.commands.get(*args, **kw)
        self.cmd_callback(*cmd)
        return cmd[0]

    def _start_send_thread(self, c):
        threading.Thread(target=self.send_click, args=(c,), daemon=True).start()

    def _anarchy(self):
        c = self._queue_get()
        logger.debug(type='gameplay', action='anarchy', content=c)
        self._start_send_thread(c)

    def _grab(self, time_limit):
        cnt = collections.Counter()
        limit = time.time() + time_limit
        t = time.time()
        while t < limit:
            try:
                c = self._queue_get(timeout=limit - t)
            except queue.Empty:
                c = None
            if c is not None:
                cnt[c] += 1
                self.grab_callback(cnt, None)
            t = time.time()
        return cnt

    def _democracy(self):
        cnt = self._grab(config.democracy_time)
        if not cnt:
            return
        c = cnt.most_common(1)[0][0]
        self.grab_callback(None, c)
        logger.debug(type='gameplay', action='democracy', content=[c, cnt])
        self._start_send_thread(c)

    def _raffle(self):
        lst = []
        cnt = self._grab(config.raffle_time)
        if not cnt:
            return
        for k, x in cnt.items():
            lst += [k] * x
        c = random.choice(lst)
        self.grab_callback(None, c)
        logger.debug(type='gameplay', action='raffle', content=[c, cnt])
        self._start_send_thread(c)

    def run_queue(self):
        while True:
            self.modes[config.selected]()

    def send_command(self, cmd, user=''):
        if not config.enabled:
            return

        cmd, st = cmd
        if config.hold_click:
            if st != CommandType.button_press:
                return  # Do not send at command end
            with self.cmds_lock:
                self.commands.put((cmd, user))
        else:
            # TODO: This should be disabled at least on
            # Democracy/Raffle modes. It may break the game
            # with multiple people holding commands at the same time
            self.send_click(cmd, st)

    def send_click(self, cmd, st=None):
        sst = CommandType.button_press if st is None else st

        if config.delay:
            time.sleep(config.delay)
        self.send_message(build_command(sst, button_hold[cmd]))
        if st is not None:
            return

        time.sleep(config.click_duration)
        self.send_message(build_command(CommandType.button_release, button_hold[cmd]))

    def send_message(self, msg):
        """ Low level function to handle connections and send atual data to TCP socket.
        """
        if self.conn is None:
            self.connect()

        for _ in (0, 1):
            try:
                with self.lock:
                    self.conn.send(msg)
            except Exception as e:
                print(e)
                self.connect()
            else:
                break
        else:
            print('Command not sent...')

    def send_udp(self, cmd):
        cmd = b'c' + button_hold[cmd]
        if self.udp is None:
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.sendto(cmd, (self.ADDR, self.PORT))


controller_instance = Controller()