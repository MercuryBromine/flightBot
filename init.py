from selenium import webdriver
from time import sleep


def main():
    flightBot()

class flightBot:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def findFlights(self):

        self.driver.get("https://www.qatarairways.com/en-gb/homepage.html")

        sleep(10)

        #Departure Destination#
        userDeparture = input("Enter the departure airport in the following format 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nDeparture Airport: ")
        departure_field = self.driver.find_element_by_xpath('//*[@id="T7-from"]')
        departure_field.click()
        departure_field.send_keys(userDeparture)

        sleep(2)

        #Arrival Destination#
        print("")
        userArrival = input("Enter the arrival airport in the following format: 'City' '(Airport Code)'\nFor example: 'Cardiff (CWL)'\nArrival Airport: '")
        arrival_field = self.driver.find_element_by_xpath('//*[@id="T7-to"]')
        arrival_field.click()
        arrival_field.send_keys(userArrival)

        sleep(2)

        #Departure Date#
        print("")
        userDepartureDate = input("Enter the departure date in the following format: 'Day' 'Month' 'Year'\nFor example: '06 Jun 2020'\nDeparture Date: ")
        departure_date = self.driver.find_element_by_xpath('//*[@id="T7-departure_1"]')
        departure_date.click()
        departure_date.clear()
        departure_date.send_keys(userDepartureDate)

        sleep(2)

        #Arrival Date#
        print("")
        userArrivalDate = input("Enter the arrival date in the following format: 'Day' 'Month' 'Year'\nFor example: '06 Jun 2020'\nArrival Date: ")
        arrival_date = self.driver.find_element_by_xpath('//*[@id="T7-arrival_1"]')
        arrival_date.click()
        arrival_date.clear()
        arrival_date.send_keys(userArrivalDate)

        sleep(2)

        #Clearing the Date Screen#
        tab_field = self.driver.find_element_by_xpath('//*[@id="tab1"]')
        self.driver.
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



