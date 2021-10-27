'''
                                                       Costly Item (Problem Statement)

While shopping online it can be seen that there are different price tag for the same item on different websites.
Help people to find the same product in less price to save money.

'''

#  Importing module    
#--------------------------------------------------------

from tkinter import *
from tkinter import Scrollbar
from bs4 import BeautifulSoup
import requests
import webbrowser
import pyttsx3


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

flipkart=''
amazon=''

###########################################################################
#                   Important function                                                                                                 #
###########################################################################

def say(s):
    engine = pyttsx3.init()
    engine.say(s)
    engine.setProperty("rate",178)
    engine.runAndWait()



# use to find most relevant items (Optimising the result)
def rele(main,search):
    relation = 0
    main = main.split()
    search = search.split()
    total =sum([x+1 for x in range(len(search))])
    for x in range(len(search)):
        if(search[x] in main):
            relation += (len(search)-x)/total
            main.remove(search[x])
    return relation
# use to convert currency
def convert(a):
    return int(float(a.replace(" ",'').replace("INR",'').replace(",",'').replace("₹",'')))

# use to extract product from flipkart
def flipkart(name = ""):
    try:
        global flipkart_url
        name1 = name.replace(" ","+")
        name=name.upper()#iphone x  -> iphone+x
        flipkart_url=f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off',headers=headers)

        soup = BeautifulSoup(res.text,'html.parser')
        score=0
        for x in range(len(soup.select('._4rR01T'))):
            flipkart_name=soup.select('._4rR01T')[x].getText().strip().upper()
            tempScore = rele(flipkart_name,name)
            if tempScore>score:
                score = tempScore
                flipkart_price = soup.select('._1_WHN1')[0].getText().strip()
            if(score==1):
                return f"{flipkart_name}\nPrise : {flipkart_price}\n"
        if(score==0):
            return '           Product Not Found'
    except :
        return "           Some Error"
    return f"{flipkart_name}\nPrise : {flipkart_price}\n"
# use to extract product from amazon
#enter amazon function

def urls():
    return f"{flipkart_url}\n\n\n{amazon_url}"

def open_url(event):
        global flipkart
        global amazon
        webbrowser.open_new(flipkart)
        webbrowser.open_new(amazon)

def search():
    
    box1.delete(1.0,"end")
    box4.delete(1.0,"end")
    box6.delete(1.0,"end")
    if(product_name_entry.get().split()!=[]):
        t1=flipkart(product_name_entry.get())

        box1.insert(1.0,t1)

        t4=amazon(product_name_entry.get())
        box4.insert(1.0,t4)

        t6 = urls()
        box6.insert(1.0,t6)
    else:
        box6.insert(1.0,'Please enter name of the product');
###########################################################################
#                   Creating GUI                                                                                                         #
###########################################################################
window = Tk()
window.wm_title("Web Scrapping Portal | Rahul")
window.minsize(1500,700)
window.config(background='#49A')
# lable
lable_one =  Label(window,relief=GROOVE, text="Enter Product Name ", font=("courier", 15))
lable_one.place(relx=0.2, rely=0.1, anchor="center")
# product name 
product_name =  StringVar()
product_name_entry =  Entry(window, textvariable=product_name, width=70)
product_name_entry.place(relx=0.5, rely=0.1, anchor="center")
# search Button
search_button =  Button(window,relief=GROOVE, text="Search", width=15, font=("courier", 15), command= search)
search_button.place(relx=0.5, rely=0.2, anchor="center")

# creating Label of boxes
flipkartLabel =  Label(window, relief=GROOVE,text="Flipkart", font=("courier", 15),bg='#49A')
amazonLabel =  Label(window,relief=GROOVE, text="Amazon", font=("courier", 15),bg='#49A')
resultLabel =  Label(window,relief=GROOVE, text="All URLs", font=("courier", 15),bg='#49A')
l8 =  Label(window, text="Loding.....", font=("courier", 30))

flipkartLabel.place(x=100,y=240)
amazonLabel.place(x=555,y=240);
#resultLabel.place(relx=0.8, rely=0.6, anchor="center")
resultLabel.place(x=1000,y=240)

# inserting scrollbar in boxes
scrollbar = Scrollbar(window)
box1 =  Text(window ,bd=7,relief=SUNKEN,height=15, width=50, yscrollcommand=scrollbar.set)
box4 =  Text(window,bd=7,relief=SUNKEN, height=15, width=50, yscrollcommand=scrollbar.set)

box1.place(x=100,y=310)
box4.place(x=550,y=310)

box6 =  Text(window,bd=7,relief=SUNKEN, height=15, width=50, yscrollcommand=scrollbar.set, fg="blue", cursor="hand2")
#box6.place(relx=0.8, rely=0.8, anchor="center")
box6.place(x=1000,y=310)
box6.bind("<Button-1>", open_url)
say("Welcome to Web scrapping portal")
window.mainloop()


