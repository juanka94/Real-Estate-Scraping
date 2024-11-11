# Real Estate Scraping Project.

## Description.

### Objectives.
This project consists of a web scraping tool for a real estate site. The tool can extract the main characteristics of each real estate property listed on the website and then save them on a CSV for prior data analysis.
With this tool, we can obtain:
- The name by which you can find the property.
- Monthly leasing price.
- Number of rooms.
- Number of bathrooms.
- Number of toilets.
- Number of parking spaces.
- A description of the property given by the owner.
- Size of the property in square meters.

### Tools & Technologies.

- Python.
- Pandas.
- Request HTTP.
- BeautifulSoup4.

## How to use it?

1. Clone this repo on your computer (`git clone https://github.com/juanka94/Real-Estate-Scraping.git`).
2. Install the packages from requirements.txt (`pip install -r requirements.txt`).
3. Execute main.py (`python3 main.py`).
4. Voilà!! You will find the properties.csv inside the assets folder.

## Next Features.

- Be able to scrap all the pages of the site. (Currently, you can only scrap the first page).
- Be able to specify the state (province).
- Be able to scrap the properties on sale.
- Add a log to view warnings or errors that occur during web scraping.
