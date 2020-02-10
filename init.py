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
        userDepartureDate = input("Enter the departure date in the following format: 'Day' 'Month', 'Year'\nFor example 05 May 2020\nDeparture Date: ")
        userArrivalDate = input("Enter the last departure date in the following format: 'Day' 'Month' 'Year'\nFor example: '06 Jun 2020'\nArrival Date: ")
        self.date = datetime.datetime.strptime(userDepartureDate,"%d %b %Y")
        self.arrival_date = datetime.datetime.strptime(userArrivalDate,"%d %b %Y")
        self.delta = self.arrival_date - self.date
        self.delta = self.delta.days + 1
        print(self.delta)

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

        tempDate = self.date.strftime('%d %b %Y')
        departure_date.send_keys(tempDate)

        sleep(1)

        #Arrival Date#
        arrival_date = self.driver.find_element_by_xpath('//*[@id="T7-arrival_1"]')
        arrival_date.click()
        arrival_date.clear()

        arrival_temp_date = self.arrival_date
        arrival_temp_date += datetime.timedelta(days=15)
        arrival_temp_date = arrival_temp_date.strftime('%d %b %Y')
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
        more_dates = self.driver.find_element_by_xpath('//*[@id="flightDetailForm_outbound:calendarInitiator_OutBound"]')
        more_dates.click()
        sleep(35)
        content = self.driver.page_source
        soup = BeautifulSoup(content)
        priceArr = []
        price_date = self.date
        for i in range(1,self.delta):
            try:
                tmp_date = price_date.strftime('%m%d%Y')
                date_id = 'OB1_'+tmp_date
                price = soup.find(id=date_id)
                if price == None:
                    next_page = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:j_id_22f:0:nex"]')
                    next_page.click()
                    sleep(35)
                    content = self.driver.page_source
                    soup = BeautifulSoup(content)
                    price = soup.find(id=date_id)
                    priceArr.append(price.text)
                    price_date += datetime.timedelta(days=1)
                else:
                    priceArr.append(price.text)
                    price_date += datetime.timedelta(days=1)
            except Exception:
                back = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:calReturnFlow"]/div[1]/button')
                back.click()
                sleep(2)
                continue

        count = 0
        for i in priceArr:
            element = i.replace('\n','').replace('\t','')
            priceArr[count] = element
            count += 1

        f = open("prices.txt", "w").close()
        f = open("prices.txt", "a")
        count = 1

        file_date = self.date
        tmp_date = file_date
        min_date = priceArr.index(min(priceArr)) #+ 1
        tmp_date += datetime.timedelta(days=min_date)
        tmp_date = tmp_date.strftime('%d %b %Y')
        min_price = min(priceArr)

        f.write("The minimum price is on " + str(min_date) + " " +tmp_date+ " : " +  + "£" + str(min_price) + "\n")

        for i in priceArr:
            tmp_date = file_date.strftime('%d %b %Y')
            f.write("The price on " + tmp_date + " : " + + "£" + str(i) + "\n")
            file_date += datetime.timedelta(days=1)
        f.close()

if __name__ == '__main__':
    main()