from tkinter import *
import os, pickle
from sys import platform
from settingswindow import RavenMinerGUISettingsWindow
from ravenminer import RavenMiner
from profilemanager import *

class RavenMinerGUI:
    def __init__(self, master, raven_miner : RavenMiner):
        self.master = master
        self.raven_miner = raven_miner
        self.settings_window = RavenMinerGUISettingsWindow(master, self.raven_miner)
        self.profile_manager = RavenMinerGUIProfileManager(master, self.raven_miner)
        self.master.title("Raven GUI Miner")

        # Load settings
        a_file = open("data.pkl", "rb")
        saved_settings = pickle.load(a_file)
        a_file.close()

        self.profile_manager.profile_list = saved_settings['profiles']
        self.raven_miner.wallet_address = list(saved_settings['profiles'].keys())[0] # TODO: Save last used wallet
        self.raven_miner.miner_path = saved_settings['minerpath']
        tmp_mining_pool_name = self.profile_manager.profile_list[self.raven_miner.wallet_address]
        self.raven_miner.mining_pool = self.raven_miner.mining_pools[tmp_mining_pool_name]
    
        # Add a grid
        self.mainframe = Frame(master)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(pady = 100, padx = 100)

        # Wallet Dropdown
        self.selected_wallet = StringVar(self.master)
        self.selected_wallet.set(list(saved_settings['profiles'].keys())[0])
        self.wallet_dropdown = OptionMenu(self.mainframe, self.selected_wallet, *self.profile_manager.profile_list.keys())
        Label(self.mainframe, text="Wallet: ").grid(row = 1, column = 1)
        self.wallet_dropdown.grid(row = 1, column = 2)
        Button(self.mainframe, text = "+", command = self.add_profile).grid(row = 1, column = 3)
        Button(self.mainframe, text = "Edit", command = self.edit_profile).grid(row = 1, column = 4)
        Button(self.mainframe, text = "Del", command = self.del_profile).grid(row = 1, column = 5)
        # Track changes
        self.selected_wallet.trace('w', self.on_wallet_dropdown_change)

        
        # Stats
        Label(self.mainframe, text="Hashrate ").grid(row = 2, column = 1)
        Label(self.mainframe, text=self.raven_miner.balance).grid(row = 2, column = 2)
        Label(self.mainframe, text="Balance ").grid(row = 3, column = 1)
        Label(self.mainframe, text=self.raven_miner.hashrate).grid(row = 3, column = 2)

        self.start_mining_btn = Button(self.mainframe, text = "Start Mining", command = lambda: self.raven_miner.start_mining(self.walletaddr.get())).grid(row = 4, column = 1)
        self.stop_mining_btn = Button(self.mainframe, text = "Stop Mining", command = lambda: self.raven_miner.stop_mining()).grid(row = 4, column = 2)
        self.open_settings_window = Button(self.mainframe, text="Settings", command = self.settings_window.open).grid(row = 5, column = 1)
    
    def add_profile(self):
        self.profile_manager.mode = ProfileModes.ADD_PROFILE
        self.profile_manager.open(self.on_profile_menu_close)
    
    def on_profile_menu_close(self):
        # Update wallet address list
        self.wallet_dropdown.grid_forget()
        self.wallet_dropdown = OptionMenu(self.mainframe, self.selected_wallet, *self.profile_manager.profile_list.keys())
        self.wallet_dropdown.grid(row = 1, column = 2)

    # TODO: Should probably add a warning
    def del_profile(self):
        del self.profile_manager.profile_list[self.selected_wallet.get()]
        self.selected_wallet.set(list(self.profile_manager.profile_list.keys())[0]) # TODO: Would cause a problem when deleting the final key
        # Update dropdown
        self.profile_manager.save_profiles()
        self.on_profile_menu_close()

    def edit_profile(self):
        self.profile_manager.mode = ProfileModes.EDIT_PROFILE
        self.profile_manager.open(self.on_profile_menu_close)

    def on_wallet_dropdown_change(self, *args):
        self.raven_miner.wallet_address = self.selected_wallet.get()


