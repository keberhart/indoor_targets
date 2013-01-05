#!/usr/bin/env python
#
#   Kyle Eberhart - 12DEC12
#

from ConfigParser import SafeConfigParser
import gtk
import pygtk
import logging
import pango
import sys
import os
import gtktargets

CFG_FILE_NAME = 'program.cfg'
LOG_FILE_NAME = '/tmp/program.log'


class Window(gtk.Window):
    '''The main window of our application.'''

    def __init__(self):
        '''init all of the fun stuff in our window.'''
        self.setup_configs()
        self.setup_logging()
        self.setup_window()
        self.show_all()

    def setup_window(self):
        '''Set up all the bits of our window.'''
        gtk.Window.__init__(self)
        self.set_title("Shot Detector")
        self.resize(230, 150)
        self.connect('destroy', lambda w: gtk.main_quit())
        self.connect('delete_event', lambda w, e: gtk.main_quit())

        # Now start adding gui bits
        vbox1 = gtk.VBox(False, 0)
        self.add(vbox1)
        vbox1.show()

        # menubar bits
        menu_bar = gtk.MenuBar()
        vbox1.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        # File menu
        file_item = gtk.MenuItem('File')
        file_item.show()
        file_menu = gtk.Menu()
        quit_item = gtk.MenuItem('Quit')
        quit_item.connect_object('activate', lambda w: gtk.main_quit(), None)
        quit_item.show()
        file_menu.append(quit_item)
        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)

        # Drawing area
        self.draw_area = gtktargets.SmallBore50Ft()
        vbox1.pack_start(self.draw_area, True, True, 0)

    def setup_configs(self):
        '''Read our config files if any and do what they say.'''
        self.log_enable = False
        config_file = os.path.join(sys.path[0], CFG_FILE_NAME)
        if not os.path.exists(config_file):
            return False
        config_parser = SafeConfigParser()
        config_parser.read(config_file)
#TODO: Add some more code here to actually read in the config file.

    def setup_logging(self):
        '''Configure our logging stuff.'''
        if not self.log_enable:
            return
        self.log_name = LOG_FILE_NAME
        LEVELS = {'DEBUG' : logging.DEBUG,
                  'INFO' : logging.INFO,
                  'WARNING' : logging.WARNING,
                  'ERROR' : logging.ERROR,
                  'CRITICAL' : logging.CRITICAL,
                  }
        level = LEVELS.get((self.log_level.upper()), logging.NOTSET)
        logging.basicConfig(level=level, filename=self.log_name)
        self.logger = logging.getLogger(__name__)

if __name__ == "__main__":
    win = Window()
    target = gtk.main()
