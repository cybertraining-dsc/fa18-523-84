#Initial Cluster Setup

from fabric import Connection

#parent node eth0: 10.0.0.42  wlan0:10.0.0.31

workers = {'PiCluster_w01': '10.0.0.36', 
	   'PiCluster_w02': '10.0.0.37', 
	   'PiCluster_w03': '10.0.0.41', 
	   'PiCluster_w04': '10.0.0.40'}

for key, value in workers.items():
	#print(key+': '+value)
	c = Connection(value, connect_timeout=60)
	c.connect_kwargs.password = 'Weather_Center01' #change back to raspberry
	
	result = c.run('uname -s')
	print("{}: {}".format(value, result.stdout.strip()))
	
	'''
	#change password and hostname
	print('INFO: changing password')
	c.run('echo pi:Weather_Center01 | sudo chpasswd') #uname -s
	print('INFO: password changed')
	print('INFO: changing hostname')
	c.run('sudo hostnamectl set-hostname '+key)
	c.run('echo $(hostname -I | cut -d\  -f1) $(hostname) | sudo tee -a /etc/hosts')
	print('INFO: hostname changed')
	'''
	
	#update nodes
	print('\n\nINFO: updating node\n\n')
	print('INFO: running sudo apt-get update')
	c.run('sudo apt-get update')
	print('INFO: running apt-get upgrade -y')
	c.run('sudo apt-get upgrade -y')
	print('INFO: running sudo apt-get dist-upgrade -y')
	c.run('sudo apt-get dist-upgrade -y')
	print('\n\nINFO: updates complete\n\n')
	
	#install git
	print('\n\nINFO: installing git and adding git repos\n\n')
	c.run('sudo apt-get install git -y')
	try:
		c.run('sudo mkdir git-repos')
		c.run('cd git-repos')
		c.run('git clone https://github.com/cloudmesh-community/fa18-523-84.git')
	except:
		print('ERROR: could not clone git repos')
	print('\n\nINFO: git setup complete\n\n')
	
	#Install packages and programs
	print('\n\nINFO: installing python packages\n\n')
	c.run('sudo apt-get install python3-pip -y')
	c.run('sudo apt-get install python3-pandas -y')
	#c.run('sudo easy_install3 cassandra-driver')
	print('\n\nINFO: python packages installed\n\n')
	
	#Install Cassandra on each node
	#source: https://cassandra.apache.org/doc/latest/getting_started/installing.html#installation-from-binary-tarball-files
	print('\n\nINFO: installing cassandra\n\n')
	c.run('sudo apt-get purge openjdk*')
	c.run('sudo apt-get install openjdk-8-jdk -y')
	try:
		c.run('wget "https://www-us.apache.org/dist/cassandra/3.11.3/apache-cassandra-3.11.3-bin.tar.gz"')
		c.run('tar -xvf apache-cassandra-3.11.3-bin.tar.gz')
	except:
		print('ERROR: cassandra was not installed')
	print('\n\nINFO: cassandra installation successful\n\n')
	    
	#reboot each node
	#c.run('sudo shutdown -r 1') #reboot in 60 sec to avoid issues with ssh connection
	
