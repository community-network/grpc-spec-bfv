import sys
import httpcore
from google.protobuf.json_format import MessageToDict

sys.path.append("./proto")
from .proto import stats_pb2, auth_pb2, PrivateGames_pb2, inventory_pb2


class ApiClient:
    session: httpcore.AsyncConnectionPool

    def __init__(self):
        self.session = httpcore.AsyncConnectionPool(http2=True, keepalive_expiry=30)

    async def grpc_auth(self, BK_ol: str):
        response = await self.session.request(
            "POST",
            "https://sparta-gw-bfv.battlelog.com/proto/prod_default/prod_default/casablanca/pc/auth/viaAuthCode",
            headers={
                "X-PatchVersion": "7.3",
                "Content-Type": "application/x-protobuf",
                "X-RequestId": "1633955633_c",
            },
            content=auth_pb2.AuthRequest(
                auth_code=BK_ol, platform=1
            ).SerializeToString(),
        )
        item = auth_pb2.AuthResponse()
        item.ParseFromString(response.content)
        return MessageToDict(item)

    async def create_game_template(
        self, gw_sess: str, playground_id: str, checksum: str, location: str
    ):
        response = await self.session.request(
            "POST",
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

    async def get_playground(self, gw_sess: str, playground_id: str):
        response = await self.session.request(
            "POST",
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

    async def list_playgrounds_by_owner(self, gw_sess: str, player_id: int):
        response = await self.session.request(
            "POST",
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

    async def get_constraints(self, gw_sess: str):
        response = await self.session.request(
            "POST",
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

    async def get_scheduled_blueprints(self, gw_sess: str):
        response = await self.session.request(
            "POST",
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

    async def get_blueprints_by_id(self, gw_sess: str, blueprint_id: str):
        response = await self.session.request(
            "POST",
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

    async def get_inventories(self, gw_sess: str, player_id: str):
        response = await self.session.request(
            "POST",
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

    async def getstats(self, gw_sess: str, player_ids: list[int]):
        response = await self.session.request(
            "POST",
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
