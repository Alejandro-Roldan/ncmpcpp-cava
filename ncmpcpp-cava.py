#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import os, signal, sys
import subprocess


TITLE = 'ncmpcpp'

def resize(event=None): 
    ncmpcpp_widget.prestart()
    cava_widget.prestart()

def quitting(event=None, event2=None):
    ncmpcpp_widget.pkill()
    cava_widget.pkill()

    root.quit()

class Shell_Widget:
    def __init__(self, master, height, width, column, row, command):
        self.frame = tk.Frame(master, height=height, width=width)

        self.frame.grid(column=column, row=row, sticky='nwes')
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.wid = self.frame.winfo_id()
        self.command = command.format(self.wid)

        self.pstart()

    def pstart(self):
        ''' Start the process and save pid '''
        self.subprc = subprocess.run(self.command + '&', shell=True)

        self.pid = self.get_pid()

    def get_pid(self):
        '''
            Get process id using pgrep searching based on full command
            -f to search full commands
            -n to return only the newest process with that name
            Returns output in bytes so need to decode and then transform into int
        '''
        pgrep_out = subprocess.check_output(['pgrep', '-f', '-n', self.command])
        # Returns output in bytes
        # Need to decode with sys.stdout.encoding and transform from str to int
        pgrep_out = int(pgrep_out.decode(sys.stdout.encoding))

        return pgrep_out

    def pkill(self):
        ''' Kill process with process id '''
        try:
            os.kill(self.pid, signal.SIGTERM)
            return 0
        except ProcessLookupError:
            return 1

    def prestart(self):
        ''' Restarts the process '''
        self.pkill()
        self.pstart()



def Root_Binds():
    # Closing window
    root.protocol('WM_DELETE_WINDOW', quitting)
    signal.signal(signal.SIGINT, quitting)
    signal.signal(signal.SIGTERM, quitting)
    # Window resizing 
    root.bind('<Configure>', resize)


if __name__ == '__main__':
    root = tk.Tk()

    root.title(TITLE)
    # root.attributes('-zoomed', True)  # makes the window a pop up/dialog
    root.update()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe = tk.Frame(root)
    mainframe.grid(column=0, row=0, sticky='nwes')
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=5)
    mainframe.rowconfigure(1, weight=3)

    ncmpcpp_command = 'urxvt -embed {} -e ncmpcpp'
    ncmpcpp_widget = Shell_Widget(mainframe, 400, 800, 0, 0, ncmpcpp_command)

    cava_command = 'urxvt -embed {} -e cava'
    cava_widget = Shell_Widget(mainframe, 200, 800, 0, 1, cava_command)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=0, pady=0)

    Root_Binds()

    root.mainloop()