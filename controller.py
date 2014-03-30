import random
import threading
import queue
import socket
import time
import collections
import config


_base_button = b'\x00\x03'
_base_press = b'a'
_base_release = b'b'

original_map = {
    # Button pressed
    b'65': 'a',
    b'66': 'b',
    b'10': 'start',
    b'32': 'select',
    b'37': 'left',
    b'38': 'up',
    b'39': 'right',
    b'40': 'down',
}

button_hold = {
    'a': b'65',
    'b': b'66',
    'start': b'67',
    'select': b'68',
    'left': b'69',
    'up': b'70',
    'right': b'71',
    'down': b'72',
}

cmds = list(button_hold)
maxlen_cmd = max(len(i) for i in cmds)

button_hold_chr = {
    k: b'c' + chr(int(v)).lower().encode('ascii')
    for k, v in button_hold.items()
}


def find_command(val):
    if not val.startswith(_base_button):
        return None

    val = val[len(_base_button):]
    st = val[:1]
    val = original_map.get(val[1:3])
    if val is None:
        return None

    return val, st


class Controller(object):
    ADDR = '127.0.0.1'
    PORT = 8589

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
        self._start_send_thread(c)

    def _raffle(self):
        lst = []
        cnt = self._grab(config.raffle_time)
        if not cnt:
            return
        print(cnt.most_common())
        for k, x in cnt.items():
            lst += [k] * x
        c = random.choice(lst)
        self.grab_callback(None, c)
        self._start_send_thread(c)

    def run_queue(self):
        while True:
            self.modes[config.selected]()

    def send_command(self, cmd, correct_cmd=False, user=''):
        if not config.enabled:
            return

        if not correct_cmd:
            cmd = find_command(cmd)
        if cmd is None:
            return

        cmd, st = cmd
        if config.hold_click:
            if st != _base_press:
                return  # Do not send at command end
            #self.send_click(cmd)
            with self.cmds_lock:
                self.commands.put((cmd, user))
        else:
            self.send_click(cmd, st)

    def send_click(self, cmd, st=None):
        sst = _base_press if st is None else st

        if config.delay:
            time.sleep(config.delay)
        self.send_message(_base_button + sst + button_hold[cmd])
        if st is not None:
            return

        time.sleep(config.click_duration)
        self.send_message(_base_button + _base_release + button_hold[cmd])

    def send_message(self, msg):
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
        cmd = button_hold_chr[cmd]
        if self.udp is None:
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.sendto(cmd, (self.ADDR, self.PORT))


controller = Controller()
