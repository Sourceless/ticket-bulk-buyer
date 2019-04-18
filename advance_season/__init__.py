"""
Trainline Advance Ticket Bulk Booker

Usage:
  advance_season <origin> <destination> <set_off_time> <return_time> <date_from> <date_to> <email> [-w]
  advance_season -h

Options:
  -h --help   Show this screen.
  -w          Include weekends
  --young     Include 16-25 railcard
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import WebDriverException
from docopt import docopt
import time
import datetime
import getpass


DRIVER = webdriver.Chrome()
DRIVER.implicitly_wait(10)


def really_force_click(element):
    try:
        force_click(element)
        return
    except WebDriverException:
        time.sleep(1)
        really_force_click(element)


def force_click(element):
    element.send_keys(Keys.SPACE)


def get_price_and_times(date, start, end, origin, destination, first_run=True, add_railcard=False):
    if first_run:
        DRIVER.get('https://thetrainline.com/')

        from_ = DRIVER.find_element_by_id('from.text')
        from_.send_keys(origin)
        from_.send_keys(Keys.RETURN)

        to_ = DRIVER.find_element_by_id('to.text')
        to_.send_keys(destination)
        to_.send_keys(Keys.RETURN)

        return_ = DRIVER.find_element_by_id('return')
        return_.click()
    else:
        DRIVER.get('https://thetrainline.com/')

    out_date = DRIVER.find_element_by_id('page.journeySearchForm.outbound.title')
    # out_date.send_keys(Keys.BACKSPACE * 20)
    out_date.clear()
    out_date.send_keys(date)
    out_date.send_keys(Keys.RETURN)

    out_arrive_by = DRIVER.find_element_by_name('dateType')
    Select(out_arrive_by).select_by_value('arriveBefore')

    start_hour, start_mins = start.split(':')
    hour = DRIVER.find_element_by_name('hours')
    Select(hour).select_by_value(start_hour)

    mins = DRIVER.find_element_by_name('minutes')
    Select(mins).select_by_value(start_mins)

    back_date = DRIVER.find_element_by_id('page.journeySearchForm.inbound.title')
    # out_date.send_keys(Keys.BACKSPACE * 20)
    back_date.clear()
    back_date.send_keys(date)
    back_date.send_keys(Keys.RETURN)

    end_hour, end_mins = end.split(':')
    hour = DRIVER.find_elements_by_name('hours')[1]
    Select(hour).select_by_value(end_hour)

    mins = DRIVER.find_elements_by_name('minutes')[1]
    Select(mins).select_by_value(end_mins)

    if add_railcard:
        railcard_box = DRIVER.find_element_by_id('passenger-summary-btn')
        railcard_box.click()

        railcard_button = railcard_box.find_element_by_xpath("//button[contains(.,'Add railcard')]")
        railcard_button.click()

        railcard_select = DRIVER.find_element_by_id('railcardRow0')
        Select(railcard_select).select_by_visible_text('16-25 Railcard')

        done = railcard_box.find_element_by_xpath("//button[contains(.,'Done')]")
        done.click()

    submit = DRIVER.find_element_by_xpath("//button[contains(.,'Get times & tickets')]")
    submit.click()

    price = DRIVER.find_element_by_xpath("//span[contains(@data-test,'cjs-price')]")
    return_price = price.get_attribute('innerText')

    continue_ = DRIVER.find_element_by_xpath("//button[contains(@data-test, 'cjs-button-continue')]")
    really_force_click(continue_)

    direction_select = DRIVER.find_element_by_id('direction')
    Select(direction_select).select_by_visible_text('Forward facing')

    position_select = DRIVER.find_element_by_id('position')
    Select(position_select).select_by_visible_text('Window')

    carriage_select = DRIVER.find_element_by_id('carriageType')
    Select(carriage_select).select_by_visible_text('Quiet')

    continue_ = DRIVER.find_element_by_xpath("//button[contains(@data-test, 'cjs-button-continue')]")
    really_force_click(continue_)

    time.sleep(5)

    continue_ = DRIVER.find_element_by_xpath("//button[contains(@data-test, 'cjs-button-continue')]")
    really_force_click(continue_)

    time.sleep(5)


def find_by_data_test(type_, data_test):
    return DRIVER.find_element_by_xpath("//{}[contains(@data-test, '{}')]".format(type_, data_test))


def sign_in(email_data, password_data):
    DRIVER.get('https://www.thetrainline.com/book/login')
    email = find_by_data_test('input', 'login-form-email-input')
    email.send_keys(email_data)

    password = find_by_data_test('input', 'login-form-password-input')
    password.send_keys(password_data)

    submit = find_by_data_test('button', 'login-form-submit')
    submit.click()


def calc_dates(start, end, skip_weekends=True):
    date_format = "%Y-%m-%d"
    start_date = datetime.datetime.strptime(start, date_format)
    end_date = datetime.datetime.strptime(end, date_format)

    delta = end_date - start_date

    dates = []

    for i in range(delta.days + 1):
        new_date = start_date + datetime.timedelta(i)

        if skip_weekends and new_date.weekday() in (5, 6):
            continue

        dates.append(new_date.strftime('%d-%b-%y'))

    return dates


def main():
    arguments = docopt(__doc__)

    password = getpass.getpass('Trainline password: ')
    sign_in(arguments['<email>'], password)

    first_run = True
    for date in calc_dates(arguments['<date_from>'], arguments['<date_to>'], not arguments.get('-w', False)):
        get_price_and_times(date, arguments['<set_off_time>'], arguments['<return_time>'], arguments['<origin>'], arguments['<destination>'], first_run, arguments.get('--young', False))
        first_run = False

    continue_ = DRIVER.find_element_by_xpath("//button[contains(@data-test, 'cjs-button-continue')]")
    continue_.click()

if __name__ == '__main__':
    main()
