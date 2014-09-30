#!/usr/bin/env python3
from collections import deque
import sys
from PyQt4 import QtGui, QtCore

import config
import form
import form_cmd
import form_buttons
import randomness
import server
import controller
import log
from user import User, PCUser, PersonUser


if 'win' in sys.platform:
    # Fix the task bar icon for Windows
    import ctypes
    ctypes.windll.shell32.\
        SetCurrentProcessExplicitAppUserModelID('com.privateTPPsystem')


class ClickLineEdit(QtGui.QLineEdit):
    key_dict = {v: k.split('_', 1)[-1] for k, v in
                QtCore.Qt.__dict__.items() if k.startswith('Key_')}

    def __init__(self, name, value, *args):
        super().__init__(*args)
        self.name = name
        self.key_value = None
        self.set_key(value)

    def set_key(self, value):
        self.setText(self.key_dict[value])
        self.key_value = value

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            try:
                self.set_key(event.key())
            except KeyError:
                pass
            return True

        return super().event(event)


def set_fossil(window):
    window.setWindowIcon(QtGui.QIcon('data/fossil.png'))


class Main(object):

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.window = QtGui.QMainWindow()
        self.cmd_window = QtGui.QMainWindow()
        set_fossil(self.window)
        set_fossil(self.cmd_window)

        self.btn_window = None
        self.widget_buttons = []

        self.ui = form.Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.uic = form_cmd.Ui_MainWindow()
        self.uic.setupUi(self.cmd_window)

        self.current_user = None
        self.cmd_text_anarchy = deque(maxlen=25)
        self.cmd_text_others = deque(maxlen=10)
        self.last_cmd = '[ ]'
        self.cmd_bubble = []

        self.fix_ui()
        self.load_config()
        self.create_slots()

        User.callback = self.insert_user
        controller.Controller.cmd_callback = self.write_data
        controller.Controller.grab_callback = self.write_bubble
        server.load()
        self.window.show()
        self.cmd_window.show()

    def fix_ui(self):
        table = self.ui.table_user
        table.setColumnWidth(0, 180)
        table.setColumnWidth(1, 75)
        self.uic.f_democracy.setShown(False)

    def load_config(self):
        self.ui.activate.setChecked(config.enabled)
        self.ui.box_hold_button.setChecked(config.hold_click)
        self.ui.time_button_hold.setValue(config.click_duration)
        self.ui.time_democracy.setValue(config.democracy_time)
        self.ui.time_raffle.setValue(config.raffle_time)
        self.ui.time_delay.setValue(config.delay)

        self.ui.connection.setText('Connected')

    def insert_user(self, name):
        self.ui.table_user.addTopLevelItem(QtGui.QTreeWidgetItem([name, '']))

    def write_bubble(self, cnt, c):
        if cnt is None:
            self.last_cmd = '[ {} ]'.format(c)

        text = self.last_cmd + '\n'
        if cnt is not None:
            for cmd, x in cnt.most_common(8):
                cmd += ' ' * (controller.maxlen_cmd - len(cmd)) + '  '
                text += cmd + '{: 3}'.format(x) + '\n'

        self.uic.l_democracy.setText(text)

    def write_data(self, cmd, user=''):
        label = self.uic.l_anarchy
        if config.selected == 'anarchy':
            dq = self.cmd_text_anarchy
        else:
            dq = self.cmd_text_others

        cmd = controller.button_text.get(cmd, cmd)

        cmd = ' ' * (controller.maxlen_cmd - len(cmd)) + cmd
        umaxlen = 20
        user += ' ' * (umaxlen - min(len(user), umaxlen))
        user = user[:umaxlen]
        dq.append(user + '  ' + cmd)
        label.setText('\n'.join(dq))

    def create_slots(self):
        def add_user():
            self.ui.frame_user.setEnabled(True)
            self.current_user = None

        def edit_user():
            item = self.ui.table_user.currentItem()
            if item is None:
                return
            self.ui.frame_user.setEnabled(True)

            idx = self.ui.table_user.currentIndex()
            name = item.text(0)
            user = User.get(name)
            self.current_user = idx, user

            self.ui.edit_name.setText(name)
            if isinstance(user, PersonUser):
                self.ui.tabWidget.setCurrentWidget(self.ui.tab)
                self.ui.edit_ip.setText(user.ip)
            elif isinstance(user, PCUser):
                self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)
                self.ui.pc_period.setValue(user.period)

        def save_person_user():
            name = self.ui.edit_name.text()
            ip = self.ui.edit_ip.text()

            if self.current_user is not None:
                self.ui.table_user.itemFromIndex(self.current_user[0]).setText(0, name)
                user = self.current_user[1]
            else:
                user = PersonUser(name, ip)

            user.name = name
            user.ip = ip

            self.ui.edit_name.setText('')
            self.ui.edit_ip.setText('')
            self.ui.frame_user.setEnabled(False)

        def save_pc_user():
            name = self.ui.edit_name.text()
            period = self.ui.pc_period.value()
            if self.current_user is not None:
                self.ui.table_user.itemFromIndex(self.current_user[0]).setText(0, name)
                user = self.current_user[1]
            else:
                user = PCUser(name, period, None)

            user.name = name
            user.period = period

            self.ui.edit_name.setText('')
            self.ui.frame_user.setEnabled(False)

        def set_mode(index):
            mode = self.ui.mode.itemText(index).lower()
            log.logger.log(type='gameplay', action='change_mode', content=mode)
            config.selected = mode
            self.uic.l_mode.setText(mode.capitalize())
            self.uic.f_democracy.setShown(mode != 'anarchy')
            self.cmd_text_anarchy.clear()
            self.cmd_text_others.clear()

        def delete_user():
            item = self.ui.table_user.currentItem()
            if item is None:
                return
            idx = self.ui.table_user.currentIndex()
            name = item.text(0)
            user = User.get(name)
            if isinstance(user, PersonUser):
                print('Cannot delete Person User:', name)
                return
            user.stop = True
            User.users.pop(name)  # Let gc do its job...
            self.ui.table_user.takeTopLevelItem(idx.row())

        def _button_option_block(buttons, widget):
            layout = QtGui.QVBoxLayout()
            layout.setSpacing(0)
            layout.setMargin(0)
            btns = []
            for cmd, value in buttons:
                inner = QtGui.QWidget()
                inner_layout = QtGui.QHBoxLayout()
                inner_layout.setSpacing(0)
                inner_layout.setMargin(0)
                inner_layout.addWidget(QtGui.QLabel(cmd.capitalize()))
                inner_layout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
                line_edit = ClickLineEdit(cmd, int(value))
                btns.append(line_edit)
                line_edit.setMaximumWidth(80)
                inner_layout.addWidget(line_edit)
                inner.setLayout(inner_layout)
                layout.addWidget(inner)
            widget.setLayout(layout)
            return btns

        def save_buttons_value():
            for widget in self.widget_buttons:
                controller.button_hold[widget.name] = str(widget.key_value).encode('ascii')

        def set_buttons():
            self.btn_window = QtGui.QMainWindow()
            set_fossil(self.btn_window)
            ui = form_buttons.Ui_MainWindow()
            ui.setupUi(self.btn_window)
            btns = list(controller.button_hold.items())
            self.widget_buttons = \
                _button_option_block(btns[:len(btns)//2], ui.buttons_1) + \
                _button_option_block(btns[len(btns)//2:], ui.buttons_2)

            ui.pushButton.clicked.connect(save_buttons_value)
            self.btn_window.show()

        self.ui.activate.clicked.connect(config.set_variable('enabled'))
        self.ui.random_name.clicked.connect(lambda: self.ui.edit_name.setText(randomness.select_name()))
        self.ui.lst_add.clicked.connect(add_user)
        self.ui.lst_edit.clicked.connect(edit_user)
        self.ui.save_person.clicked.connect(save_person_user)
        self.ui.save_pc.clicked.connect(save_pc_user)
        self.ui.time_button_hold.valueChanged.connect(config.set_variable('click_duration'))
        self.ui.box_hold_button.clicked.connect(config.set_variable('hold_click'))
        self.ui.time_democracy.valueChanged.connect(config.set_variable('democracy_time'))
        self.ui.time_raffle.valueChanged.connect(config.set_variable('raffle_time'))
        self.ui.time_delay.valueChanged.connect(config.set_variable('delay'))
        self.ui.mode.currentIndexChanged.connect(set_mode)
        self.ui.lst_del.clicked.connect(delete_user)
        self.ui.set_buttons.clicked.connect(set_buttons)

        set_mode(config.mode_idx(config.selected))

if __name__ == '__main__':
    log.logger.log(type='meta', message='Program started')
    prog = Main()
    prog.app.exec_()
    # This is not being called.
    # TODO: hook these things to the quit signal from Qt.
    # TODO: also close all the TCP connections!
    log.logger.stop()