try:
    from .local import *
except ImportError:
    from .common import *
