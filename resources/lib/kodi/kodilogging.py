# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

import xbmc

import xbmcaddon

from resources.lib.tubecast.utils import PY3


class KodiLogHandler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)
        addon_id = xbmcaddon.Addon().getAddonInfo('id')
        if not PY3:
            addon_id = addon_id.decode('utf-8')
        prefix = "[%s] " % addon_id
        formatter = logging.Formatter(prefix + '%(name)s: %(message)s')
        self.setFormatter(formatter)

    def emit(self, record):
        levels = {
            logging.CRITICAL: xbmc.LOGFATAL,
            logging.ERROR: xbmc.LOGERROR,
            logging.WARNING: xbmc.LOGWARNING,
            logging.INFO: xbmc.LOGINFO,
            logging.DEBUG: xbmc.LOGDEBUG,
            logging.NOTSET: xbmc.LOGNONE,
        }
        try:
            xbmc.log(self.format(record), levels[record.levelno])
        except UnicodeEncodeError:
            xbmc.log(self.format(record).encode(
                'utf-8', 'ignore'), levels[record.levelno])

    def flush(self):
        pass


def config():
    logger = logging.getLogger()
    logger.addHandler(KodiLogHandler())
    logger.setLevel(logging.DEBUG)


def get_logger():
    return logging.getLogger(xbmcaddon.Addon().getAddonInfo('id'))
