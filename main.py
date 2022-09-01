import datetime
import json
import os
import uuid

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from redis import StrictRedis
from starlette.requests import Request
from starlette.responses import Response

import resp_code
from mytools import Video

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

load_dotenv(verbose=True)

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
    },
)

# --------env-----------
APPID = os.getenv("APPID")
SECRET = os.getenv("SECRET")
# TODO: 部署正式环境记得换.env中的内容
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASS = os.getenv("REDIS_PASS")


# --------env-----------


class VideoInfo(BaseModel):
    pass


@app.get("/")
async def root():
    return {"message": "Hello my API"}


@app.get(
    "/v1/wx/session/{code}",
    summary="静默登录",
    tags=["用户模块"],
    response_description="响应描述？完了再写",
)
async def login(code: str):
    """
    接收用户登录凭证，返回**session_id**
    """
    res = requests.get(
        url="https://api.weixin.qq.com/sns/jscode2session",
        params={
            "appid": APPID,
            "secret": SECRET,
            "js_code": code,
            "grant_type": "authorization_code",
        },
    )
    if res.status_code == 200:
        result = json.loads(res.text)
        session_id = uuid.uuid1().hex
        redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASS)
        redis.hset(session_id, "session_key", result["session_key"])
        redis.hset(session_id, "openid", result["openid"])
        redis.expire(session_id, 7200)
        # TODO: 考虑是否写入MySQL
        return resp_code.resp_200(data={"session": session_id})

    else:
        return resp_code.resp_400(message="errno", data="errno")


@app.get("/v1/wx/video-info")
async def get_video_info(url: str):
    # url = find_url(video_str)
    v = Video(url)
    match url:
        case url if "douyin" in url:
            v.douyin()
        # TODO: 挨着写，还有无数个
    if Video.status_code == 200:
        var = Video.video_info
        return resp_code.resp_200(data=var)
    else:
        return resp_code.resp_400(message="errno", data="errno")


@app.get("/v1/wx/video-file")
async def get_video_file(url: str, req: Request):
    """透传 API"""
    # host = "http://example.intranet"
    # url = "{}/other/{}".format(host, other_path)
    # body = bytes(await req.body()) or None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ("
        "KHTML, like Gecko) "
        "Chrome/51.0.2704.63 Safari/537.36"
    }
    r = requests.request(
        method="get",
        url=url,
        headers=headers,
        # headers={
        #     "Cookie": req.headers.get("cookie") or "",
        #     "Content-Type": req.headers.get("Content-Type"),
        # },
        # params=req.query_params,
        # data=body,
        stream=True,
        # allow_redirects=False,
    )
    t = datetime.datetime.now()
    t = t.strftime("%Y%m%d%H%M%S")
    # h = dict(r.headers)
    # h.pop("Content-Length", None)
    return Response(
        r.content,
        media_type="video/mp4",
        headers={
            "Content-Type": "application/force-download;",
            "Content-Disposition": f"attachment; filename={t}.mp4",
            "Content-Length": f'{r.headers["Content-Length"]}',
        },
    )


if __name__ == "__main__":
    pass
