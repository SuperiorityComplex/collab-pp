import threading
import grpc
import sys
import time
sys.path.append('../backend/grpc_stubs')
import main_pb2
import main_pb2_grpc

server = "127.0.0.1:3000"

class Client():
	def __init__(self, username):
		self.username = username
		self.channel = grpc.insecure_channel(server)
		self.stub = main_pb2_grpc.PPStub(self.channel)
		self.community = 'NO_COMM'

		response = self.stub.CreateUser(
			main_pb2.UserRequest(username=self.username)
		)

	def normal_action(self, color, row, col):
		response = self.stub.NormalAction(
			main_pb2.UserRequest(username=self.username, color=color, row=row, col=col)
		)

		if 'Error' in response.message:
			print(self.username, '-', response)

	def join_community(self, community):
		response = self.stub.JoinCommunity(
			main_pb2.UserRequest(username=self.username, community=community)
		)
		self.community=community

		if 'Error' in response.message:
			print(self.username, '-', response)

	def community_transaction(self, color, row, col):
		response = self.stub.JoinCommunityTransaction(
			main_pb2.UserRequest(username=self.username, color=color, row=row, col=col)
		)

		if 'Error' in response.message:
			print(self.username, '-', response)