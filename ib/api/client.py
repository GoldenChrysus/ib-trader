import easyib
from ib.singleton import Singleton
import warnings

warnings.filterwarnings('ignore')


class IBClient(metaclass=Singleton):
    def __init__(self) -> None:
        self.api = easyib.REST()
