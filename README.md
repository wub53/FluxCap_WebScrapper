# FluxCap_WebScrapper

Web Scrapper for downloading assets from icokik, facebook etc + scrapping content off Landing Page

# STEPS to initiate the Scrapper

1. In the directory where venv is , initiate the virtual env by command " source venv/bin/activate "
2. Go to spiders folder and run command " scrapy crawl video-scraper 
3. uvicorn main:app --host 0.0.0.0 --port 8000     ---- this command makes FASTAPI server to listen from any device not only localhost"
