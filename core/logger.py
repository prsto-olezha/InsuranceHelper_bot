from loguru import logger
import sys
#=============================

class Formatter:
    def __init__(self):
        self.padding = 0
        self.fmt = "{time:DD-MM-YYYY at HH:mm:ss} " \
                   "| {level} | " \
                   "{name}:{function}:{line}{extra[padding]} " \
                   "| {message}\n{exception}"

    def format(self, record):
        length = len("{name}:{function}:{line}".format(**record))
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt
    


formatter = Formatter()

logger.remove()
logger.add("core/logs/{time:YY-MM-DD}.log", rotation='00:00')
logger.add(sys.stderr, format=formatter.format)