#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
import tkinter as tk                     
from tkinter import ttk 

#Connect database
import cx_Oracle
import oracledbconnect as dbconnect
connect=cx_Oracle.connect(dbconnect.user,dbconnect.password,dbconnect.dns)
cur=connect.cursor()


# In[2]:


window=tk.Tk()
window.geometry('1000x500')
window.title('PO Application')
tabControl=ttk.Notebook(window)
#define tabs
tab1=ttk.Frame(tabControl)
tab2=ttk.Frame(tabControl)
tab3=ttk.Frame(tabControl)

#add tab titles
tabControl.add(tab1,text="PO Enquiry")
tabControl.add(tab2,text="PO Header")
tabControl.add(tab3,text="PO Line")

#grid for tab
tabControl.grid()


# In[3]:


#Add widgets to tab1 PO Enquiry Tab
labelframe=tk.LabelFrame(tab1,text='Enter details to Enquire PO')
labelframe.grid(column=1,row=1)

tk.Label(labelframe,text='PO#').grid(column=0,row=1,sticky='E',pady=5)
ponum=tk.Entry(labelframe,width=10)
ponum.grid(column=1,row=1,pady=5)

tk.Label(labelframe,text='    ').grid(column=2,row=1,padx=50, pady=5)

tk.Label(labelframe,text='PO Date').grid(column=3,row=1,sticky='E',pady=5)
pondate=tk.Entry(labelframe,width=10)
pondate.grid(column=4,row=1,pady=5)

tk.Label(labelframe,text='Supplier#').grid(column=0,row=2,sticky='W',pady=5)
posuppnum=tk.Entry(labelframe,width=10)
posuppnum.grid(column=1,row=2,pady=5)

tk.Label(labelframe,text='    ').grid(column=2,row=2,padx=50, pady=5)

tk.Label(labelframe,text='Supplier Name').grid(column=3,row=2,sticky='W',pady=5)
posupname=tk.Entry(labelframe,width=10)
posupname.grid(column=4,row=2,pady=5)


# In[ ]:


window.mainloop()

