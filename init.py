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

        departure_message = "Enter the departure date in the following format: 'Day' 'Month', 'Year'\nFor example: '01 Jan 2020'\n"
        arrival_message = "Enter the arrival date in the following format: 'Day' 'Month', 'Year'\nFor example: '01 Jan 2020'\n"

        earliest_departure_date = input(departure_message + "Earliest Departure Date: ")
        print("")
        latest_departure_date = input(departure_message + "Latest Departure Date: ")
        print("")
        earliest_arrival_date = input(arrival_message + "Earliest Arrival Date: ")
        print("")
        latest_arrival_date = input(arrival_message + "Latest Arrival Date: ")

        departure_airport = input("Enter the departure airport in the following format: 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nDeparture Airport: ")
        arrival_airport = input("Enter the arrival airport in the following format: 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nArrival Airport: ")

        self.earliest_departure_date = datetime.datetime.strptime(earliest_departure_date,"%d %b %Y")
        self.latest_departure_date = datetime.datetime.strptime(latest_departure_date,"%d %b %Y")
        self.earliest_arrival_date = datetime.datetime.strptime(earliest_arrival_date,"%d %b %Y")
        self.latest_arrival_date = datetime.datetime.strptime(latest_arrival_date,"%d %b %Y")

        self.departure_delta = self.latest_departure_date - self.earliest_departure_date
        self.departure_delta = self.departure_delta.days + 1

        self.arrival_delta = self.latest_arrival_date - self.earliest_arrival_date
        self.arrival_delta = self.arrival_delta.days + 1

        self.driver.get("https://www.qatarairways.com/en-gb/homepage.html")

        sleep(12)

        #Departure Destination#
        departure_field = self.driver.find_element_by_xpath('//*[@id="T7-from"]')
        departure_field.click()
        departure_field.send_keys(departure_airport) 

        sleep(1)

        #Arrival Destination#
        arrival_field = self.driver.find_element_by_xpath('//*[@id="T7-to"]')
        arrival_field.click()
        arrival_field.send_keys(arrival_airport) 

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
        self.arrival_prices()
        self.departure_prices()

    def findPrices(self,delta,price_date,identifier,next_page_xpath):
        self.price_array = []
        more_dates = self.driver.find_element_by_xpath('//*[@id="flightDetailForm_outbound:calendarInitiator_OutBound"]')
        more_dates.click()
        sleep(35)
        count = 1

        while count <= delta: #need to make as a temp variable
            try:
                content = self.driver.page_source
                soup = BeautifulSoup(content)
                temp_date = price_date.strftime('%m%d%Y')
                date_id = identifier + temp_date
                price = soup.find(id=date_id)

                if price == None:
                    next_page = self.driver.find_element_by_xpath(next_page_xpath)
                    self.driver.execute_script("arguments[0].click();", next_page)
                    sleep(35)
                    content = self.driver.page_source
                    soup = BeautifulSoup(content)
                    price = soup.find(id=date_id)
                    self.price_array.append(price.text)
                    price_date += datetime.timedelta(days=1)
                    count += 1

                else:
                    self.price_array.append(price.text)
                    price_date += datetime.timedelta(days=1)
                    count +=1

            except Exception:
                back = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:calReturnFlow"]/div[1]/button')
                back.click()
                sleep(2)
                more_dates.click()
                sleep(35)
                continue

        

    def departure_prices(self):
        delta = self.departure_delta
        outbound_identifier = 'OB1_'
        price_date = self.earliest_departure_date
        self.next_page_xpath = '//*[@id="monthlyCalendarForm:j_id_22f:0:nex"]'
        self.findPrices(delta,price_date,outbound_identifier,next_page_xpath)

        count = 0
        for i in self.price_array:
            element = i.replace('\n','').replace('\t','')
            self.price_array[count] = element
            count += 1

        while '' in self.price_array:
            self.price_array.remove('')

        f = open("departure_prices.txt", "w").close()
        f = open("departure_prices.txt", "a")
        count = 1

        file_date = self.earliest_departure_date
        temp_date = file_date
        min_date = self.price_array.index(min(self.price_array)) + 1
        temp_date += datetime.timedelta(days=min_date)
        temp_date = temp_date.strftime('%b %Y')
        min_price = min(self.price_array)

        f.write("The minimum price is on " + str(min_date) + " " + temp_date + " : " + "£" + str(min_price) + "\n")

        for i in self.price_array:
            temp_date = file_date.strftime('%d %b %Y')
            f.write("The price on " + temp_date + " : " + "£" + str(i) + "\n")
            file_date += datetime.timedelta(days=1)
        f.close()

    def arrival_prices(self):
        delta = self.arrival_delta
        inbound_identifier = 'RT1_'
        price_date = self.earliest_arrival_date
        next_page_xpath = '//*[@id="monthlyCalendarForm:j_id_22f:1:nex"]'

        self.findPrices(delta,price_date,inbound_identifier,next_page_xpath)

        count = 0
        for i in self.price_array:
            element = i.replace('\n','').replace('\t','')
            self.price_array[count] = element
            count += 1

        while '' in self.price_array:
            self.price_array.remove('')

        f = open("arrival_prices.txt", "w").close()
        f = open("arrival_prices.txt", "a")
        count = 1

        file_date = self.earliest_arrival_date
        temp_date = file_date
        min_date = self.price_array.index(min(self.price_array)) + 1
        temp_date += datetime.timedelta(days=min_date)
        temp_date = temp_date.strftime('%b %Y')
        min_price = min(self.price_array)

        f.write("The minimum price is on " + str(min_date) + " " + temp_date + " : " + "£" + str(min_price) + "\n")

        for i in self.price_array:
            temp_date = file_date.strftime('%d %b %Y')
            f.write("The price on " + temp_date + " : " + "£" + str(i) + "\n")
            file_date += datetime.timedelta(days=1)
        f.close()




if __name__ == '__main__':
    main()