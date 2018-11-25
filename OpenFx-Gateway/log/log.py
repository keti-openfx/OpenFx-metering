import logging
import logging.handlers




def metering_log(level,msg):
    logger = logging.getLogger('metering')
    fomatter = logging.Formatter('[ % (levelname)s | % (filename)s: % (lineno)s] % (asctime)s > % (message)s')
    fileHandler = logging.FileHandler("./metering_log")
    streamHandler = logging.StreamHandler()
    fileHandler.setFormatter(fomatter)
    streamHandler.setFormatter(fomatter)
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)
    if level=='debug':
        logger.debug(str(msg))
    elif level=='info':
        logger.info(str(msg))
    elif level=='error':
        logger.error(str(msg))
    elif level=='critical':
        logger.critical(str(msg))

