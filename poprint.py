#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import cx_Oracle
import oracledbconnect as dbconnect


# In[2]:


connect=cx_Oracle.connect(dbconnect.user,dbconnect.password,dbconnect.dns)


# In[3]:


cursors=connect.cursor()
cursors.execute("""SELECT UNIQUE SUPPLIERNUM,SUPPLIERNAME,PONUM,PO_DATE,PAYTERM,ADDRESSLINE1,ADDRESSLINE2,CITY,PROVINCE,COUNTRY FROM SANRUSHA_PO_DETAILS_V""")
poh=cursors.fetchall()
cursors.close()


# In[4]:


cursor2=connect.cursor()
cursor2.prepare("""SELECT *FROM SANRUSHA_PO_DETAILS_V WHERE PONUM=:INPONUM""")


# In[5]:


logo ="sanrusha.png"


# In[6]:


for i in range(len(poh)):
    poi=poh[i][2]
    podocname=poh[i][0]+'-'+poh[i][2]+'-'+str(datetime.datetime.now().strftime('%Y%m%d'))
    print(podocname)
    doc = SimpleDocTemplate(podocname+".pdf", pagesize=letter,rightMargin=72,leftMargin=72,
                        topMargin=32,bottomMargin=18)
    Story=[]
    
    #Logo
    im = Image(logo)
    im.hAlign='RIGHT'
    Story.append(im)
    
    #Document Style
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
    #Date Time stamp
    ponum='PO Number: '+poh[i][2]
    podate='PO Date: '+str(poh[i][3])
    poterm="Payment Term: "+str(poh[i][4])
    Story.append(Paragraph(ponum, styles["Normal"]))
    Story.append(Paragraph(podate, styles["Normal"]))
    Story.append(Paragraph(poterm, styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    #Delivery Address
    addrpur = ['Ship To:','','','Bill To:']
    addr1 = [poh[i][1],'','',poh[i][1]]
    addr2 = [poh[i][5],'','',poh[i][5]]
    addrcity = [poh[i][6],'','',poh[i][6]]
    addrstate = [poh[i][7],'','',poh[i][7]]
    addrcntr = [poh[i][8],'','',poh[i][8]]
    
    addr=[addrpur,addr1,addr2,addrcity,addrstate,addrcntr]
    adt=Table(addr)
    adt._argW[1]=1.5*inch
    adt._argW[3]=1.7*inch
    adt.hAlign='LEFT'
    
    Story.append(adt)
    Story.append(Spacer(1, 12))
    Story.append(Spacer(1, 12))
    
    #print(addr)
    
    #PO Line
    cursor2.execute(None,INPONUM=poh[i][2])
    pol=cursor2.fetchall()
    polintitle=[["Line#","Item","Description","Unit Price","Qty","Amount"]]
    polintab2=[]
    total=0
    for j in range(len(pol)):
        polin=str(pol[j][5])
        poitem=str(pol[j][6])
        poitemdesc=str(pol[j][7])
        pounitpr=str(pol[j][8])
        poqty=str(pol[j][9])
        pohamt=str(pol[j][10])
        
        
        polintab1=[[polin,poitem,poitemdesc,pounitpr,poqty,pohamt]]
        polintab2=polintab2+polintab1;
        total=total+pol[j][10]
        #if j==0:
         #   polintab=polintitle+polintab1
        #else:
         #   polintab=polintab+polintab1
    polintab3=[['','','','','Total Amt:',total]]
    polintab=polintitle+polintab2+polintab3
    #polintab[-1][5]=total
    
    t=Table(polintab,style=[
    ('GRID',(0,0),(-1,-1),1,colors.black),
    ('BOX',(0,0),(-1,-1),1,colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
    ('ALIGN',(0,0),(-1,0),'CENTER'),
    ('ALIGN',(3,0),(5,-1),'RIGHT'),
    ('GRID',(0,-1),(-2,-1),1,colors.white),
    ('GRID',(0,0),(-2,-2),1,colors.black),
    ('BOX',(-2,-2),(-1,-1),1,colors.black),
    ('GRID',(-2,-2),(-1,-1),1,colors.black)
    ])
        
    t._argW[2]=2.5*inch
    t._argW[3]=1*inch
    t._argW[4]=0.75*inch
    t._argW[5]=1*inch
    t.hAlign = 'LEFT'
        
    Story.append(t)
    Story.append(Spacer(1, 12))
    
    
    doc.build(Story)


# In[7]:


cursor2.close()

