from tkinter import *
import os, pickle
from sys import platform
from settingswindow import RavenMinerGUISettingsWindow

class RavenMinerGUI:
    def __init__(self, master, raven_miner):
        self.master = master
        self.raven_miner = raven_miner
        self.settings_window = RavenMinerGUISettingsWindow(master, self.raven_miner)
        self.master.title("Raven GUI Miner")
    
        # Add a grid
        self.mainframe = Frame(master)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(pady = 100, padx = 100)


        self.start_mining_btn = Button(self.mainframe, text = "Start Mining", command = lambda: self.raven_miner.start_mining(self.walletaddr.get())).grid(row = 6, column = 1)
        self.stop_mining_btn = Button(self.mainframe, text = "Stop Mining", command = lambda: self.raven_miner.stop_mining()).grid(row = 6, column = 2)
        self.open_settings_window = Button(self.mainframe, text="Settings", command = self.settings_window.open).grid(row = 8, column = 1)
        Label(self.mainframe, text="Hashrate ").grid(row = 4, column = 1)
        Label(self.mainframe, text=self.raven_miner.balance).grid(row = 4, column = 2)
        Label(self.mainframe, text="Balance ").grid(row = 5, column = 1)
        Label(self.mainframe, text=self.raven_miner.hashrate).grid(row = 5, column = 2)
        self.load_settings()
    

    def load_settings(self):
        # Load settings
        # init file if it doesn't exist and populate it with blank entries
        # TODO: Inefficient
        if not os.path.isfile("data.pkl"):
            f = open("data.pkl", "w")
            f.close()
            self.raven_miner.mining_pool = self.raven_miner.mining_pools['Ravenpool']
            self.raven_miner.save_settings()

        a_file = open("data.pkl", "rb")
        output = pickle.load(a_file)
        a_file.close()

        print(output)
        # Populate fields
        self.raven_miner.wallet_address = output['wallet']
        self.raven_miner.miner_path = output['minerpath']
        self.raven_miner.mining_pool = self.raven_miner.mining_pools[output['miningpoolname']]

