from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import datetime


def main():
    flightBot()

class flightBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.findFlights()

    def findFlights(self):

        message = "Enter the earliest departure date in the following format: 'Day' 'Month', 'Year'\nFor example: '01 Jan 2020'\n"
        earliest_departure_date = input(message + "Earliest Departure Date: ")
        print("")
        latest_departure_date = input(message + "Latest Departure Date: ")
        print("")
        earliest_arrival_date = input(message + "Earliest Arrival Date: ")
        print("")
        latest_arrival_date = input(message + "Latest Arrival Date: ")

        self.earliest_departure_date = datetime.datetime.strptime(earliest_departure_date,"%d %b %Y")
        self.latest_departure_date = datetime.datetime.strptime(latest_departure_date,"%d %b %Y")
        self.earliest_arrival_date = datetime.datetime.strptime(earliest_arrival_date,"%d %b %Y")
        self.latest_arrival_date = datetime.datetime.strptime(latest_arrival_date,"%d %b %Y")

        self.delta = self.latest_departure_date - self.earliest_departure_date
        self.delta = self.delta.days + 1

        self.driver.get("https://www.qatarairways.com/en-gb/homepage.html")

        sleep(12)

        #Departure Destination#
        departure_field = self.driver.find_element_by_xpath('//*[@id="T7-from"]')
        departure_field.click()
        departure_field.send_keys('Cardiff (CWL)') 

        sleep(1)

        #Arrival Destination#
        arrival_field = self.driver.find_element_by_xpath('//*[@id="T7-to"]')
        arrival_field.click()
        arrival_field.send_keys('Amritsar (ATQ)') 

        sleep(1)

        #Departure Date#
        departure_date = self.driver.find_element_by_xpath('//*[@id="T7-departure_1"]')
        departure_date.click()
        departure_date.clear()
        departure_temp_date = self.earliest_departure_date.strftime('%d %b %Y')
        departure_date.send_keys(departure_temp_date)

        sleep(1)

        #Arrival Date#
        arrival_date = self.driver.find_element_by_xpath('//*[@id="T7-arrival_1"]')
        arrival_date.click()
        arrival_date.clear()
        arrival_temp_date = self.earliest_arrival_date.strftime('%d %b %Y')
        arrival_date.send_keys(arrival_temp_date) 

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

        #Search Button#
        search_btn = self.driver.find_element_by_xpath('//*[@id="T7-search"]')
        search_btn.click()
        sleep(25)
        self.findPrices()

    def findPrices(self):
        price_array = []
        price_date = self.earliest_departure_date
        more_dates = self.driver.find_element_by_xpath('//*[@id="flightDetailForm_outbound:calendarInitiator_OutBound"]')
        more_dates.click()
        sleep(35)
        #May need to use a while loop and a counter as if the loading page freezes then the last values will be missed
        for i in range(1,self.delta):
            try:
                content = self.driver.page_source
                soup = BeautifulSoup(content)
                temp_date = price_date.strftime('%m%d%Y')
                date_id = 'OB1_'+ temp_date
                price = soup.find(id=date_id)

                if price == None:
                    next_page = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:j_id_22f:0:nex"]')
                    next_page.click()
                    sleep(35)
                    content = self.driver.page_source
                    soup = BeautifulSoup(content)
                    price = soup.find(id=date_id)
                    price_array.append(price.text)
                    price_date += datetime.timedelta(days=1)

                else:
                    price_array.append(price.text)
                    price_date += datetime.timedelta(days=1)

            except Exception:
                back = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:calReturnFlow"]/div[1]/button')
                back.click()
                sleep(2)
                more_dates.click()
                sleep(35)
                continue

        count = 0
        for i in price_array:
            element = i.replace('\n','').replace('\t','')
            price_array[count] = element
            count += 1

        f = open("prices.txt", "w").close()
        f = open("prices.txt", "a")
        count = 1

        file_date = self.earliest_departure_date
        temp_date = file_date
        min_date = price_array.index(min(price_array)) + 1
        temp_date += datetime.timedelta(days=min_date)
        temp_date = temp_date.strftime('%b %Y')
        min_price = min(price_array)

        f.write("The minimum price is on " + str(min_date) + " " +temp_date+ " : " +  + "£" + str(min_price) + "\n")

        for i in price_array:
            temp_date = file_date.strftime('%d %b %Y')
            f.write("The price on " + temp_date + " : " + + "£" + str(i) + "\n")
            file_date += datetime.timedelta(days=1)
        f.close()

if __name__ == '__main__':
    main()