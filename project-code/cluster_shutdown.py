#shutdown cluster

#ERROR WITH FABRIC SHUTDOWN AND REBOOT http://www.fabfile.org/upgrading.html#task-functions-decorators
#Work around is to schedule shutdown for 1min later.

from fabric import Connection

parent_node = '10.0.0.31' #wlan0 = 10.0.0.31 | eth0 = 169.254.156.125

workers = {'w1': '169.254.62.205', 'w2': '169.254.122.189', 'w3': '169.254.159.1', 'w4': '169.254.111.219'}

for key, value in workers.items():
	print(key+': '+value)
	c = Connection(value)
	c.connect_kwargs.password = 'Weather_Center01' #change back to raspberry
	result = c.run('sudo shutdown -h 1') #uname -s
	print("{}: {}".format(value, result.stdout.strip()))