import logging
from datetime import datetime
import os


now = datetime.now()
logfile = f'chatlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
logpath = os.path.join('logs', logfile)
logging.basicConfig(filename=logpath, 
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s',
                    datefmt='%H:%M:%S')
logger = logging.getLogger()

logger.info("This is a test")
logger.info("Another test")
