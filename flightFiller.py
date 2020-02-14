from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import datetime


def main(master):
    flightFiller(master)

class flightFiller:
    def __init__(self,master):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.qatarairways.com/en-gb/homepage.html")
        sleep(12)

        #Departure Destination#
        departure_field = self.driver.find_element_by_xpath('//*[@id="T7-from"]')
        departure_field.click()
        departure_field.send_keys(master.departure_airport) 

        sleep(1)

        #Arrival Destination#
        arrival_field = self.driver.find_element_by_xpath('//*[@id="T7-to"]')
        arrival_field.click()
        arrival_field.send_keys(master.arrival_airport) 

        sleep(1)

        #Departure Date#
        departure_date = self.driver.find_element_by_xpath('//*[@id="T7-departure_1"]')
        departure_date.click()
        departure_date.clear()

        departure_date.send_keys(master.departure_date)

        sleep(1)

        #Arrival Date#
        arrival_date = self.driver.find_element_by_xpath('//*[@id="T7-arrival_1"]')
        arrival_date.click()
        arrival_date.clear()
        arrival_date.send_keys(master.return_date) 

        sleep(1)

        #Clearing the Date Screen#
        tab_field = self.driver.find_element_by_xpath('//*[@id="tab1"]')
        tab_field.click()

        sleep(1)

        #Passengers#
        passenger_field = self.driver.find_element_by_xpath('//*[@id="T7-passengers"]')
        passenger_field.click()
        tab_field.click()

        sleep(1)

        search_btn = self.driver.find_element_by_xpath('//*[@id="T7-search"]')
        search_btn.click()
        sleep(25)
        self.findPrices(master)
    
    def findPrices(self,master):
        deltas = [master.departure_dates_delta, master.return_dates_delta]
        identifiers = ['OB1_', 'RT1_']
        price_dates = [master.earliest_departure_date, master.earliest_return_date]
        next_page_xpaths = ['//*[@id="monthlyCalendarForm:j_id_22f:0:nex"]','//*[@id="monthlyCalendarForm:j_id_22f:1:nex"]']
        files = ["departure_prices.txt", "return_prices.txt"]
        file_dates = [master.earliest_departure_date, master.earliest_return_date]
        price_array = [[],[]]

        more_dates = self.driver.find_element_by_xpath('//*[@id="flightDetailForm_outbound:calendarInitiator_OutBound"]')
        more_dates.click()
        sleep(35)
        back = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:calReturnFlow"]/div[1]/button')
        direction_count = 0
        day_count = 0
        general_count = 0

        while direction_count < 2:
            while day_count < deltas[direction_count]:
                try:
                    content = self.driver.page_source
                    soup = BeautifulSoup(content)
                    temp_date = price_dates[direction_count].strftime('%m%d%Y')
                    date_id = identifiers[direction_count] + temp_date
                    price = soup.find(id=date_id)

                    if price == None:
                        next_page = self.driver.find_element_by_xpath(next_page_xpaths[direction_count])
                        next_page.click()
                        sleep(35)
                        content = self.driver.page_source
                        soup = BeautifulSoup(content)
                        price = soup.find(id=date_id)
                        price_array[direction_count].append(price.text)
                        price_dates[direction_count] += datetime.timedelta(days=1)
                        day_count += 1
                    else:
                        price_array[direction_count].append(price.text)
                        price_dates[direction_count] += datetime.timedelta(days=1)
                        day_count += 1
                except Exception:
                    back.click()
                    sleep(2)
                    more_dates.click()
                    sleep(35)
                    continue
            
            for i in price_array[direction_count]:
                element = i.replace('\n','').replace('\t','')
                price_array[direction_count][general_count] = element
                general_count += 1

            while '' in price_array[direction_count]:
                price_array[direction_count].remove('')

            price_files = open(files[direction_count], "w").close()
            price_files = open(files[direction_count], "a")

            general_count = 1

            min_date = price_array[direction_count].index(min(price_array[direction_count])) + 1
            temp_file_date = file_dates[direction_count]
            temp_file_date += datetime.timedelta(days=min_date)
            temp_file_date = temp_file_date.strftime('%b %Y')
            min_price = min(price_array[direction_count])

            price_files.write("The minimum price is on " + str(min_date) + " " + temp_file_date + " : " + "£" + str(min_price) + "\n")

            for i in price_array[direction_count]:
                temp_file_date = file_dates[direction_count].strftime("%d %b %Y")
                price_files.write("The price on " + temp_file_date + " : " + "£" + str(i) + "\n")
                file_dates[direction_count] += datetime.timedelta(days=1)
            price_files.close()

            back = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:calReturnFlow"]/div[1]/button')
            back.click()
            sleep(2)
            more_dates.click()
            sleep(35)
            day_count = 0
            general_count = 0
            direction_count += 1

if __name__ == "__main__":
    main(master)