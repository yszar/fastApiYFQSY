from fastapi import FastAPI
from pydantic import BaseModel

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="去水印接口",
    description=description,
    version="v0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)


class VideoInfo(BaseModel):
    pass

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/video")
async def get_video_info(name: str):
    return {"message": f"Hello {name}"}
