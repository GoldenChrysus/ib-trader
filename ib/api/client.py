import easyib
from ib.singleton import Singleton
import time
import threading
import warnings

warnings.filterwarnings('ignore')


class IBClient(metaclass=Singleton):
    def __init__(self) -> None:
        self.api = easyib.REST()
        thread = threading.Thread(target=self.keep_alive)

        thread.start()

    def keep_alive(self):
        while True:
            self.api.re_authenticate()
            time.sleep(60)
