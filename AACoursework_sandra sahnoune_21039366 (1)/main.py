from tkinter import *
from tkinter import Tk, StringVar
import tkinter.messagebox
from unittest.mock import seal
from railwaynetworks import RailwayNetwork
'''
This class defines a GUI for the Task 1 & Task 2 
'''
class GUI(tkinter.Frame):
  def __init__(self, parent):
    tkinter.Frame.__init__(self, parent)
    self.parent = parent
    self.rail_net = RailwayNetwork()
    self.rail_net.load_railway_stations_data("railway_stations.csv")
    self.rail_net.load_railway_stations_map("railway_network.csv")
    w_width =1000
    w_height = 700
    self.parent.geometry("1000x700")
    self.parent.title("Train Ticketing System")  
    self.parent.configure(background='lightgrey')
    Label(self.parent,text="UK Railway System",font="bold 30",bg="lightgrey").place(x=w_width/2 - 200,y=5)
    
    ### --- DEFINING GUI for TASK1 -----###
    self.task1_label=Label(self.parent,text="Task 1",font="bold 25",bg="lightgrey").place(x=50,y=100)
    self.search_label=Label(self.parent,text="Enter Name",font="bold 15",bg="lightgrey").place(x=50,y=150)
    self.search_result=Text(self.parent,font="bold 15",bg="lightgrey",height=11, width=43)
    self.search_result.place(x=10,y=420)

    self.search_entry=Entry(self.parent,text='Enter Search',font="Bold 15")
    self.search_entry.place(x=250,y=155)
    self.search_train_button=Button(self.parent,text="Search for Train",command=self.search_btn_cmd,font="Bold 20").place(x=10,y=350)
    
    ### --- DEFINING GUI for TASK2 -----###
    self.task2_label=Label(self.parent,text="Task 2",font="bold 25",bg="lightgrey").place(x=500,y=100)
    self.deptarture_label=Label(self.parent,text="Choose Departure",font="bold 15",bg="lightgrey").place(x=500,y=150)
    self.arrival_label=Label(self.parent,text="Choose Arrivals",font="bold 15",bg="lightgrey").place(x=500,y=250)

    self.deptarture_entry=Entry(self.parent,text='Enter destination or CSR',font="Bold 15")
    self.deptarture_entry.place(x=700,y=155)
    self.arrival_entry=Entry(self.parent,text='Enter Arrival or CSR',font="Bold 15")
    self.arrival_entry.place(x=700,y=255)
    self.search_route_button=Button(self.parent,text="Search for Route",command=self.route_btn_cmd,font="Bold 20").place(x=500,y=350)
    self.route_result=Text(self.parent,font="bold 15",bg="lightgrey",height=11, width=43)
    self.route_result.place(x=500,y=420)

  def search_btn_cmd(self):
    result_str = ""
    result = self.rail_net.search_railway_station(self.search_entry.get())
    for key  in result:
        result_str+="\n"
        if key != 'x':
            result_str+="{0}, {1}".format(key,result[key])
        else:
            result_str+=result[key]
    if len(self.search_result.get(1.0,END)) > 0:
        self.search_result.delete(1.0,END)
    self.search_result.insert(END,"Search Result:{0}".format(result_str))


  def route_btn_cmd(self):
    result_str = ""
    dep= self.deptarture_entry.get()
    arriv = self.arrival_entry.get()
    result = self.rail_net.search_railway_path(dep,arriv)
    if type(result) is str:
      result_str = result
    else:
      for x  in range(len(result)):
          result_str+="\n\t|\n\tv\n"
          result_str+=result[x]
    if len(self.route_result.get(1.0,END)) > 0:
        self.route_result.delete(1.0,END)
    self.route_result.insert(END,"Search Result:{0}".format(result_str))
    




if __name__ == "__main__":
    root = tkinter.Tk()
    net_interface = GUI(root)
    root.mainloop()