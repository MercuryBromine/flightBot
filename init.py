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

        sleep(15)

        #Departure Destination#
        #userDeparture = input("Enter the departure airport in the following format 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nDeparture Airport: ")
        departure_field = self.driver.find_element_by_xpath('//*[@id="T7-from"]')
        departure_field.click()
        departure_field.send_keys('Cardiff (CWL)') #userDeparture

        sleep(2)

        #Arrival Destination#

        #userArrival = input("Enter the arrival airport in the following format: 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nArrival Airport: ")
        arrival_field = self.driver.find_element_by_xpath('//*[@id="T7-to"]')
        arrival_field.click()
        arrival_field.send_keys('Amritsar (ATQ)') #userArrival

        sleep(2)

        #Departure Date#

        #userDepartureDate = input("Enter the departure date in the following format: 'Day' 'Month' 'Year'\nFor example: '06 Jun 2020'\nDeparture Date: ")
        departure_date = self.driver.find_element_by_xpath('//*[@id="T7-departure_1"]')
        departure_date.click()
        departure_date.clear()

        self.tempDate = self.date.strftime('%d %b %Y')
        departure_date.send_keys(self.tempDate)

        sleep(2)

        #Arrival Date#

        #userArrivalDate = input("Enter the arrival date in the following format: 'Day' 'Month' 'Year'\nFor example: '06 Jun 2020'\nArrival Date: ")
        arrival_date = self.driver.find_element_by_xpath('//*[@id="T7-arrival_1"]')
        arrival_date.click()
        arrival_date.clear()
        arrival_date.send_keys('06 Jun 2020') #userArrivalDate

        sleep(2)

        #Clearing the Date Screen#
        tab_field = self.driver.find_element_by_xpath('//*[@id="tab1"]')
        tab_field.click()

        sleep(2)

        #Passengers#
        passenger_field = self.driver.find_element_by_xpath('//*[@id="T7-passengers"]')
        passenger_field.click()
        tab_field.click()

        sleep(2)

        #Search Button#
        search_btn = self.driver.find_element_by_xpath('//*[@id="T7-search"]')
        search_btn.click()
        self.findPrices()
        self.repeatFilling()

    def findPrices(self):
        sleep(20)
        numberArr = []
        decimalArr = []
        content  = self.driver.page_source
        soup = BeautifulSoup(content)
        for i in soup.findAll('span', attrs={'class':'priceDetails'}):
            number = i.find('span', attrs={'class':'number'})
            decimal = i.find('sup', attrs={'class':'decimal'})
            numberArr.append(number.text)
            decimalArr.append(decimal.text)

        count = 0

        for i in numberArr:
            element = i.replace('\n','').replace('\t','')
            numberArr[count] = element
            count += 1

        count = 0
        tempPrices = []
        for i in numberArr:
            tempPrices.append(float(i + decimalArr[count]))
            count += 1

        self.prices.append(min(tempPrices))

        print("The lowest price is on " + self.tempDate + " May 2020 is: " + str(min(tempPrices)))

        print(self.prices)

    def repeatFilling(self):
        for i in range(1,3):
            self.driver.get("https://www.qatarairways.com/en-gb/homepage.html")

            sleep(5)

            #Departure Date#
            departure_date = self.driver.find_element_by_xpath('//*[@id="T7-departure_1"]')
            departure_date.click()
            departure_date.clear()
            self.date += datetime.timedelta(days=1)
            self.tempDate = self.date.strftime('%d %b %Y')
            departure_date.send_keys(self.tempDate)

            sleep(2)

            #Search Button#
            search_btn = self.driver.find_element_by_xpath('//*[@id="T7-search"]')
            search_btn.click()
            self.findPrices()
        #self.output()

    '''def output(self):
        self.outputFile = open("prices.txt", "a")
        for i in self.prices:
            self.outputFile.write(self.tempDate + " price: " + str(i) + "\n")'''

if __name__ == '__main__':
    main()


