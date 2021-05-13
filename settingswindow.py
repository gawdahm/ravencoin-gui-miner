from tkinter import *

# TODO: Path isn't saved yet.

class RavenMinerGUISettingsWindow():
    def __init__(self, master, raven_miner):
        self.master = master
        self.window = ""
        self.raven_miner = raven_miner
        return
        
    def open(self):
        if not self.window:
            self.window = Toplevel(self.master)
            self.window.title("Settings")
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
            self.minerpath = StringVar(self.window)

            # Miner Path
            Label(self.mainframe, text="Path to executable: ").grid(row = 1, column = 1)
            miner_path_entry = Entry(self.mainframe, textvariable=self.minerpath).grid(row = 1, column = 2)

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
            self.minerpath.set(self.raven_miner.miner_path)
            self.miningpoolname.set(self.raven_miner.mining_pool.name)
    
    # TODO: Old. Bad. Broken.
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
