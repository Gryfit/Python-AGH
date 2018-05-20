Remote
======

Dependencies
------------
Python 3
ruamel.yaml	to load yaml files
socket	to send UDP
tkinter	to render GUI

Use
---
Run command:

	python3 ./projekt.py

to choose configuration file you need to edit line 68:
	
	with open("your_configuration_file.yaml", 'r') as stream:

Description
-----------
First dummy window is created by Tk() with minsize and title properties. In this window mainframe is created, it will be recreated every time user switches room.
Next data are loaded form *.yaml file.
Data are then parsed into list of instances of class Room. Each object represent single room with devices.
Room class is a core of this code therefore I will explain it in detail:

Fields:
     'name'      type: str       name of room
     'objects'   type: list      list of devices
     'master'    type: Tk object main instance of Tk window
additionally between instances two fields are shared:
    'UDP_IP'     type: str       broadcast IP
    'UDP_PORT'   type: int       broadcast port
Methods:
	send(self,msg)		 sends msg to UDP_IP:UDP_PORT
	draw(self)			 recreates mainframe and adds labels and buttons
	addObject(self,object1)	 adds tuple (device_id, device_description)

Buttons perform send function with argument ‘on’/’off’ + device_id.
Labels display device_description.
Menu buttons use Room.name as labels and perform draw function on linked element.

Author
------
Bartłomiej Tonia

License
-------
GNU GPL
