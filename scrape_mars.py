# Step 2- MongoDB and Flask Application

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt


# Convert Jupyter NB into Python Script
def scrape_all():

    # Import Splinter and set the chromedriver path
    from webdriver_manager.chrome import ChromeDriverManager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Save NASA MARS URL and visit the page
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the latest news title and article
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Save FEATURED SPACE IMAGE URL and visit the page
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Design an XPATH selector to grab the featured image
    xpath = '/html/body/div[1]/img'

    # Use splinter to Click the featured image 
    # to bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, "html.parser")
    image_url = soup.find("img", class_="headerimage fade-in")["src"]

    # Concatenate URL with image_url
    featured_image_url = url + image_url

    # Save MARS FACTS URL and visit the page
    url = 'https://galaxyfacts-mars.com/'

    #Extract the Facts Table from the URL using pandas
    tables=pd.read_html(url)
    df=tables[0]
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert Data back to HTML
    html_table = df.to_html(classes="table table-striped table-bordered")

    # Visit USGS webpage for Mars hemispehere images
    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "collapsible results" )
    pics = results.find_all("div", class_="item")

    # Iterate through each image
    for pic in pics:
        
        # Scrape the titles
        title = pic.find("h3").text
        
        # Clean title so I only have the name of the hemishpere
        title = title.replace("Enhanced", "")
        
        # Go the pic links
        link = pic.find("a")["href"]
        pic_link = url + link    
        browser.visit(pic_link)
        
        # Parse link HTMLs with Beautiful Soup
        html = browser.html
        soup = bs(html, "html.parser")
        
        # Scrape the full size images
        downloads = soup.find("div", class_="downloads")
        pic_url = downloads.find("a")["href"]
        
        # Add URLs and Titles for the full size images to image_urls
        image_urls.append({"title": title, "image_url": url + pic_url})

    scraped_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts": html_table,
        "hemispheres": image_urls,
        "last_modified": dt.datetime.now()
    }

    return scraped_data
