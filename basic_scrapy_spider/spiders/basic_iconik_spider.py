from http import cookies
import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy_selenium import SeleniumRequest
from scrapy_playwright.page import PageMethod
import scrapy
from scrapy_playwright.page import PageMethod
from scrapy_playwright.page import PageMethod

import scrapy
from scrapy_playwright.page import PageMethod

class VideoScraper(Spider):
    name = "video_scraper"
    #start_url = "https://icnk.io/u/Aokozj3WZKHg/"

    def start_requests(self):
        yield scrapy.Request(
                url = "https://icnk.io/u/CtYlCj0yk6Fd/",
                meta= dict (
                    playwright = True,
                    playwright_include_page = True,
                    playwright_page_methods = [
                        PageMethod("wait_for_timeout", 4000),
                        PageMethod("wait_for_selector", "button.dropdown_button__button"),
                        PageMethod("wait_for_timeout", 2000),
                        PageMethod("click", "button.dropdown_button__button"),
                        PageMethod("wait_for_timeout", 2000),
                        PageMethod("wait_for_selector",".actions_list__item > .actions_list__item_icon_label > div > div "),
                        PageMethod("wait_for_timeout", 2000),
                        # PageMethod("click",".actions_list__item > .actions_list__item_icon_label > div > div "),
                        # PageMethod("wait_for_timeout", 2000),
                        #PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        #PageMethod("wait_for_selector", "div._media_wrapper_22ggl_25 video"),
                    ],
                errback = self.errback
            ),
                callback = self.start_scraping
                #callback=self.parse
            )
        #print ("the respnse text  ----------",response.text)
        
    async def printOutput(self, response):
        if "playwright_page_method_result" in response.meta:
            print("RESPONSE IN PRINTOUTPUT: --------------------", response.text)

    async def start_scraping(self, response):
        page = response.meta["playwright_page"]

        # Set up the download handler
        async with page.expect_download() as download_info:
            # Click the "Original" text to trigger the download
            await page.click(".actions_list__item > .actions_list__item_icon_label > div > div ")

        # Wait for the download to start
        download = await download_info.value

        # Save the downloaded file to a specific location
        file_path = "/home/ubuntu/FluxCap_WebScrapper/basic_scrapy_spider/Downloads/downloaded_video.mp4"
        await download.save_as(file_path)

        self.logger.info(f"-----------------------Video downloaded and saved to: {file_path}-----------------------")

        # Close the page
        await page.close()

    async def errback(self , failure):
        print("----------------------- FAILURE PAGE CLOSED --------------------------")
        page = failure.request.meta["playwright_page"]
        await page.close()
