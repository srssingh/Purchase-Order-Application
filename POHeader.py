#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
import tkinter as tk                     
from tkinter import ttk
from tkinter import scrolledtext
from datetime import date

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

tk.Label(labelframe,text='*PO#').grid(column=0,row=1,sticky='E',pady=5)
ponum=tk.Entry(labelframe,width=10)
ponum.grid(column=1,row=1,pady=5)

tk.Label(labelframe,text='    ').grid(column=2,row=1,padx=50, pady=5)

tk.Label(labelframe,text='PO Date').grid(column=3,row=1,sticky='E',pady=5)
pondate=tk.Entry(labelframe,width=10)
pondate.grid(column=4,row=1,pady=5)

tk.Label(labelframe,text='Supplier#').grid(column=0,row=2,sticky='W',pady=5)
posuppnum=tk.Entry(labelframe,width=10)
posuppnum.grid(column=1,row=2,pady=5,padx=15)

tk.Label(labelframe,text='    ').grid(column=2,row=2,padx=50, pady=5)

tk.Label(labelframe,text='Supplier Name').grid(column=3,row=2,sticky='W',pady=5)
posupname=tk.Entry(labelframe,width=10)
posupname.grid(column=4,row=2,pady=5,padx=15)


# In[4]:


def readfromdatabase():
    cur.prepare(""" 
               SELECT SUPPLIERNUM,
               SUPPLIERNAME,
               PONUM,
               PAYTERM,
               POLINENUM,
               POITEMNUM,
               POLINEDESCRIPTION,
               POLINEUNITPRICE,
               QTY,
               POLINEAMT,
               ADDRESSLINE1,
               ADDRESSLINE2,
               CITY,
               PROVINCE,
               COUNTRY
               FROM SANRUSHA_PO_DETAILS_V
               WHERE PONUM=:ponumquery
               AND TO_CHAR(PO_DATE,'DD-MON-YY')=NVL(TO_CHAR(:podatequery,'DD-MON-YY'),TO_CHAR(PO_DATE,'DD-MON-YY'))
               AND suppliernum=NVL(:posuppnumquery,suppliernum)
               AND suppliername=NVL(:posupnamequery,suppliername)
                """)
    cur.execute(None,ponumquery=ponum.get(),podatequery=pondate.get(),posuppnumquery=posuppnum.get(),posupnamequery=posupname.get())
    return cur.fetchall()
    


# In[5]:


def showallrecords():
    data=readfromdatabase()
    labelframe2 = tk.LabelFrame(tab1, text="Enquiry Result")
    labelframe2.grid(column=1,row=2)
    tk.Label(labelframe2,text='Supp#'+'|   '+'Supplier Name                  '+'|   '+'PO#   '+'|   '+'Pay Term'+'|   '+'PO Line#'+'|   '+'PO Item#'+'|   '+'PO Line Description'+'|   '+'Unit Price'+'|   '+'Qty'+'|   '+'Amount').grid(column=0,row=2)
    
    for index, dat in enumerate(data):
        try:
            tk.Label(labelframe2,text=dat[0]+'|   '+dat[1]+'|   '+dat[2]+'|   '+dat[3]+'|   '+str(dat[4])+'|   '+dat[5]+'|   '+dat[6]+'|   '+str(dat[7])+'|   '+str(dat[8])+'|   '+str(dat[9])).grid(column=0,row=index+6)
        except:
            tk.Label(labelframe2,text='Exception').grid(column=0,row=6)


# In[6]:


enqbt=tk.Button(labelframe,text='Enquire', command=showallrecords)
enqbt.grid(column=1,row=3, columnspan=3)


# In[7]:


#Create Frames in PO Header
lframepoh=tk.LabelFrame(tab2,text='Enter PO Header Details ')
lframepoh.grid(column=1,row=1)


# In[8]:


#Add widgets to lframepoh frame in PO Header Tab

tk.Label(lframepoh,text='PO#').grid(column=0,row=1,sticky='E',pady=5)
ponumpoh=tk.Entry(lframepoh,width=20)
ponumpoh.grid(column=1,row=1,padx=15,pady=5,sticky='W')

tk.Label(lframepoh,text='    ').grid(column=2,row=1,padx=50, pady=5)

tk.Label(lframepoh,text='Supplier#').grid(column=0,row=2,sticky='E',pady=5)
posuppnumpoh=tk.Entry(lframepoh,width=20)
posuppnumpoh.grid(column=1,row=2,pady=5,padx=15,sticky='W')

#+Delivery Address
lframepodeladd=tk.LabelFrame(lframepoh,text='Delivery Address ',pady=5,padx=15)
lframepodeladd.grid(column=1,row=3)

tk.Label(lframepodeladd,text='Address Line1').grid(column=0,row=1,sticky='E',pady=1)
pohaddl1=tk.Entry(lframepodeladd,width=20)
pohaddl1.grid(column=1,row=1,pady=1,padx=15,sticky='W')

tk.Label(lframepodeladd,text='Address Line2').grid(column=0,row=2,sticky='E',pady=1)
pohaddl2=tk.Entry(lframepodeladd,width=20)
pohaddl2.grid(column=1,row=2,pady=1,padx=15,sticky='W')

tk.Label(lframepodeladd,text='Province').grid(column=0,row=3,sticky='E',pady=1)
pohaddlprov=tk.Entry(lframepodeladd,width=20)
pohaddlprov.grid(column=1,row=3,pady=1,padx=15,sticky='W')

tk.Label(lframepodeladd,text='City').grid(column=0,row=4,sticky='E',pady=1)
pohaddlpcity=tk.Entry(lframepodeladd,width=20)
pohaddlpcity.grid(column=1,row=4,pady=1,padx=15,sticky='W')

tk.Label(lframepodeladd,text='Country').grid(column=0,row=5,sticky='E',pady=1)
pohaddlpcountry=tk.Entry(lframepodeladd,width=20)
pohaddlpcountry.grid(column=1,row=5,pady=1,padx=15,sticky='W')

#-Delivery Address

tk.Label(lframepoh,text='PO Date').grid(column=3,row=1,sticky='E',pady=5)
podatepoh=tk.Entry(lframepoh,width=20)
podatepoh.grid(column=4,row=1,pady=5,padx=15,sticky='W')

tk.Label(lframepoh,text='    ').grid(column=2,row=2,padx=50, pady=5)

tk.Label(lframepoh,text='Supplier Name').grid(column=3,row=2,sticky='E',pady=5)
posupnamepoh=tk.Entry(lframepoh,width=20)
posupnamepoh.grid(column=4,row=2,pady=5,padx=15,sticky='W')


#+Supplier Address
lframeposuppadd=tk.LabelFrame(lframepoh,text='Supplier Address ',pady=1,padx=15)
lframeposuppadd.grid(column=4,row=3)

tk.Label(lframeposuppadd,text='Address Line1').grid(column=0,row=1,sticky='E',pady=1)
pohadds1=tk.Entry(lframeposuppadd,width=20)
pohadds1.grid(column=1,row=1,pady=1,padx=15,sticky='W')

tk.Label(lframeposuppadd,text='Address Line2').grid(column=0,row=2,sticky='E',pady=1)
pohadds2=tk.Entry(lframeposuppadd,width=20)
pohadds2.grid(column=1,row=2,pady=1,padx=15,sticky='W')

tk.Label(lframeposuppadd,text='Province').grid(column=0,row=3,sticky='E',pady=1)
pohaddsprov=tk.Entry(lframeposuppadd,width=20)
pohaddsprov.grid(column=1,row=3,pady=1,padx=15,sticky='W')

tk.Label(lframeposuppadd,text='City').grid(column=0,row=4,sticky='E',pady=1)
pohaddspcity=tk.Entry(lframeposuppadd,width=20)
pohaddspcity.grid(column=1,row=4,pady=1,padx=15,sticky='W')

tk.Label(lframeposuppadd,text='Country').grid(column=0,row=5,sticky='E',pady=1)
pohaddspcountry=tk.Entry(lframeposuppadd,width=20)
pohaddspcountry.grid(column=1,row=5,pady=1,padx=15,sticky='W')
#-Supplier Address


# In[9]:


def suppval():
    cur.prepare(""" 
               SELECT SUPPLIERID
               FROM SANRUSHA_SUPPLIERS
               WHERE SUPPLIERNUM=:pohsuppnum
               AND SUPPLIERNAME=:pohsuppname
                """)
    cur.execute(None,pohsuppnum=posuppnumpoh.get(),pohsuppname=posupnamepoh.get())
    suppdata=cur.fetchall()
    if cur.rowcount==0:
        return 0
    else:
        return suppdata


# In[10]:


def deladdval():
    cur.prepare(""" 
               SELECT DELVSITEID               
               FROM SANRUSHA_DELIVERY_SITES
               WHERE UPPER(ADDRESSLINE1)=UPPER(:pohaddressl1)
               AND UPPER(ADDRESSLINE2)=NVL(UPPER(:pohaddressl2),UPPER(ADDRESSLINE2))
               AND UPPER(CITY)=UPPER(:pohaddresspcity)
               AND UPPER(PROVINCE)=UPPER(:pohaddresssprov)
               AND UPPER(COUNTRY)=UPPER(:pohaddresspcountry)
               AND PURPOSE='WAREHOUSE'
               AND ROWNUM=1
                """)
    cur.execute(None,pohaddressl1=pohaddl1.get(),pohaddressl2=pohaddl2.get(),pohaddresspcity=pohaddlpcity.get(),pohaddresssprov=pohaddlprov.get(),pohaddresspcountry=pohaddlpcountry.get())
    deldata=cur.fetchall()
    if cur.rowcount==0:
        return 0
    else:
        return deldata


# In[11]:


def poheaderid():
    cur.execute("""SELECT SANRUSHA_PO_HEADER_S.nextval FROM DUAL""")
    pohid=cur.fetchone()
    return pohid


# In[12]:


def pohvalinsert():
 
    labelpohvalframe2 = tk.LabelFrame(tab2, text='Validation Result')
    labelpohvalframe2.grid_forget()
    labelpohvalframe2.grid(column=1,row=2)
    #tk.Label(labelpohvalframe2,text='Hello there').grid(column=0,row=0)
    pohsuppval=suppval()
    pohdeladdval=deladdval()
    poheadseq=poheaderid()
    
    #tk.Label(labelpohvalframe2,text=f'PO Header id {poheadseq[0]}').grid(column=0,row=0)
    
    if not ponumpoh.get():
        tk.Label(labelpohvalframe2,text=f'PO number is required').grid(column=1,row=0)

    if pohsuppval==0:
        tk.Label(labelpohvalframe2,text=f'Invalid Supplier').grid(column=1,row=1)
    else:
        tk.Label(labelpohvalframe2,text=f'Supplier# {posuppnumpoh.get()} Supplier Name {posupnamepoh.get()} ').grid(column=1,row=1)
        tk.Label(labelpohvalframe2,text=f'Valid Supplier details count {len(pohsuppval)}').grid(column=1,row=2)
        tk.Label(labelpohvalframe2,text=f'Supplier id {pohsuppval[0][0]}').grid(column=1,row=3)
    
    if pohdeladdval==0:
        tk.Label(labelpohvalframe2,text=f'Delivery adress is missing or wrong').grid(column=1,row=4)
    else:
        tk.Label(labelpohvalframe2,text=f'Delivery address1 {pohaddl1.get()} city {pohaddlpcity.get()} ').grid(column=1,row=5)
        tk.Label(labelpohvalframe2,text=f'Valid delivery address count {len(pohdeladdval)}').grid(column=1,row=4)
        tk.Label(labelpohvalframe2,text=f'Delivery Site id {pohdeladdval[0][0]}').grid(column=1,row=6)
         
            
    if pohsuppval != 0 and pohdeladdval !=0 and ponumpoh.get():
        try:
            #records=[poheadseq,ponumpoh.get(),podatepoh.get(),pohsuppval[0][0],pohdeladdval[0][0],pohdeladdval[0][0]]
            tk.Label(labelpohvalframe2,text=f'Inserting PO header').grid(column=1,row=7)
            cur.execute("""INSERT INTO SANRUSHA_PO_HEADER (POHEADERID, PONUM, PO_DATE, SUPPLIERID, SHIPTOSITEID, BILLTOSITEID,PAYTERM,CREATIONDATE,UPDATEDATE) 
            VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9)""",[poheadseq[0],ponumpoh.get(),podatepoh.get(),pohsuppval[0][0],pohdeladdval[0][0],pohdeladdval[0][0],'NET30',date.today(),date.today()])
            connect.commit()
            tk.Label(labelpohvalframe2,text=f'Successfully inserted PO header').grid(column=1,row=8)
        except Exception as e:
            tk.Label(labelpohvalframe2,text=f' Exception {format(e)}').grid(column=1,row=8)
            
    
    for error in cur.getbatcherrors():
         tk.Label(labelpohvalframe2,text=f'Error in inserting {error.message.rstrip()} at row {error.offset}').grid(column=1,row=9)


# In[13]:


pohbt=tk.Button(lframepoh,text='Submit', command=pohvalinsert)
pohbt.grid(column=2,row=4)


# In[14]:


window.mainloop()

