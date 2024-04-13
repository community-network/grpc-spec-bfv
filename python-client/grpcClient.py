import sys
import httpcore
from google.protobuf.json_format import MessageToDict

sys.path.append("./proto")
from proto import stats_pb2, auth_pb2, PrivateGames_pb2, inventory_pb2


async def grpcAuth(BK_ol: str):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/auth/viaAuthCode",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
            },
            content=auth_pb2.AuthRequest(auth_code=BK_ol, platform=1).SerializeToString(),
        )
        item = auth_pb2.AuthResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)


async def createGameTemplate(
    gw_sess: str, playground_id: str, checksum: str, location: str
):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/PrivateGames/createGameTemplate",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=PrivateGames_pb2.CreateGameTemplateRequest(
                protocol="4237442",
                playground=playground_id,
                checksum=checksum,
                pingsites=[{"name": location, "ping": 10}],
            ).SerializeToString(),
        )
        item = PrivateGames_pb2.CreateGameTemplateResponse()
        item.ParseFromString(response.content)
        info = MessageToDict(item)
        if info.get("pingSite", None) == None:
            item = PrivateGames_pb2.CreateGameTemplateErrorResponse()
            item.ParseFromString(response.content)
            return MessageToDict(item)
        return info


async def getPlayground(gw_sess: str, playground_id: str):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/PrivateGames/getPlayground",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=PrivateGames_pb2.PlaygroundRequest(
                playground_id=playground_id
            ).SerializeToString(),
        )
        item = PrivateGames_pb2.PlaygroundResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)


async def listPlaygroundsByOwner(gw_sess: str, player_id: int):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/PrivateGames/listPlaygroundsByOwner",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=PrivateGames_pb2.ListPlaygroundsByOwnerRequest(
                playerid=int(player_id), blueprint_type="vanilla"
            ).SerializeToString(),
        )
        item = PrivateGames_pb2.ListPlaygroundsByOwnerResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)


async def getConstraints(gw_sess: str):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/PrivateGames/GetConstraints",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=PrivateGames_pb2.Empty().SerializeToString(),
        )
        item = PrivateGames_pb2.GetConstraintsResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)


async def getScheduledBlueprints(gw_sess: str):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/PrivateGames/getScheduledBlueprints",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=PrivateGames_pb2.GetScheduledBlueprintsRequest(
                grpc_protocol_version="4237442"
            ).SerializeToString(),
        )
        item = PrivateGames_pb2.GetScheduledBlueprintsResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)


async def getBlueprintsById(gw_sess: str, blueprint_id: str):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/PrivateGames/getBlueprintsById",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=PrivateGames_pb2.GetBlueprintsByIdRequest(
                blueprint_ids=[blueprint_id], include_fields=["vanilla"]
            ).SerializeToString(),
        )
        item = PrivateGames_pb2.GetBlueprintsByIdResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)


async def getInventories(gw_sess: str, player_id: str):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/inventory/getInventories",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=inventory_pb2.GetInventoriesRequest(
                players=[{"personaId": player_id}], invType=1
            ).SerializeToString(),
        )
        print(response.content)
        # todo: what does it return?


async def getstats(gw_sess: str, player_ids: list[int]):
    async with httpcore.AsyncConnectionPool(http2=True) as client:
        response = await client.request(
            'POST',
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/stats/getstats",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
                "X-GatewaySession": gw_sess,
            },
            content=stats_pb2.GetStatsRequest(players=player_ids).SerializeToString(),
        )
        item = stats_pb2.GetStatsResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)
