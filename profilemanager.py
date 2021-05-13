from tkinter import *
import pickle
from enum import Enum
class ProfileModes(Enum):
    ADD_PROFILE = 1
    EDIT_PROFILE = 2

class RavenMinerGUIProfileManager():
    def __init__(self, master, raven_miner):
        self.master = master
        self.mode = ProfileModes.ADD_PROFILE
        self.window = ""
        self.raven_miner = raven_miner
        self.profile_list = {"wallet1" : "Ravenpool", "wallet2" : "2miners"}
        return

    def open(self, on_close_callback):
        if not self.window:
            self.window = Toplevel(self.master)
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.on_close_callback = on_close_callback

            # Grid configuration
            self.mainframe = Frame(self.window)
            self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
            self.mainframe.columnconfigure(0, weight = 1)
            self.mainframe.rowconfigure(0, weight = 1)
            self.mainframe.pack(pady = 100, padx = 100)

            # Create variables
            self.miningpoolname = StringVar(self.window)
            self.walletaddr = StringVar(self.window)

            # Wallet Info
            if self.mode == ProfileModes.EDIT_PROFILE:
                wallet_entry_state = 'readonly'
            elif self.mode == ProfileModes.ADD_PROFILE:
                wallet_entry_state = 'normal'

            self.wallet_entry = Entry(self.mainframe, textvariable=self.walletaddr, state = wallet_entry_state).grid(row = 2, column = 2)
            Label(self.mainframe, text="Wallet Address: ").grid(row = 2, column = 1)


            # Mining pool drop down
            self.choices = self.populate_mining_pool_dropdown()
            self.pool_dropdown = OptionMenu(self.mainframe, self.miningpoolname, *self.choices)
            Label(self.mainframe, text="Mining Pool: ").grid(row = 3, column = 1)
            self.pool_dropdown.grid(row = 3, column = 2)

            Button(self.mainframe, text = "Save", command = lambda: self.add_profile()).grid(row = 4, column = 1)

            # Track changes
            self.miningpoolname.trace('w', self.change_dropdown)

            # Prepopulate fields with currently selected wallet (edit mode) or leave blank/default (add mode)
            if self.mode == ProfileModes.ADD_PROFILE:
                    self.window.title("Add Profile")

                    self.miningpoolname.set(self.choices[0])
            elif self.mode == ProfileModes.EDIT_PROFILE:
                    self.window.title("Edit Profile")
                    self.walletaddr.set(self.raven_miner.wallet_address)
                    self.wallet_entry = Entry(self.mainframe, textvariable=self.walletaddr,  state ='readonly').grid(row = 2, column = 2)
                    self.miningpoolname.set(self.profile_list[self.raven_miner.wallet_address]) # Set default option
    
    def add_profile(self):
        self.profile_list[self.walletaddr.get()] = self.miningpoolname.get()
        self.save_profiles()
        if not self.window == "": # If the window has been initialised/opened
            self.on_closing()
    
    def save_profiles(self):
        a_file = open("data.pkl", "wb")
        dictionary_data = {
            'profiles' : self.profile_list,
            'minerpath' : self.raven_miner.miner_path,
            }
        pickle.dump(dictionary_data, a_file)
        a_file.close()
    
    def populate_mining_pool_dropdown(self):
        pools = []
        for key in self.raven_miner.mining_pools:
            pools.append(key)
        return pools

    def populate_profile_dropdown(self):
        pools = []
        for key in self.profile_list:
            pools.append(key)
        return pools

    def change_dropdown(self, *args):
        self.raven_miner.mining_pool = self.raven_miner.mining_pools[self.miningpoolname.get()]
        print(self.miningpoolname.get())

    def on_closing(self):
        self.window.destroy()
        self.window = ""
        if self.on_close_callback:
            self.on_close_callback()
