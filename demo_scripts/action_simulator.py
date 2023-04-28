import time
import sys
import random
from client import Client


default_user_delay = 7

# rainbow color palette
colors = ['#ff0000', '#ffa500', '#ffff00', '#008000', '#0000ff', '#4b0082', '#ee82ee']

def main():
	'''
	Simulates N users doing normal actions

	sleeps for random times and 
	'''

	num_users = 10
	if len(sys.argv) > 1:
		num_users = int(sys.argv[1])

	simulated_users = []
	for n in range(num_users):
		username = "Sim_" + str(n)
		simulated_users.append(Client(username))

	sleep_times = [(5+random.randint(1, 5))] * num_users

	while(True):
		time.sleep(1)

		sleep_times = [time-1 for time in sleep_times]

		for i, t in enumerate(sleep_times):
			if t <= 0:
				# submit normal action

				color = colors[random.randint(0, len(colors)-1)]
				row = random.randint(0, 9)
				col = random.randint(0, 9)

				simulated_users[i].normal_action(color, row, col)


				# reset sleep time for this user
				sleep_times[i] = default_user_delay + random.randint(1, default_user_delay)

if __name__ == '__main__':
	main()