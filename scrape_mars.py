# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# create the scraping function
def scrape():

    # set up the splinter service
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = True)

    # WEB SCRAPING - NASA Mars News

    # specify the initial browser URL
    web_url = "https://redplanetscience.com"

    # send the browser to the specified URL
    browser.visit(web_url)

    # define the BeautifulSoup instance
    soup = bs(browser.html, "html.parser")

    # retrieve a list of the matching HTML elements
    results = soup.body.find_all("div", class_ = "list_text")

    # get the title and paragraph from the first item in the collection
    news_title = results[0].find("div", class_ = "content_title").text.strip()
    news_paragraph = results[0].find("div", class_ = "article_teaser_body").text.strip()

    # WEB SCRAPING - JPL Mars Space Images - Featured Image

    # specify the second browser URL
    web_url = "https://spaceimages-mars.com"

    # send the browser to the specified URL
    browser.visit(web_url)

    # navigate to and select the Mars option
    browser.find_by_id("options").select_by_text("Mars")

    # define the BeautifulSoup instance
    soup = bs(browser.html, "html.parser")

    # get the featured image full URL
    featured_image_url = f'{web_url}/{soup.body.find("img", class_ = "headerimage fade-in")["src"]}'

    # WEB SCRAPING - Mars Facts

    # specify the second browser URL
    web_url = "https://galaxyfacts-mars.com"

    # convert the HTML into a list of DataFrames
    table_dfs = pd.read_html("https://galaxyfacts-mars.com")

    # retrieve the corresponding DataFrame
    table_df = table_dfs[0]

    # convert the DataFrame into HTML
    table_html = table_df.to_html()

    # WEB SCRAPING - Mars Hemispheres

    # specify the initial browser URL
    web_url = "https://marshemispheres.com"

    # send the browser to the specified URL
    browser.visit(web_url)

    # define the BeautifulSoup instance
    soup = bs(browser.html, "html.parser")

    # retrieve a list of the HTML item elements
    results = soup.body.find("div", class_ = "collapsible results").find_all("div", class_ = "item")

    # initialize the list of dictionaries
    hemisphere_image_urls = []

    # extract the relevant information
    for result in results:
        
        # extract the relevant anchor
        current_anchor = result.find("div", class_ = "description").find("a", class_ = "itemLink product-item")
        
        # extract the title
        img_title = current_anchor.find("h3").text.strip()
        
        # construct the link to the subpage
        link = f'{web_url}/{current_anchor["href"]}'
        
        # navigate to the subpage
        browser.visit(link)
        
        # redefine the BeautifulSoup instance
        soup = bs(browser.html, "html.parser")
        
        # extract the image link
        img_link = f'{web_url}/{soup.body.find("div", class_ = "downloads").find("ul").find_all("li")[1].find("a")["href"]}'
        
        # append the information to the list
        hemisphere_image_urls.append({"title": img_title, "img_url": img_link})

    # close the browser
    browser.quit()
    
    return [{"source": "nasa_mars_news", "data": {"title": news_title, "paragraph": news_paragraph}},
            {"source": "jpl_mars_space_images", "data": featured_image_url},
            {"source": "mars_facts", "data": table_html},
            {"source": "mars_hemispheres", "data": hemisphere_image_urls}]