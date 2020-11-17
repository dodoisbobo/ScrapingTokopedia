from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import pandas as pd

#use the chromedriveer to open or access websites
PATH = "C:\Program Files (x86)\chromedriver.exe"
#use the driver library of chrome
driver = webdriver.Chrome(PATH)

def allLinks():
    #boolean for while loop
    listCounter=True
    #access the tokopedia handphone category page
    driver.get("https://www.tokopedia.com/p/handphone-tablet/handphone")
    #allow driver to scroll to given height of the page
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    #allow wait duration for the page to load everything
    time.sleep(3)
    #list to store 100 product that is available in the product list
    contentLinks=[]
    
    while listCounter:
        #List of each products link in the product list page
        item = driver.find_elements_by_xpath(".//div[@class='css-bk6tzz e1nlzfl3']")
        #access each element in list
        for itemList in item:
            #within the web page, look for tag <a>
            itemA = itemList.find_element_by_tag_name('a')
            #condition to append only 100 list of product into the list
            if(len(contentLinks) == 100):
                #set counter to false to exit while loop
                listCounter=False
                #make sure for loop is exited
                break
            else:
                contentLinks.append(itemA.get_property('href'))
        try:
            #click next page of the product list page, so that we can access more products
            nextPage = driver.find_element_by_xpath(".//button[@aria-label='Halaman berikutnya']")
            #execute javascript script to click on the available button
            driver.execute_script("arguments[0].click();",nextPage)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)
        except:
            #set counter to false to exit while loop
            listCounter=False
    return contentLinks
    
def collect(list):
    #list to store all products and their details
    allData=[]
    #counter
    count=1
    #access all product links
    for i in range (len(list)):
        #variable to check for a condition when tokopedia is accessed with legit link but return non-exist page
        error = ""
        #counter condition
        exist=False
        time.sleep(3)
        try:
            #set load timeout for pages taking more than 15s to load
            driver.set_page_load_timeout(15)
            #access the links
            driver.get(list[i])
        except TimeoutException:
            #when a timeout happen, refresh the page 1 time
            driver.refresh()
        #perform double scrolling, because tokopedia website need to scroll in order to get some elements
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(12)
        try:
            #this is element that only appears when a legit link is accessed, however tokopedia return a non-exist page
            error = driver.find_element_by_xpath(".//div[@class='css-p1erks-unf-emptystate e1lf3yex0']")
        except NoSuchElementException:
            #Only when the page is correct and contains all the product detials then do this
            try:
                #get product name text
                name = driver.find_element_by_xpath(".//h1[@class='css-x7lc0h']").text
            except NoSuchElementException:
                name ="HandPhone"
            try:
                #get product description text
                des = driver.find_element_by_xpath(".//p[@class='css-olztn6-unf-heading e1qvo2ff8']").text
            except NoSuchElementException:
                des ="No description"
            try:
                #get image link
                image = driver.find_element_by_xpath(".//img[@class='success fade']").get_property('src')
            except NoSuchElementException:
                image ="No Image"
            try:
                #get price text
                price = driver.find_element_by_xpath(".//h3[@class='css-c820vl']").text
            except NoSuchElementException:
                price = "No Price"
            try:
                #get rate text
                rate = driver.find_element_by_xpath(".//span[@data-testid='lblPDPDetailProductRatingNumber']").text
            except NoSuchElementException:
                rate = "No rate"
        #This condition will do an indefinite amount of refresh when we are accessing legit link but tokopedia return us non-exist page
        #which will cost a lot amount of time
        if(error != ""):
            while(exist==False):
                driver.refresh()
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(3)
                try:
                    #this is element that only appears when a legit link is accessed, however tokopedia return a non-exist page
                    error = driver.find_element_by_xpath(".//div[@class='css-p1erks-unf-emptystate e1lf3yex0']")
                except NoSuchElementException:
                    exist = True
                    try:
                        name = driver.find_element_by_xpath(".//h1[@class='css-x7lc0h']").text
                    except NoSuchElementException:
                        name ="HandPhone"
                    try:
                        des = driver.find_element_by_xpath(".//p[@class='css-olztn6-unf-heading e1qvo2ff8']").text
                    except NoSuchElementException:
                        des ="No description"
                    try:
                        image = driver.find_element_by_xpath(".//img[@class='success fade']").get_property('src')
                    except NoSuchElementException:
                        image ="No Image"
                    try:
                        price = driver.find_element_by_xpath(".//h3[@class='css-c820vl']").text
                    except NoSuchElementException:
                        price = "No Price"
                    try:
                        rate = driver.find_element_by_xpath(".//span[@data-testid='lblPDPDetailProductRatingNumber']").text
                    except NoSuchElementException:
                        rate = "No rate"
                        
                
                #The code below is to change refreshing indefinitely to max 5 time and set all details to not found
                #The purpose of this is to greatly reduce amount of time of the scraping
                #UNDO THIS CODE IF YOU NEED
                # count+=1
                # if(count == 5):
                    # exist =True
                    # name = "Product not found"
                    # des = "Product not found"
                    # image = "Product not found"
                    # price = "Product not found"
                    # rate = "Product not found"
                    
        #dictionary to store all the product details so that we can build a dataframe   
        dict = {
            'Name':name,
            'Description':des,
            'Image':image,
            'Price':price,
            'Rating':rate
        }
        #append all the product details to the list
        allData.append(dict)
    
    #create a dataframe
    data = pd.DataFrame(allData)
    #write the dataframe into csv file
    data.to_csv('All-Data.csv')
#start time for the program
start=time.time()
#function to gather all the links
a = allLinks()
#collect and store all product details
collect(a)
#elapsed time of the program
e = time.time() - start
#print the duration of the program
print("%02d:%02d:%02d" % (e//3600, (e%3600//60), (e%60//1)))