from models.pages.mainpage import MainPage


class Application:

    def __init__(self):
        self.main_page = MainPage()

app = Application()