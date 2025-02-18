from SystemUtils.GRpc.board_pb2_grpc import *
from SystemUtils.GRpc.board_pb2 import *
import grpc

from google.protobuf import wrappers_pb2

def get_tc_status(id = 1):

    channel = grpc.insecure_channel('localhost:50051')
    stub = BoardServiceStub(channel)

    request = wrappers_pb2.Int32Value(value=id)
    response = stub.GetPeriodicReport(request)
    print(response)

get_tc_status()