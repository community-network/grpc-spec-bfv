import httpcore
import sys
from component import (
    AuthResponse,
    CreateGameTemplateErrorResponse,
    CreateGameTemplateRequest,
    CreateGameTemplateResponse,
    GRPCController,
    AuthRequest,
    GetBlueprintsByIdRequest,
    GetInventoriesRequest,
    GetScheduledBlueprintsRequest,
    GetScheduledBlueprintsResponse,
    GetStatsRequest,
    ListPlaygroundsByOwnerRequest,
    ListPlaygroundsByOwnerResponse,
    PlaygroundRequest,
    PlaygroundResponse,
    GetConstraintsResponse,
    GetStatsResponse,
    GetBlueprintsByIdResponse,
)


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
            content=GRPCController(protobuf=True).serialize_bytes(
                AuthRequest().with_code(BK_ol)
            ),
        )
        return (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, AuthResponse)
            .to_dict()
        )


async def createGameTemplate(
    gw_sess: str, playgroundId: str, checksum: str, location: str
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
            content=GRPCController(protobuf=True).serialize_bytes(
                CreateGameTemplateRequest().create(playgroundId, checksum, location)
            ),
        )
        info = (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, CreateGameTemplateResponse)
            .to_dict()
        )
        if info["pingSite"] == None:
            return (
                GRPCController(protobuf=True)
                .deserialize_bytes(response.content, CreateGameTemplateErrorResponse)
                .to_dict()
            )
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
            content=GRPCController(protobuf=True).serialize_bytes(
                PlaygroundRequest().with_id(playground_id)
            ),
        )
        return (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, PlaygroundResponse)
            .to_dict()
        )


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
            content=GRPCController(protobuf=True).serialize_bytes(
                ListPlaygroundsByOwnerRequest().with_id(player_id)
            ),
        )
        return (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, ListPlaygroundsByOwnerResponse)
            .to_dict()
        )


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
            content=GRPCController(protobuf=True).serialize_bytes(""),
        )
        return (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, GetConstraintsResponse)
            .to_dict()
        )


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
            content=GRPCController(protobuf=True).serialize_bytes(
                GetScheduledBlueprintsRequest().with_id()
            ),
        )
        return (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, GetScheduledBlueprintsResponse)
            .to_dict()
        )


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
            content=GRPCController(protobuf=True).serialize_bytes(
                GetBlueprintsByIdRequest().with_id(blueprint_id)
            ),
        )
        return (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, GetBlueprintsByIdResponse)
            .to_dict()
        )
        # print(response.content.hex())
        # todo: what does it return?


async def getInventories(gw_sess: str, blueprint_id: str):
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
            content=GRPCController(protobuf=True).serialize_bytes(
                GetInventoriesRequest().with_player(blueprint_id)
            ),
        )
        print(response.content.hex())
        # todo: what does it return?


async def getstats(gw_sess: str, player_id: str):
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
            content=GRPCController(protobuf=True).serialize_bytes(
                GetStatsRequest().with_id(player_id)
            ),
        )
        return (
            GRPCController(protobuf=True)
            .deserialize_bytes(response.content, GetStatsResponse)
            .to_dict()
        )
