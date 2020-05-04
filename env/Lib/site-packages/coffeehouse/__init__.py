from . import api
from .api import *  # noqa: F403,F401

from . import exception
from .exception import *  # noqa: F403,F401

from . import lydia
from .lydia import *  # noqa: F403,F401

__all__ = ["api",
           "exception",
           "lydia"] + api.__all__ + exception.__all__ + lydia.__all__
__version__ = "2.1.0"
__author__ = "Intellivoid Technologies"
__source__ = "https://github.com/intellivoid/CoffeeHouse-Python-API-Wrapper"
__copyright__ = "Copyright (c) 2017-2020 " + __author__
