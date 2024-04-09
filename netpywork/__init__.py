from .constants import *
from .server import *
from .client import *
from .protocol import *
from datetime import timedelta

__version__ = constants.VERSION
udp_storetime: timedelta = timedelta(minutes=5)