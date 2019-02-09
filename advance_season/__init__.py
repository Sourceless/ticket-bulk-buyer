from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait


DRIVER = webdriver.Chrome()
DRIVER.implicitly_wait(10)


def get_price_and_times(date, start, end, origin, destination):
    DRIVER.get('https://thetrainline.com/')

    from_ = DRIVER.find_element_by_id('from.text')
    from_.send_keys(origin)
    from_.send_keys(Keys.RETURN)

    to_ = DRIVER.find_element_by_id('to.text')
    to_.send_keys(destination)
    to_.send_keys(Keys.RETURN)

    return_ = DRIVER.find_element_by_id('return')
    return_.click()

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
    return price.get_attribute('innerText')


def main():
    for date in ['26-Feb-19', '27-Feb-19', 28]
    tickets = get_price_and_times('26-Feb-19', '09:00', '18:00', 'York', 'Leeds')
    print(tickets)


if __name__ == '__main__':
    main()
