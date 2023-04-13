
# ESG Hub
### Description:
ESG Hub is a web application in which you can search ESG data from different data providers. It also provides a detailed chart view of the different topics of ESG and basic financial and market data, too.

### Languanges and frameworks:
* Python
* Django
* SQLite
* HTML
* CSS
* Javascript
* Bootstrap

### Distinctiveness and Complexity:
The django project and app was made exclusively for this project and was not copied from a previous project. I wanted to make the whole project as a new, so I had to configure the django the way my project required. I considered and tried the use of websockets with django channels and daphne, but I decided to stick with the traditional http requests for this project because the content of the site not necessarily need that real-time experience that websocket can offer. I used pure CSS+Javascript to make the ESG data gauge updated accordingly. The gauge changes rotation angle and color as well. For the detailed mixed chart, I used a js library (Charts.js). The data are exchanged in JSON packages with a lot of information which I had to extract from the JSON package to process. Frontend uses the Bootstrap grid system. It also contains an embedded video from Youtube (on the What is ESG? site). The search bar gives you automatic result suggestions after you type in at least 3 letters. One of the databases contains almost 6000 entries which is way more than anything in previous projects. It contains a list of companies with IDs. It was tricky to upload this amount of data and needed to use the django built-in bulk_create function for this with a specific batch size (the upload was not made with a plain iteration one-by-one). The application uses multiple API calls to provide data to the frontend. The ESG data comes from ESG Analytics based on their database (more on this in the hint section). And the financial and market data comes from Alpha Vantage API. Both are free APIs with limited usage possible. So I had to overcome this with data caching in the database (please find more information below). The detailed ESG database can be get through an http get request.


### Walkthrough of usage:
You start your journey on the main, landing page. It has a header with a navbar and a footer with information. The home button takes you back here. The What is ESG? button goes to a short information page where you can learn about ESG and also view an embedded video about it.

If you would like to search for a company, you need to type in the name of the company (not the symbol or ticker). After 3 letters the system will give you suggestions about the possible companies. You can click one of them or use arrow keys to navigate through the list and select one with enter. After clicking the search button (or hitting enter again) the site will grab all the information about that company and redirect you to the result page.

On the result page, you can see the name and symbol of the company with basic financial data (last day closing share price along with the price change that occurred on that particular day) and data about the market capitalization of the company in billion USD. Under these, you see the ESG rating of MSCI and S&P data providers. Each uses a different approach to evaluate a company, so it is possible that the two data alter. If no data is available for the company then you NA. Below you can see a detailed bar + line chart where you can compare the performance of the company with the industry average. There are a lot of different topics which are on the x-axis.

If you would like to search for another company, you do not have to go back to the home page, you can simply use the search bar on this page the same as before. Hit enter to search.

### HINTS FOR USAGE:
The ESG data come from ESG Analytics (esganalytics.io) which provides free API for the data. This free API is very limited, it is allowed to have only 20 calls in a month. That is why I made the databases that way it saves the new searches (it is basically a cache). So you can use the search on the cached companies which will not make an API call to ESG Analytics to save the calls. So please search firstly these companies, the software will provide you data directly from the cache:

- Apple Inc
- Tesla Inc
- Netflix Inc
- BlackRock Inc
- Ford Motor Company
- Morgan Stanley
- Morning Star Inc
- MSCI Inc

The stock price and financial data come from Alpha Vantage. This is also a free API with limitations. It can handle 5 calls every minute and 500 calls in a month in total.

**Notes**
- Note that the data of ESG Analytics are sometimes outdated and not in sync with the original data source (MSCI or S&P).
- Note that the database (the list of companies) of the two API providers are not in sync.
- If you reach these limitations or other unexpected error happens, the site will show you an alert.

In a real-world application, I would choose a more reliable source of ESG data (for example directly from MSCI), but it is barely available for an individual person. Or another approach would be to build a proper database of companies and ESG data.

### Files:
##### mysite folder
settings.py contains the settings of the project, including installed apps, CSRF_TRUSTED_ORIGIN which are needed to be able to use django admin site.

urls.py contains all the urls, including the home ursl.py

##### home folder
The **static folder** is where the CSS, Javascript, and media files live. I made 3 separate JS files for the different view/HTML render. The name contains the script prefix and the name of the HTML file afterward to distinguish them. Since there are not that many files and media here I did not make different folders for them, but in a real-world application it is recommended. I left the stock.csv file here. The content of this csv was uploaded into a django model called Database. The code for uploading this csv is commented out in the views.py 'query' function.

The **template folder** where the html files live. The layout contains the skeleton of the site with a header, footer, and body. It is extended later with the 3 different views. The index is for the landing page, the result is for displaying the result of the query (ESG and financial data). The what_is_esg is a short information site about ESG.

**root**
admin.py includes the models for modification and supervision.

models.py contains 3 models (Datababse, DataDetails, DataExt). The database contains almost 6000 entries, it is a list with company names and IDs. It provides information for automatic search result suggestions for the user. The other two databases (DataDetails and DataExt) are only for storing the previously searched companies' ESG data for caching purposes. (more on this below).

views.py where all the html rendering, data processing, database queries, and API calls are managed.






