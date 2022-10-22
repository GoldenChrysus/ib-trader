import easyib
import warnings

warnings.filterwarnings('ignore')


class IBClient:
    def __init__(self) -> None:
        self.instance = easyib.REST()


CLIENT = IBClient()
INSTANCE = CLIENT.instance
