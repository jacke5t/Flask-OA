from BluePrint import make_manage
from BluePrint import create_app
from config import Develop, Product


app = create_app(Develop)
manager = make_manage()


if __name__ == '__main__':
    manager.run()

