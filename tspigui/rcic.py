# ############################################################################ #
# tspigui - Simple, touch-screen Raspberry Pi GUI for personal projects        #
# rcic.py - Runtime context information container                              #
# pareidolia.es, 2020                                                          #
# ############################################################################ #
# TODO Support for dynamic properties to be implemented
import logging
from logging.handlers import TimedRotatingFileHandler

class Rcic:

    SEPARATOR = '='
    COMMENT_CHAR = '#'
    
    def __init__(self, appname):

        logger = logging.getLogger(appname)
        logger.setLevel(logging.DEBUG) # Default; may be changed by config later
        fh = TimedRotatingFileHandler(appname + '.log', when='D',
                                      interval=1, backupCount=7)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s]\t %(message)s \
<%(module)s.%(funcName)s>')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        self.log = logger
        logger.info('***** ***** ***** ***** ***** ***** *****')
        logger.debug('Logger initialized')

        # Configuration properties
        self.properties_file_name = appname + '.properties'
        self.properties = self.load_properties()
        logger.debug('Properties file loaded (%s), %d properties found',
                     self.properties_file_name, len(self.properties))
        # TODO Set log level per config

        logger.info('Initialization complete!')

    def load_properties(self):
        props = {}
        with open(self.properties_file_name, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(self.COMMENT_CHAR):
                    key_value = l.split(self.SEPARATOR)
                    key = key_value[0].strip()
                    value = self.SEPARATOR.join(key_value[1:]) \
                               .strip().strip('"') 
                    props[key] = value 
        return props

    def get_property(self, key):
        return self.properties.get(key, None)

    def has_property(self, key):
        return key in self.properties
        
# ############################################################################ #
