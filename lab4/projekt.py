from ruamel import yaml
from socket import *
from tkinter import *

# Room class stores:
#     'name'      type: str       name of room
#     'objects'   type: list      list of devices
#     'master'    type: Tk object main instance of Tk window
# additionally between instances two fields are shared:
#     'UDP_IP'    type: str       broadcast ip
#     'UDP_PORT'  type: int       broadcast port

class Room:
    name = ""
    objects = []
    UDP_IP = "255.255.255.255"
    UDP_PORT = 2018
    master = None

    def __init__(self, name, master):
        self.name = name
        self.objects = []
        self.master = master

# Adding devices takes 'object1' type: tuple(id, description)
    def addObject(self,object1):
        self.objects.append(object1)

# Sends 'msg' type: str to stored in class IP:PORT
    def send(self,msg):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.sendto(bytes(msg, "utf-8"), (self.UDP_IP, self.UDP_PORT))

# Draws window
    def draw(self):
        global mainframe
        mainframe.destroy()
        mainframe = Frame(self.master)
        mainframe.pack()
        for o in self.objects:
            f = Frame(mainframe)
            f.pack(fill=BOTH, expand=YES)
            l = Label(f, text= o[1])
            l.pack(side=LEFT)
            on = Button(f, text="ON", command=lambda o=o: self.send("on "+o[0]))
            on.pack(side=RIGHT)
            off = Button(f, text="OFF", command=lambda o=o: self.send("off "+o[0]))
            off.pack(side=RIGHT)

# global main frame allows fast frame-clearing while changing rooms
mainframe = None


def main():
    global mainframe
# Creates main Tk instance minimal size of 200x200 name Pilot
# and links mainframe to it
    top = Tk()
    top.minsize(200, 200)
    top.title("Pilot")
    mainframe = Frame(top)
    mainframe.pack()
# Placeholder awaits user to pick room
    l = Label(mainframe, text="Choose room ;)")
    l.pack()
# Loads from yaml and parse it
    with open("conf2.yaml", 'r') as stream:
        data_loaded = yaml.load(stream, Loader=yaml.Loader)
    List = []
    for i in range(0,len(data_loaded)):
        for room_name in data_loaded[i]:
            List.append(Room(room_name,top))
            for id in data_loaded[i][room_name]:
                List[-1].addObject((id,data_loaded[i][room_name][id]))
#adds menu based on list of objects
    menubar = Menu(top)
    for room in List:
        menubar.add_command(label=room.name, command=room.draw)
    top.config(menu=menubar)
    top.mainloop()

#calls main
main()
