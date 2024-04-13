from bfGrpc import *


class PingSite(gRPCMessage):
    name = TypedGRPC(1, str)
    ping = TypedGRPC(2, int)

    def create(self, name, ping):
        self.grpc_name = name
        self.grpc_ping = ping
        return self


class GetStatsRequest(gRPCMessage):
    pid = TypedGRPC(2, gRPCInt64)
    # defs = TypedGRPC(1, PlayerName)

    def with_id(self, pid):
        self.grpc_pid = pid
        # self.grpc_pid.grpc_pid = pid
        # self.grpc_defs = 2293814966
        return self


class PlayerInfo(gRPCMessage):
    personaId = TypedGRPC(1, gRPCInt64)
    # personaId = TypedGRPC(2, gRPCInt64)
    # platform  = TypedGRPC(3, int)


class StatField(gRPCMessage):
    name = TypedGRPC(1, str)
    value = TypedGRPC(2, gRPCSignedInt64)


class CatFields(gRPCMessage):
    fields = TypedGRPCList(1, StatField)


class StatCategory(gRPCMessage):
    catName = TypedGRPC(1, str)
    catFields = TypedGRPC(2, CatFields)


class PlayerStat(gRPCMessage):
    player = TypedGRPC(1, int)
    categories = TypedGRPCList(2, StatCategory)


class GetStatsResponse(gRPCMessage):
    playerStats = TypedGRPCList(1, PlayerStat)


class GetInventoriesRequest(gRPCMessage):
    players = TypedGRPCList(1, PlayerInfo)
    invType = TypedGRPC(2, int)

    def with_player(self, personaId):
        p = PlayerInfo()
        p.grpc_personaId = personaId
        # p.grpc_nucleusId = nucleusId
        # p.grpc_platform = platform
        self.grpc_invType = 1
        self.grpc_players = [p]
        return self


class GetBlueprintsByIdRequest(gRPCMessage):
    blueprint_ids = TypedGRPCList(1, str)
    include_fields = TypedGRPCList(2, str)

    def with_id(self, blueprint_id):
        self.grpc_blueprint_ids = [blueprint_id]
        self.grpc_include_fields = ["vanilla"]
        return self


class GetScheduledBlueprintsRequest(gRPCMessage):
    protocol_version = TypedGRPC(1, str)

    def with_id(self):
        self.grpc_protocol_version = "4237442"
        return self


class BlueprintInfo(gRPCMessage):
    blueprintType = TypedGRPC(1, str)
    blueprintId = TypedGRPC(2, str)


class GetBlueprintsByIdResponse(gRPCMessage):
    blueprintInfo = TypedGRPCList(1, BlueprintInfo)


class GetScheduledBlueprintsResponse(gRPCMessage):
    blueprintInfo = TypedGRPCList(1, BlueprintInfo)


class GlobalConstraints(gRPCMessage):
    maxPlaygroundsPerPlayer = TypedGRPC(1, int)
    maxGameServersPerPlayer = TypedGRPC(2, int)
    maxFollowedHostsListSize = TypedGRPC(3, int)


class GetConstraintsResponse(gRPCMessage):
    globalConstraints = TypedGRPC(1, GlobalConstraints)


class PlaygroundRequest(gRPCMessage):
    playground_id = TypedGRPC(2, str)

    def with_id(self, playground_id):
        self.grpc_playground_id = playground_id
        return self


class BoolMutator(gRPCMessageFlat):
    boolValue = TypedGRPC(1, bool, default=False)


class FloatMutator(gRPCMessageFlat):
    floatValue = TypedGRPC(1, gRPCFloat32)
    behaviour = TypedGRPC(2, int)


class StringMutator(gRPCMessageFlat):
    stringValue = TypedGRPC(1, str, default="OFF")


class IntMutator(gRPCMessageFlat):
    intValue = TypedGRPC(1, int)
    behaviour = TypedGRPC(2, int)


class CustomMutator(gRPCMessage):
    floatVal = TypedGRPC(1, gRPCFloat32)
    intVal = TypedGRPC(2, int)


class classMutator(gRPCMessage):
    boolValue = TypedGRPC(1, BoolMutator)
    limits = TypedGRPC(5, CustomMutator)


class MapInfo(gRPCMessage):
    mapname = TypedGRPC(1, str)
    mode = TypedGRPC(2, str)
    gameSize = TypedGRPC(3, int)
    rounds = TypedGRPC(4, int)
    mapMode = TypedGRPC(6, str)
    warmUpSize = TypedGRPC(8, int)
    allowedSpectators = TypedGRPC(9, int)


class Creation(gRPCMessage):
    seconds = TypedGRPC(1, int)
    # nanos = TypedGRPC(2, int)


class Classes(gRPCMessage):
    name = TypedGRPC(1, str)
    className = TypedGRPC(2, str)
    value = TypedGRPC(3, classMutator)


class MapRotation(gRPCMessage):
    mapRotation = TypedGRPCList(1, MapInfo)
    roundIndex = TypedGRPC(2, int)


class descMutator(gRPCMessage):
    text = TypedGRPC(1, str)


class serverDesc(gRPCMessage):
    serverName = TypedGRPC(1, str)
    description = TypedGRPC(2, descMutator)


class Playground(gRPCMessage):
    playgroundId = TypedGRPC(1, str)
    ownerId = TypedGRPC(2, int)
    bluePrintType = TypedGRPC(3, str)
    configName = TypedGRPC(4, str)
    infoMutators = TypedGRPCList(6, Classes)
    mapRotation = TypedGRPC(7, MapRotation)
    checksum = TypedGRPC(9, str)
    createdAt = TypedGRPC(11, Creation)
    updatedAt = TypedGRPC(12, Creation)
    serverdesc = TypedGRPC(13, serverDesc)


class PlaygroundResponse(gRPCMessage):
    server = TypedGRPC(1, Playground)


class ListPlaygroundsByOwnerRequest(gRPCMessage):
    playerid = TypedGRPC(1, int)
    blueprint_type = TypedGRPC(2, str)

    def with_id(self, playerid):
        self.grpc_playerid = playerid
        self.grpc_blueprint_type = "vanilla"
        return self


class ListPlaygroundsByOwnerResponse(gRPCMessage):
    playgrounds = TypedGRPCList(1, Playground)
    validatedPlaygrounds = TypedGRPCList(2, Playground)


class CreateGameTemplateRequest(gRPCMessage):
    protocol = TypedGRPC(1, str)
    playground = TypedGRPC(2, str)
    checksum = TypedGRPC(3, str)
    pingsites = TypedGRPCList(5, PingSite)

    def create(self, playgroundId: str, checksum: str, location: str):
        self.grpc_protocol = "4237442"
        self.grpc_playground = playgroundId
        self.grpc_checksum = checksum
        self.grpc_pingsites = [
            PingSite().create(location, 10)
            #     PingSite().create("aws-bom", 100),
            #     PingSite().create("aws-brz", 100),
            #     PingSite().create("aws-cdg", 100),
            #     PingSite().create("aws-cmh", 100),
            #     PingSite().create("aws-dub", 10),
            #     PingSite().create("aws-fra", 10),
            #     PingSite().create("aws-hkg", 100),
            #     PingSite().create("aws-iad", 100),
            #     PingSite().create("aws-icn", 100),
            #     PingSite().create("aws-lhr", 100),
            #     PingSite().create("aws-nrt", 100),
            #     PingSite().create("aws-pdx", 100),
            #     PingSite().create("aws-sin", 100),
            #     PingSite().create("aws-sjc", 100),
            #     PingSite().create("aws-syd", 100),
            #     PingSite().create("m3d-dxb", 100),
            #     PingSite().create("m3d-hkg", 100),
            #     PingSite().create("m3d-jnb", 100),
        ]
        return self


class CreateGameTemplateResponse(gRPCMessage):
    # Can be string if error!!
    gameId = TypedGRPC(1, gRPCInt64)
    pingSite = TypedGRPC(2, str)


class CreateGameTemplateErrorResponse(gRPCMessage):
    error = TypedGRPC(1, str)
    pingSite = TypedGRPC(2, str)


class AuthResponse(gRPCMessage):
    authCode = TypedGRPC(1, str)
    playerId = TypedGRPC(2, int)


class AuthRequest(gRPCMessage):
    auth_code = TypedGRPC(1, str)
    platform = TypedGRPC(5, int)

    def with_code(self, code):
        self.set_rpc_value("platform", 1)
        self.set_rpc_value("auth_code", code)
        return self
