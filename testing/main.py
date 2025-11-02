import sys
from pprint import pprint
import asyncio
from duck_grpc_client_bfv.grpcClient import ApiClient
from duck_grpc_client_bfv.accessToken import checkBf5GatewaySession
from duck_grpc_client_bfv.component import *


async def main():
    token = "QUOxADTSOsYJr1SgJ8RayWcsgvJqgGa4bqIcrEg7AQ"
    code = await checkBf5GatewaySession(token)
    answer = await ApiClient().grpc_auth(code)
    gw_sess = answer["authCode"]
    answer = await ApiClient().get_playground(gw_sess, "9be10590-441c-11ea-ab05-68bba39e8402")
    # answer = await getConstraints(gw_sess)
    # print(answer["playerId"])
    # answer = await listPlaygroundsByOwner(gw_sess, answer["playerId"])

    # playground = answer["server"]
    # answer = await createGameTemplate(
    #     gw_sess, playground["playgroundId"], playground["checksum"], "aws-fra"
    # )
    # sheduled = await getScheduledBlueprints(gw_sess)
    # answer = await getBlueprintsById(
    #     gw_sess, sheduled["blueprintInfo"][0]["blueprintId"]
    # )
    # answer = await getInventories(gw_sess, 794397421)
    # answer = await getstats(gw_sess, 794397421)

    print(answer)

    # answer = b"\n\xd7\x01Checksum '126010cf44f507127b264ba0bcd23c99483fdf2bf07f34a9638ab7e7f9666e7b' didn't match expected '57460576e0cae5d50e83b3592619cadfc5845564c082729a21200a8f3a9c0de9' in playground a4dd7c90-3638-11ec-8a34-20ee8c1834d6\x10e"
    # print(GRPCController(protobuf=True).deserialize_bytes(answer, CreateGameTemplateErrorResponse).to_dict())


if __name__ == "__main__":
    asyncio.run(main())

# {
# "AWS India": "aws-bom",
# "AWS Brazil": "aws-brz",
# "AWS Paris France": "aws-cdg",
# "AWS Columbus USA": "aws-cmh",
# "AWS Dublin": "aws-dub",
# "AWS Germany": "aws-fra",
# "AWS Hong Kong": "aws-hkg",
# "AWS Virginia": "aws-iad",
# "AWS South korea": "aws-icn",
# "AWS United Kingdom": "aws-lhr",
# "AWS Tokyo": "aws-nrt",
# "AWS Portland USA": "aws-pdx",
# "AWS Singapore": "aws-sin",
# "AWS San Jose USA": "aws-sjc",
# "AWS Australia": "aws-syd",
# "M3D Dubai": "m3d-dxb",
# "M3D Hong Kong": "m3d-hkg",
# "M3D South Africa": "m3d-jnb"
# }
