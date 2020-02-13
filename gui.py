from tkinter import Tk, Frame, Label, Entry, StringVar, Button, messagebox
import datetime
import flightFiller

def main():
    win = Tk()
    new_window = application(win)
    win.mainloop()

class application:
    def __init__(self,master):
        #== Window Configeration ==#

        self.master = master
        self.master.resizable(False,False)
        self.master.title('Qatar Airways Flight Bot')
        #self.master.config()

        #== Frames ==#

        self.lbl_frame = Frame(self.master, width=1350, height=600, bd=10)
        self.lbl_frame.pack()

        self.btn_frame = Frame(self.master, width=1000, height=600, bd=10)
        self.btn_frame.pack()

        #==Text Variables==#

        self.departure_airport_var = StringVar()
        self.arrival_airport_var = StringVar()
        self.departure_dates_var = StringVar()
        self.return_dates_var = StringVar()

        #==Departure Airport==#

        self.departure_airport_lbl = Label(self.lbl_frame, text="Departure Airport", font=("Arial",20))
        self.departure_airport_lbl.grid(row=0,column=0,padx=8,pady=20)

        self.departure_airport_entry = Entry(self.lbl_frame, textvariable=self.departure_airport_var, font=('Arial',20))
        self.departure_airport_entry.grid(row=0,column=1,padx=8,pady=20)

        #==Arrival Airport==#
        
        self.arrival_airport_lbl =  Label(self.lbl_frame, text="Arrival Airport", font=("Arial",20))
        self.arrival_airport_lbl.grid(row=1,column=0,padx=8,pady=20)

        self.arrival_airport_entry = Entry(self.lbl_frame, textvariable=self.arrival_airport_var, font=('Arial',20))
        self.arrival_airport_entry.grid(row=1,column=1,padx=8,pady=20)

        #==Departure Dates==#

        self.departure_dates_lbl =  Label(self.lbl_frame, text="Departure Dates", font=("Arial",20))
        self.departure_dates_lbl.grid(row=2,column=0,padx=8,pady=20)

        self.departure_dates_entry = Entry(self.lbl_frame, textvariable=self.departure_dates_var, font=('Arial',20))
        self.departure_dates_entry.grid(row=2,column=1,padx=8,pady=20)

        #==Return Dates==#

        self.return_dates_lbl = Label(self.lbl_frame, text="Return Dates", font=("Arial",20))
        self.return_dates_lbl.grid(row=3,column=0,padx=8,pady=20)

        self.return_dates_entry = Entry(self.lbl_frame, textvariable=self.return_dates_var, font=('Arial',20))
        self.return_dates_entry.grid(row=3,column=1,padx=8,pady=20)

        #==Passengers==#

        '''Need to add in the function to find the passengers before adding it to the gui'''

        #==Buttons==#

        self.find_prices_btn = Button(self.btn_frame, text='Find Prices', width=17, font=('Arial',20), command=self.decode_input)
        self.find_prices_btn.grid(row=0,column=0,padx=8,pady=20)

    def decode_input(self):
        self.departure_airport = self.departure_airport_var.get()
        self.arrival_airport = self.arrival_airport_var.get()
        self.departure_dates = self.departure_dates_var.get()
        self.return_dates = self.return_dates_var.get()

        if(self.departure_airport and self.arrival_airport and self.departure_dates and self.return_dates) == "":
            messagebox.showerror("Error", "Fields cannot be blank")
        else:
            self.departure_dates = self.departure_dates.split('-')
            self.return_dates = self.return_dates.split('-')
            
            self.earliest_departure_date = datetime.datetime.strptime(self.departure_dates[0], "%d/%m/%Y")
            self.latest_departure_date = datetime.datetime.strptime(self.departure_dates[1], "%d/%m/%Y")

            self.earliest_return_date = datetime.datetime.strptime(self.return_dates[0], "%d/%m/%Y")
            self.latest_return_date = datetime.datetime.strptime(self.return_dates[1], "%d/%m/%Y")

            self.departure_date = datetime.datetime.strftime(self.earliest_departure_date, "%d %b %Y")
            self.return_date = datetime.datetime.strftime(self.earliest_return_date, "%d %b %Y")

            self.departure_dates_delta = self.latest_departure_date - self.earliest_departure_date
            self.departure_dates_delta = self.departure_dates_delta.days + 1

            self.return_dates_delta = self.latest_return_date - self.earliest_return_date
            self.return_dates_delta = self.return_dates_delta.days + 1

            self.execute_code()

    def execute_code(self):
        messagebox.showinfo("Information", "Finding Prices")
        flightFiller.main(self)
        messagebox.showinfo("Information", "Found Prices")






if __name__ == '__main__':
    main()