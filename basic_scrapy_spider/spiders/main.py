from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()


# write api handlers for
# 1. Accepting iconik link and executing the scrapper to download the video.
# 2. Ensuring  the video is downloaded , call openai with respective option that has been sent inthe request with the prompt.


class VideoLink(BaseModel):
    vid_link: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/download")
async def process_vid_link (video_link_obj : VideoLink):
    print(video_link_obj.vid_link) 
    try:
        # Run the scrapy command with the URL as an argument
        command = [
            "scrapy", "crawl", "video_scraper",
            "-a", f"start_url={video_link_obj.vid_link}"
        ]

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "error": result.stderr}

    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"vid_link_got":video_link_obj.vid_link}
