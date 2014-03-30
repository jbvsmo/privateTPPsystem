import os
import ast
import configparser

dir = os.path.dirname(__file__)
server_name = b'Private Twitch! By JB'
conf_file = os.path.join(dir, 'TwitchController.config')
enabled = True


#def enable(val):
#    global enabled
#    enabled = val


#------------------------------------------------------
# Config Parser
class EvalParser(configparser.ConfigParser):
    def gete(self, section, option):
        data = self.get(section, option)
        return ast.literal_eval(data)

parser = EvalParser()
parser.read(conf_file)

#------------------------------------------------------


def mode_idx(name):
    try:
        return modes.index(name.lower())
    except IndexError:
        return 0  # The First mode


def set_variable(name):
    def function(value):
        globals()[name] = value
    return function


g = parser.gete
modes = g('main', 'modes').split()
selected = g('main', 'selected')
hold_click = g('main', 'hold_click')
click_duration = g('main', 'click_duration')
delay = g('main', 'delay')
democracy_time = g('democracy', 'time')
raffle_time = g('raffle', 'time')
