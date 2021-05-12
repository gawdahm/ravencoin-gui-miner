from tkinter import *
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
        return
    
    def open(self):
        if not self.window:
            self.window = Toplevel(self.master)
            if self.mode == ProfileModes.ADD_PROFILE:
                    self.window.title("Add Profile")
            elif self.mode == ProfileModes.EDIT_PROFILE:
                    self.window.title("Edit Profile")
                    
            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            Label(self.mainframe, text="Wallet Address: ").grid(row = 2, column = 1)
            wallet_entry = Entry(self.mainframe, textvariable=self.walletaddr).grid(row = 2, column = 2)

            # Mining pool drop down
            self.choices = self.populate_mining_pool_dropdown()
            self.pool_dropdown = OptionMenu(self.mainframe, self.miningpoolname, *self.choices)
            Label(self.mainframe, text="Mining Pool: ").grid(row = 3, column = 1)
            self.pool_dropdown.grid(row = 3, column = 2)

            Button(self.mainframe, text = "Save", command = lambda: self.save_settings()).grid(row = 4, column = 1)

            # Track changes
            self.miningpoolname.trace('w', self.change_dropdown)

            # Populate fields
            self.walletaddr.set(self.raven_miner.wallet_address)
            self.miningpoolname.set(self.raven_miner.mining_pool.name)
    
    def save_settings(self):
        self.raven_miner.wallet_address = self.walletaddr.get()
        # TODO: move save_settings here
        self.raven_miner.save_settings()
        self.on_closing()

    def populate_mining_pool_dropdown(self):
        pools = []
        for key in self.raven_miner.mining_pools:
            pools.append(key)
        return pools
    
    def change_dropdown(self, *args):
        self.raven_miner.mining_pool = self.raven_miner.mining_pools[self.miningpoolname.get()]
        print(self.miningpoolname.get())

    def on_closing(self):
        self.window.destroy()
        self.window = ""
