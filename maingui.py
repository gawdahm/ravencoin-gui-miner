from tkinter import *
import os, pickle
from sys import platform
from settingswindow import RavenMinerGUISettingsWindow
from profilemanager import *

class RavenMinerGUI:
    def __init__(self, master, raven_miner):
        self.master = master
        self.raven_miner = raven_miner
        self.settings_window = RavenMinerGUISettingsWindow(master, self.raven_miner)
        self.profile_manager = RavenMinerGUIProfileManager(master, self.raven_miner)
        self.master.title("Raven GUI Miner")
    
        # Add a grid
        self.mainframe = Frame(master)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(pady = 100, padx = 100)

        # Wallet Dropdown
        self.selected_wallet = StringVar(self.master)
        self.wallet_list = ["wallet1", "wallet2", "wallet3"]
        self.wallet_dropdown = OptionMenu(self.mainframe, self.selected_wallet, *self.wallet_list)
        Label(self.mainframe, text="Wallet: ").grid(row = 1, column = 1)
        self.wallet_dropdown.grid(row = 1, column = 2)
        Button(self.mainframe, text = "+", command = self.add_profile).grid(row = 1, column = 3)
        Button(self.mainframe, text = "Edit", command = self.edit_profile).grid(row = 1, column = 4)
        Button(self.mainframe, text = "Del", command = self.settings_window.open).grid(row = 1, column = 5)

        
        # Stats
        Label(self.mainframe, text="Hashrate ").grid(row = 2, column = 1)
        Label(self.mainframe, text=self.raven_miner.balance).grid(row = 2, column = 2)
        Label(self.mainframe, text="Balance ").grid(row = 3, column = 1)
        Label(self.mainframe, text=self.raven_miner.hashrate).grid(row = 3, column = 2)

        self.start_mining_btn = Button(self.mainframe, text = "Start Mining", command = lambda: self.raven_miner.start_mining(self.walletaddr.get())).grid(row = 4, column = 1)
        self.stop_mining_btn = Button(self.mainframe, text = "Stop Mining", command = lambda: self.raven_miner.stop_mining()).grid(row = 4, column = 2)
        self.open_settings_window = Button(self.mainframe, text="Settings", command = self.settings_window.open).grid(row = 5, column = 1)
        self.load_settings()
    
    def add_profile(self):
        self.profile_manager.mode = ProfileModes.ADD_PROFILE
        self.profile_manager.open()

    def edit_profile(self):
        self.profile_manager.mode = ProfileModes.EDIT_PROFILE
        self.profile_manager.open()

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

