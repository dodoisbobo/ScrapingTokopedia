# ScrapingTokopedia

You will need to have Selenium and Panda install in your python library

In the file Brick.py, you will need to change the PATH to your own chromedriver path

The duration of the scraping may vary. Sometimes the legit Tokopedia products link may return us a Non-Exist page and would not allow us to retrieve product details. This can be solve with refreshing the page. However, the Non-exist page may not be solve with only 1 time refresh, it may take several refresh.

Thus, in order to keep the robust of the program, I have set the refresh time to indefinite until it found the details that we need. Otherwise, you can undo the comments of code in Brick.py that will allow only refreshing the non-exist page to 5 times which will store the details if found and will default the details to "Product not found" if it did not found anything. I have pinpoint which chunk of code to undo for this. In doing this, we can also reduce the scraping amount of time by a lot.

At the end of the program, you will see the duration of the program and a CSV file in your folder which contains Brick.py
