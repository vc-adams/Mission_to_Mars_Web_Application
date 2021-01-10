import warnings
import pymongo
import time
import datetime
import requests
import datefinder
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as BS


# identify location of chromedriver and store it as a variable
# chromedriver = !which chromedriver
# print(type(chromedriver))
# chromedriver[0]


# Step 1 - Scraping

def scrape():
    # ======================================================================================================
    # ========================================= 1.1 NASA Mars News =========================================
    # ======================================================================================================

    # 1.1.1 Retrieve the data/information on NASA's Mars website

    # Retrieve page with the requests module
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    window = browser.windows.current

    # Allow the page to complete load before scrapping the page.
    # Reference:
    # https: // splinter.readthedocs.io/en/latest/api/driver-and-element-api.html
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = BS(html, "html.parser")
    # time.sleep(3)

    # 1.1.2 Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News
    # Title and Paragraph Text. Assign the text to variables that you can reference later.

    # 1.1.2.1 Determine Which News Title and its Corresponding Paragraph is the most recent

    # 1.1.2.1.1 Collect the div Tags with a class = content_title, class = content_title corresponds
    # all the News Articles on the NASA Mars Exploration Program Webpage

    # Collect all the div tags with a class = content_title
    # References:
    #   https://stackoverflow.com/questions/1058599/how-to-get-a-nested-element-in-beautiful-soup
    #   https://stackoverflow.com/questions/46510966/beautiful-soup-nested-tag-search
    div_tags_class_content_title = [
        div.get_text(separator=';') for div in news_soup.body.find_all("div", class_="list_text")]
    # This will print to the terminal/bash window where the flask app is running.
    # print(div_tags_class_content_title)

    # Get the dates within the div_tags_class_content_title for each News Article
    # Reference:
    #     https://datefinder.readthedocs.io/en/latest/
    index_no = 0
    dates_in_class_list_text = []

    for div_tag in div_tags_class_content_title:
        dates_in_class_list_text.append(list(datefinder.find_dates(div_tag)))

    # 1.1.2.1.2 Determine the Most Recent Date
    # Loop through the first column in dates_in_class_list_text and determine which is the most recent date.
    # References:
    #     https://docs.python.org/3/library/datetime.html

    # start_date_str is the oldest date that Python's datetime library will recognize.
    start_date_str = "January 01, 0001"
    start_date_obj = datetime.datetime.strptime(start_date_str, '%B %d, %Y')

    index_no = 0
    latest_date_index = 0

    for dates in dates_in_class_list_text:
        count = 0

        for date in dates:

            if count <= 0:
                count = count + 1

                if date > start_date_obj:
                    start_date_obj = date
                    latest_date = date
                    latest_date_index = index_no

        index_no = index_no + 1

    # try:
    # 1.1.2.2 Collect the latest News Title and Corresponding Paragraph Text
    latest_news_date = div_tags_class_content_title[latest_date_index].split(";")[
        0]
    latest_news_title = div_tags_class_content_title[latest_date_index].split(";")[
        1]
    latest_news_paragragh = div_tags_class_content_title[latest_date_index].split(";")[
        2]
    # except Exception:
    #     pass

    # ======================================================================================================
    # ============================= 1.2 JPL Mars Space Images - Featured Image =============================
    # ======================================================================================================

    # URL of page to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup_mars_featured_image = BS(html, "html.parser")

    # 1.2.2 Collect the a tag for the current Featured Mars Image and its url
    # Collect all the div tags with a class = img
    div_tags_class_img = soup_mars_featured_image.body.find_all(
        "a", class_="button fancybox")

    # Use splinter to click through the website
    # https://splinter.readthedocs.io/en/latest/api/driver-and-element-api.html

    # Click FULL IMAGE to see a large thumbnail of the featured image
    browser.click_link_by_partial_text('FULL IMAGE')

    # # Click more info to go to the webpage for the featured image
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    # # Click the featured image for the large image
    time.sleep(2)
    browser.click_link_by_partial_href('.jpg')

    # Search for all the img tags
    large_img = browser.find_by_tag("img")

    # Save the img tag to the featured_img_url variable
    for img in large_img:
        featured_img_url = img._element.get_attribute('src')
        print(featured_img_url)

    # ======================================================================================================
    # =========================================== 1.3 Mars Facts ===========================================
    # ======================================================================================================

    # 1.3.1 Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to scrape the table containing facts about Mars
    mars_facts_tables = pd.read_html('https://space-facts.com/mars/')

    # Save the desired table, which is a dataframe, to a variable
    mars_facts_table_df = mars_facts_tables[0]
    mars_facts_table_df.columns = ['', 'Mars']
    mars_facts_table_df = mars_facts_table_df.set_index("")
    mars_facts_table_df.columns = ['Mars']

    # 1.3.2 Use Pandas to convert the data to a HTML table string.
    # Convert the Dataframe Table back into a html table string
    mars_facts_table_html = mars_facts_table_df.to_html()

    # ======================================================================================================
    # ========================================= 1.4 Mars Hemispheres =======================================
    # ======================================================================================================

    # URL of page to be scraped
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    window = browser.windows.current

    html = browser.html
    soup_mars_hemispheres = BS(html, "html.parser")

    # 1.4.1 You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Use splinter to click through the website
    # https://stackoverflow.com/questions/45364497/cannot-chain-find-and-find-all-in-beautifulsoup
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attributes

    # Click FULL IMAGE to see a large thumbnail of the featured image
    mars_hemispheres = soup_mars_hemispheres.find_all("div", class_="item")

    # Save the img tag to the featured_img_url variable

    # References
    # - Find And Replace | Python String:
    #     - https://www.geeksforgeeks.org/python-string-replace/
    # - Ignore Future Warning Message:
    #     - https://stackoverflow.com/questions/57704412/how-to-suppress-future-warning-tensorflow
    # - Splinter Broswer Documentation
    #     - https://splinter.readthedocs.io/en/latest/browser.html#managing-windows
    # - Splinter Finding Documentation
    #     - https://splinter.readthedocs.io/en/latest/finding.html
    # - Dictionaries:
    #     - https://www.geeksforgeeks.org/add-a-keyvalue-pair-to-dictionary-in-python/
    #     - https://www.kite.com/python/answers/how-to-append-a-value-to-an-empty-dictionary-in-python

    # # Save the img tag to the featured_img_url variable
    # mars_hemispheres = soup.find_all("div", class_ = "item")
    # print(len(mars_hemispheres))
    # print(mars_hemispheres[0])
    # print("************************************************************")
    # print("************************************************************")
    warnings.filterwarnings("ignore", message=r"browse",
                            category=FutureWarning)

    planets_mars_scraped_data_list_tuples = []
    index = 1

    h3_mars_hemispheres = soup_mars_hemispheres.find_all("h3")
    for hemisphere in range(len(h3_mars_hemispheres)):
        #     print(len(h3_mars_hemispheres))
        mars_hemisphere_name = h3_mars_hemispheres[hemisphere].string.replace(
            "<h3>", "")
        # print(mars_hemisphere_name)

        browser.windows.current = browser.windows[0]
        time.sleep(1)
        browser.click_link_by_partial_text(mars_hemisphere_name)
        time.sleep(1)
        browser.click_link_by_text("Sample")
        browser.windows.current = browser.windows[1]
        mars_hemisphere_url = browser.find_by_tag("img")["src"]
        # print(mars_hemisphere_url)

        hemisphere_name_index = "hemisphere_name_" + str(index)
        hemisphere_url_index = "hemisphere_url_" + str(index)

        # Individual Hemisphere List of Tuples
        hemisphere_title_and_image_url_list_tuples = [
            (hemisphere_name_index, mars_hemisphere_name), (hemisphere_url_index, mars_hemisphere_url)]

        # Hemisphere List
        planets_mars_scraped_data_list_tuples.extend(
            hemisphere_title_and_image_url_list_tuples)

        print(planets_mars_scraped_data_list_tuples)

        # Index Counter for the Hemishpheres
        index = index + 1

        time.sleep(1)
        browser.windows[1].close()
        browser.back()

    # Close the Current Window

    # References:
    #     https://docs.python.org/3/tutorial/errors.html
    #     https://stackoverflow.com/questions/574730/python-how-to-ignore-an-exception-and-proceed
    try:
        window.close()
    except Exception:
        pass

    # ======================================================================================================
    # ================================== 2.0 MongoDB and Flask Application =================================
    # ======================================================================================================

    # 2.1 Store the return value in Mongo as a Python dictionary.
    # Store the return value in Mongo as a Python dictionary.
    # mars_scraped_data_list_tuples = []
    mars_scraped_data_list_tuples = [("planet_name", "Mars"), ("latest_news_date", latest_news_date), ("latest_news_title", latest_news_title), (
        "latest_news_paragraph", latest_news_paragragh), ("featured_image_url", featured_img_url), ("facts_table_html", mars_facts_table_html)]

    planets_mars_scraped_data_list_tuples.extend(mars_scraped_data_list_tuples)

    # planets_mars_scraped_data_list_tuples
    planets_mars_scraped_data_dic = dict(planets_mars_scraped_data_list_tuples)

    return planets_mars_scraped_data_dic
