from exchange.bitmex.liveApi import liveLogger

logger = liveLogger.getLiveLogger("Exception")

def ErrorShow(msg):
    logger.warning(msg)

