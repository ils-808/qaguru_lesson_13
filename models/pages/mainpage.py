from selene import browser, have


class MainPage:
    def open(self):
        browser.open('/')

    def add_todo(self, value):
        browser.element('.new-todo').type(value).press_enter()

    def delete_todo(self, value):
        browser.all('.view>label').element_by(have.text(value)).hover().element('.destroy').click()

    def mark_as_done(self, value):
        browser.all('.view>label').element_by(have.text(value)).element('.toggle').click()

    def check_value_exist(self, value):
        return browser.all('.view>label').should(have.texts(value))
