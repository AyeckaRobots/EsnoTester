from SystemUtils.GRpc.board_pb2_grpc import *
from SystemUtils.GRpc.board_pb2 import *
import grpc

from google.protobuf import wrappers_pb2
# from google.protobuf.wrappers_pb2 import Int32Value



def __init__(self, server_ip):
    self.server_ip = server_ip
    self.channel = grpc.insecure_channel(f"{server_ip}:50051")
    self.stub = board_pb2_grpc.DeviceServiceStub(self.channel)


def get_auth(self, username, password):
    request = api_pb2.AuthRequest(username=username, password=password, ip=self.server_ip)
    response = self.stub.GetAuth(request)
    return response.token


def get_rx_status(self, token):
    request = api_pb2.TokenRequest(token=token, ip=self.server_ip)
    response = self.stub.GetRxStatus(request)
    return response.status


def get_serial_number(self, token):
    request = api_pb2.TokenRequest(token=token, ip=self.server_ip)
    response = self.stub.GetSerialNumber(request)
    return response.serial_number


def get_current_noise(self, token):
    request = api_pb2.TokenRequest(token=token, ip=self.server_ip)
    response = self.stub.GetCurrentNoise(request)
    return response.noise


def get_advanced_stats(self, token):
    request = api_pb2.TokenRequest(token=token, ip=self.server_ip)
    response = self.stub.GetAdvancedStats(request)
    return response.agg_slices


def update_noise(self, value):
    request = api_pb2.NoiseRequest(value=value)
    self.stub.UpdateNoise(request)


def set_modulator_freq_1200M(self, token):
    request = api_pb2.TokenRequest(token=token, ip=self.server_ip)
    self.stub.SetModulatorFreq1200M(request)


def change_modcod(self, pls):
    request = api_pb2.ModcodRequest(pls=pls)
    self.stub.ChangeModcod(request)


def reset_advanced_stats(self, token):
    request = api_pb2.TokenRequest(token=token, ip=self.server_ip)
    self.stub.ResetAdvancedStats(request)


def set_freq(self, freq):
    request = api_pb2.FreqRequest(freq=freq)
    self.stub.SetFreq(request)


def read_esno(self, token):
    request = api_pb2.TokenRequest(token=token, ip=self.server_ip)
    response = self.stub.ReadEsno(request)
    return response.esno

def getTcStatus(id = 1):
    # Establish a gRPC channel (make sure the server is running on the correct port)
    channel = grpc.insecure_channel('localhost:50051')

    # Create a stub to interact with the BoardService
    stub = BoardServiceStub(channel)

    # Create the request message
    request = wrappers_pb2.Int32Value(value=id)

    # Call the GetPeriodicReport method
    response = stub.GetPeriodicReport(request)