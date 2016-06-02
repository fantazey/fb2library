# -*- coding: utf-8 -*-

from datetime import datetime
from os import path


class Logger:
    def __init__(self, wid, folder):
        """
        :param wid: logger id for filename
        :param folder: folder for saving logs
        :return:
        """
        self.logfile = path.join(folder, 'log ' + str(wid) + '.txt')

    def info(self, *args):
        self.log("INF", *args)

    def debug(self, *args):
        self.log("DBG", *args)

    def error(self, *args):
        self.log("ERR", *args)

    def log(self, _class, *args):
        with open(self.logfile, 'a') as log:
            _data = u''
            for sub_str in args:
                if isinstance(sub_str, str):
                    decoded = False
                    try:
                        _data += sub_str.decode("utf-8")
                        decoded = True
                    except UnicodeDecodeError, e:
                        pass
                    if not decoded:
                        try:
                            _data += sub_str.decode("cp1251")
                        except UnicodeDecodeError, e:
                            pass
                elif isinstance(sub_str, unicode):
                    _data += sub_str
                else:
                    try:
                        _data += unicode(sub_str)
                    except Exception, e:
                        pass
            data_str = u"%s [%s] %s\n" % (
                _class,
                datetime.now().strftime('%y-%m-%d %H:%M:%S'),
                _data
            )
            log.write(data_str.encode("utf-8"))
