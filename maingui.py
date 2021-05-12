from tkinter import *
import os, pickle
from sys import platform
from settingswindow import RavenMinerGUISettingsWindow

class RavenMinerGUI:
    def __init__(self, master, raven_miner):
        self.master = master
        self.settings_window = RavenMinerGUISettingsWindow(master)
        self.raven_miner = raven_miner
        master.title("Raven GUI Miner")
    
        # Add a grid
        self.mainframe = Frame(master)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(pady = 100, padx = 100)

        # Create a Tkinter variable
        self.miningpoolname = StringVar(master)
        self.walletaddr = StringVar(master)
        self.minerpath = StringVar(master)

        # Miner Path
        Label(self.mainframe, text="Path to executable: ").grid(row = 1, column = 1)
        miner_path_entry = Entry(self.mainframe, textvariable=self.minerpath).grid(row = 1, column = 2)
        # Wallet Info
        Label(self.mainframe, text="Wallet Address: ").grid(row = 2, column = 1)
        wallet_entry = Entry(self.mainframe, textvariable=self.walletaddr).grid(row = 2, column = 2)
        # Mining pool drop down
        self.choices = self.populate_mining_pool_dropdown()
        popupMenu = OptionMenu(self.mainframe, self.miningpoolname, *self.choices)
        Label(self.mainframe, text="Mining Pool: ").grid(row = 3, column = 1)
        popupMenu.grid(row = 3, column = 2)
        Label(self.mainframe, text="Hashrate ").grid(row = 4, column = 1)
        Label(self.mainframe, text=raven_miner.balance).grid(row = 4, column = 2)
        Label(self.mainframe, text="Balance ").grid(row = 5, column = 1)
        Label(self.mainframe, text=raven_miner.hashrate).grid(row = 5, column = 2)

        #  track changes
        self.miningpoolname.trace('w', self.change_dropdown)

        self.start_mining_btn = Button(self.mainframe, text = "Start Mining", command = lambda: self.raven_miner.start_mining(self.walletaddr.get())).grid(row = 6, column = 1)
        self.stop_mining_btn = Button(self.mainframe, text = "Stop Mining", command = lambda: self.raven_miner.stop_mining()).grid(row = 6, column = 2)
        self.save_settings_btn = Button(self.mainframe, text = "Save", command = lambda: self.raven_miner.save_settings(self.walletaddr.get())).grid(row = 7, column = 1)
        self.open_settings_window = Button(self.mainframe, text="Settings", command = self.settings_window.open).grid(row = 8, column = 1)

        self.load_settings()
    
    def populate_mining_pool_dropdown(self):
        pools = []
        for key in self.raven_miner.mining_pools:
            pools.append(key)
        return pools
    
    # Button functions
    def change_dropdown(self, *args):
        self.raven_miner.mining_pool = self.raven_miner.mining_pools[self.miningpoolname.get()]
        print( self.miningpoolname.get() )

    def load_settings(self):
        # Load settings
        # init file if it doesn't exist and populate it with blank entries
        # TODO: Inefficient
        if not os.path.isfile("data.pkl"):
            f = open("data.pkl", "w")
            f.close()
            self.raven_miner.mining_pool = self.raven_miner.mining_pools['Ravenpool']
            self.raven_miner.save_settings(self.walletaddr.get())

        a_file = open("data.pkl", "rb")
        output = pickle.load(a_file)
        a_file.close()

        print(output)
        # Populate fields
        self.walletaddr.set(output['wallet'])
        self.minerpath.set(output['minerpath']) # set the default option
        self.miningpoolname.set(output['miningpoolname']) # set the default option
        self.raven_miner.mining_pool = self.raven_miner.mining_pools[output['miningpoolname']]

