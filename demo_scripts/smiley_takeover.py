import time
import sys
import random
from client import Client

default_community_delay = 30
	
colors = ['#f8e71c'] * 100

def main():

	black = [32, 42, 43, 36, 46, 47, 62, 63, 64, 65, 66, 67, 75, 76]
	white = [33, 37]
	red = [73, 74]

	for i in black:
		colors[i] = '#000000'
	for i in white:
		colors[i] = '#ffffff'
	for i in red:
		colors[i] = '#d0021b'

	num_users = 100
	if len(sys.argv) > 1:
		num_users = int(sys.argv[1])

	simulated_users = []
	for n in range(num_users):
		username = "smiley_" + str(n)
		simulated_users.append(Client(username))


	for client in simulated_users:
		client.join_community('smiley')

	while(True):
		time.sleep(default_community_delay/2 -1)

		for i, client in enumerate(simulated_users):
			color = colors[i]
			col = int(i % 10)
			row = int(i / 10)

			client.community_transaction(color, row, col)

		time.sleep(default_community_delay/2 +1)

if __name__ == '__main__':
	main()