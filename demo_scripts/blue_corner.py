import time
import sys
import random
from client import Client

default_community_delay = 30


	
def main():
	num_users = 8
	if len(sys.argv) > 1:
		num_users = int(sys.argv[1])

	simulated_users = []
	for n in range(num_users):
		username = "Blue_corner_" + str(n)
		simulated_users.append(Client(username))


	for client in simulated_users:
		client.join_community('blue corner')

	while(True):
		time.sleep(default_community_delay/2 -1)

		for i, client in enumerate(simulated_users):
			color = '#4a90e2'
			col = int((i+1) % 3)
			row = int((i+1) / 3)

			client.community_transaction(color, row, col)

		time.sleep(default_community_delay/2 +1)

if __name__ == '__main__':
	main()