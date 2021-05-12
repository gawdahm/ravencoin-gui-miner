from tkinter import *
import subprocess, os, pickle
from sys import platform
from tkinter.filedialog import askopenfilename
from ravenminer import RavenMiner
raven_miner = RavenMiner()
    

def populate_mining_pool_dropdown():
    pools = []
    for key in raven_miner.mining_pools:
        pools.append(key)
    return pools
# Button functions
def change_dropdown(*args):
    raven_miner.mining_pool = raven_miner.mining_pools[miningpoolname.get()]
    print( miningpoolname.get() )

def get_wallet_addr(*args):
    print( walletaddr.get() )

def save_settings():
    a_file = open("data.pkl", "wb")
    dictionary_data = {
        'wallet' : walletaddr.get(), 
        'miningpoolname' : miningpoolname.get(),
        'minerpath' : minerpath.get(),
        }
    pickle.dump(dictionary_data, a_file)
    a_file.close()

def check_address():
    if not walletaddr.get():
        return False
    return True

def start_mining():
    if not check_address():
        print("Invalid wallet")
        return
    #getminingdata(  )
    
    p = subprocess.Popen(minerpath.get() + raven_miner.PROCNAME + " --url=cryptonote.social:2222 --user {} --threads=1 --pass='email=runforestrun@airmail.cc'".format(walletaddr.get()), shell=True)
    print("Mining started!")

def stop_mining():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system('pkill '+ raven_miner.PROCNAME)
    elif platform == "win32":
        os.system("taskkill /f /im {}.exe".format(raven_miner.PROCNAME))

root = Tk()

# Menu
def NewFile():
    print("New File!")
def OpenFile():
    name = askopenfilename()
    print(name)
def About():
    print("This is a simple example of a menu")

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)
# !Menu

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

# Create a Tkinter variable
miningpoolname = StringVar(root)
walletaddr = StringVar(root)
minerpath = StringVar(root)

# Miner Path
Label(mainframe, text="Path to executable: ").grid(row = 1, column = 1)
miner_path_entry = Entry(mainframe, textvariable=minerpath).grid(row = 1, column = 2)
# Wallet Info
Label(mainframe, text="Wallet Address: ").grid(row = 2, column = 1)
wallet_entry = Entry(mainframe, textvariable=walletaddr).grid(row = 2, column = 2)
# Mining pool drop down
choices = populate_mining_pool_dropdown()
popupMenu = OptionMenu(mainframe, miningpoolname, *choices)
Label(mainframe, text="Mining Pool: ").grid(row = 3, column = 1)
popupMenu.grid(row = 3, column = 2)
Label(mainframe, text="Hashrate ").grid(row = 4, column = 1)
Label(mainframe, text=raven_miner.balance).grid(row = 4, column = 2)
Label(mainframe, text="Balance ").grid(row = 5, column = 1)
Label(mainframe, text=raven_miner.hashrate).grid(row = 5, column = 2)

#  track changes
miningpoolname.trace('w', change_dropdown)
walletaddr.trace("w", get_wallet_addr)

start_mining_btn = Button(mainframe, text = "Start Mining", command = lambda: start_mining()).grid(row = 6, column = 1)
stop_mining_btn = Button(mainframe, text = "Stop Mining", command = lambda: stop_mining()).grid(row = 6, column = 2)
save_settings_btn = Button(mainframe, text = "Save", command = lambda: save_settings()).grid(row = 7, column = 1)


# Load settings
# init file if it doesn't exist and populate it with blank entries
# TODO: Inefficient
if not os.path.isfile("data.pkl"):
    f = open("data.pkl", "w")
    f.close()
    save_settings()


a_file = open("data.pkl", "rb")
output = pickle.load(a_file)
a_file.close()

# Populate fields
walletaddr.set(output['wallet'])
minerpath.set(output['minerpath']) # set the default option
miningpoolname.set(output['miningpoolname']) # set the default option
raven_miner.mining_pool = raven_miner.mining_pools[output['miningpoolname']]

mainloop()