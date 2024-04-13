import asyncio
import orjson
import uuid
import httpcore
import urllib.parse

bf5_access_token = "e5d039fe-0c78-41ee-8166-90fc5fd2cc33"
COOKIE = {
    "sid": "",
    "remid": "",
}


async def checkBf5GatewaySession(session):
    async with httpcore.AsyncConnectionPool() as client:
        """check if X-GatewaySession is valid for bf5"""
        ids = uuid.uuid1()
        global bf5_access_token
        url = "https://sparta-gw-bfv.battlelog.com/jsonrpc/pc/api"
        payload = {
            "jsonrpc": "2.0",
            "method": "Stats.detailedStatsByPersonaId",
            "params": {"personaId": "794397421", "game": "casablanca"},
            "id": f"{ids}",
        }
        # check if still valid
        r = await client.request(
            "POST",
            url,
            headers={
            "content-type": "application/json",
            "X-GatewaySession": f"{bf5_access_token}",
            "X-ClientVersion": "companion-4569f32f",
            }, content=orjson.dumps(payload)
        )
        if "error" in orjson.loads(r.content):
            # get new one if fails
            url = "https://accounts.ea.com/connect/auth?client_id=sparta-backend-as-user-pc&response_type=code&release_type=none"
            r = await client.request(
                "GET",
                url,
                headers={
                "User-Agent": "Mozilla/5.0 EA Download Manager Origin/10.5.89.45622",
                "X-Origin-Platform": "PCWIN",
                "Cookie": f"sid={COOKIE['sid']}; remid={COOKIE['remid']}; _nx_mpcid=c002360c-1ab0-4ce2-83d8-9a850d649e13; ealocale=nl-nl; ak_bmsc=E1AB16946A53CE2E1495B6BBF258CB7758DDA1073361000061E5405FB2BC7035~pl1h1xXQwIfdbF9zU3hMOujtpJ70BXJaFRqFWYPsE32q4qwE4onR+N6sn+T0KrqdpyZaf2ir3u+Xh68W3cEjOb+VLrQvI0jwTr1GFp5bgZXU812telOSjDjYPK3ddYJ7kOfbHtEglOs9UhdzOFi+UIWIAFdwcNq5ZoPv9Z0i53SspWuI4W3POlFqX70LxwwXcLMTQZgnGVs8R98goScJjo0Oo4D/+8LLzJsJfIUpr4AcgSC5B/ks2m5yz8ft9nh+9w; bm_sv=0B8CB6864011B573F81CA53CE1A570AD~qrTfU4mNBNCod1jfAFpeU+tG5OJ7w4r7lIg/ezmX6RLIIemuAT6EnFMcuhkUGHhJQSwjeV1kpadZtdXJAlbDoPxAafNmbaeQC/hteaiVlTMVV7R6gKPT8kWM22cFv6Y3Axp/S5XFhd6/Aw4cH6+Bng==; notice_behavior=implied,eu; _gid=GA1.2.827595775.1598088932; _gat=1",
                "Host": "accounts.ea.com",
            })
            resultDictionary = dict((x.decode(), y.decode()) for x, y in r.headers)
            redirect = resultDictionary["location"]
            access_code = urllib.parse.urlparse(redirect).query.split("=")[1]
            url = "https://sparta-gw-bfv.battlelog.com/jsonrpc/pc/api"
            return access_code
