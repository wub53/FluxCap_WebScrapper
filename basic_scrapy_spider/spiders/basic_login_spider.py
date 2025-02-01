
from http import cookies
import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy_selenium import SeleniumRequest
from scrapy_playwright.page import PageMethod
from basic_scrapy_spider.items import CompanyListing 


# request = scrapy.Request( login_url, method='POST', 
#                           body=json.dumps(my_data), 
#                           headers={'Content-Type':'application/json'} )

filename = 'fully_rendered_html_41.txt'
filename1 = 'namesofthecompanies.txt'

def write_to_file(content,filename):
    with open (filename, "w" ) as f:
        f.write(content)

script = """
    () => {
            const allElements = document.querySelectorAll("*");
            let stylesData = "";

            allElements.forEach(element => {
                const computedStyles = window.getComputedStyle(element);
                stylesData += `Element: ${element.tagName}\n`;
                for (let style of computedStyles) {
                    stylesData += `${style}: ${computedStyles.getPropertyValue(style)}\n`;
                }
                stylesData += "\\n";
            });

            return stylesData;
        }
"""

class BasicLoginSpider(Spider):
    name = 'basic_login_spider'
    start_urls = ['https://www.pre-scient.com/']

    def start_requests(self):
        yield scrapy.Request(
                url = 'https://www.pre-scient.com/',
                meta= dict (
                    playwright = True,
                    playwright_include_page = True,

                    playwright_page_methods = [
                        PageMethod("wait_for_load_state", "networkidle"),
                        #PageMethod("wait_for_timeout", 10000),
                        PageMethod("evaluate", script),
                        #PageMethod("wait_for_timeout", 10000),
                    ],
                errback = self.errback
            ),
                callback = self.printOutput
                #callback=self.parse
            )
    

    async def printOutput(self, response):
        if "playwright_page_method_result" in response.meta:
            print("RESPONSE IN PRINTOUTPUT: --------------------", response.meta)
    # with open('computed-styles.txt', 'w') as file:
    #     file.write(response.text)

        

    # async def start_scraping(self, response):
    #     page = response.meta["playwright_page"]
    #     await page.close()
    #     print("response.url -----",response.url)
    #     next_page_url = "https://www.searchfunder.com/deal/exchange"
    #     yield scrapy.Request(response, meta = dict(playwright = True,
    #                                                playwright_include_page = True,
    #                                                playwright_page_methods= PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
    #                                                errback = self.errback,
    #                                                ),
    #                                                 callback = self.printOutput)
    #     print ("the respnse text  ----------",response.text)
    #     write_to_file(response.text,filename)
        # for quote in response.css('div.quote'):
        #         yield {
        #             'text': quote.css('span.text::text').get(),
        #             'author': quote.css('small.author::text').get(),
        #             'tags': quote.css('div.tags a.tag::text').getall(),
        #         }




    async def errback(self , failure):
        print("----------------------- FAILURE PAGE CLOSED --------------------------")
        page = failure.request.meta["playwright_page"]
        await page.close()
        

               


