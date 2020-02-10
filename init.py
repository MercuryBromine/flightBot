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
        self.date = datetime.datetime.strptime("01 May 2020","%d %b %Y")
        self.prices = []
        self.driver.get("https://www.qatarairways.com/en-gb/homepage.html")

        sleep(12)

        #Departure Destination#
        #userDeparture = input("Enter the departure airport in the following format 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nDeparture Airport: ")
        departure_field = self.driver.find_element_by_xpath('//*[@id="T7-from"]')
        departure_field.click()
        departure_field.send_keys('Cardiff (CWL)') #userDeparture

        sleep(1)

        #Arrival Destination#

        #userArrival = input("Enter the arrival airport in the following format: 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nArrival Airport: ")
        arrival_field = self.driver.find_element_by_xpath('//*[@id="T7-to"]')
        arrival_field.click()
        arrival_field.send_keys('Amritsar (ATQ)') #userArrival

        sleep(1)

        #Departure Date#

        #userDepartureDate = input("Enter the departure date in the following format: 'Day' 'Month' 'Year'\nFor example: '06 Jun 2020'\nDeparture Date: ")
        departure_date = self.driver.find_element_by_xpath('//*[@id="T7-departure_1"]')
        departure_date.click()
        departure_date.clear()

        self.tempDate = self.date.strftime('%d %b %Y')
        departure_date.send_keys(self.tempDate)

        sleep(1)

        #Arrival Date#

        #userArrivalDate = input("Enter the arrival date in the following format: 'Day' 'Month' 'Year'\nFor example: '06 Jun 2020'\nArrival Date: ")
        arrival_date = self.driver.find_element_by_xpath('//*[@id="T7-arrival_1"]')
        arrival_date.click()
        arrival_date.clear()
        arrival_date.send_keys('06 Jun 2020') #userArrivalDate

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
        self.findPrices()

    def findPrices(self):

        sleep(15)

        more_dates = self.driver.find_element_by_xpath('//*[@id="flightDetailForm_outbound:calendarInitiator_OutBound"]')
        more_dates.click()
        sleep(25)
        content = self.driver.page_source
        soup = BeautifulSoup(content)
        tempDate = self.date.strftime('%m-%d-%Y')
        dateArr = tempDate.split('-')
        dateArr[1] = list(dateArr[1])
        dateArr[1][0] = int(dateArr[1][0])
        dateArr[1][1] = int(dateArr[1][1])
        priceArr = []

        for i in range(1,32):
            date_id = 'OB1_'+dateArr[0]+str(dateArr[1][0])+str(dateArr[1][1])+dateArr[2]
            price = soup.find(id=date_id)
            if price == None:
                next_page = self.driver.find_element_by_xpath('//*[@id="monthlyCalendarForm:j_id_22f:0:nex"]')
                next_page.click()
                sleep(30)
                content = self.driver.page_source
                soup = BeautifulSoup(content)
                price = soup.find(id=date_id)
                priceArr.append(price.text)
            else:
                priceArr.append(price.text)
            dateArr[1][1] += 1
            if dateArr[1][1] == 10:
                dateArr[1][0] += 1
                dateArr[1][1] = 0

        count = 0
        for i in priceArr:
            element = i.replace('\n','').replace('\t','')
            priceArr[count] = element
            count += 1

        f = open("prices.txt", "w").close()
        f = open("prices.txt", "a")
        count = 1
        monthYearDate = self.date.strftime('%d-%b-%Y')
        monthYearDateArr = monthYearDate.split('-')

        min_date = priceArr.index(min(priceArr)) + 1
        min_price = min(priceArr)
        f.write("The minimum price is on " + str(min_date) + " " + monthYearDateArr[1] + " " +  monthYearDateArr[2] + " " + str(min_price) + "\n")

        for i in priceArr:
            f.write("The price on " + str(count) + " " + monthYearDateArr[1] + " " + monthYearDateArr[2] + ": " + str(i) + "\n")
            count += 1
        f.close()

if __name__ == '__main__':
    main()