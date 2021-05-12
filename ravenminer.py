from miningpool import MiningPool
import subprocess, os, pickle
from sys import platform

class RavenMiner :
    miner_path: str = "./"
    PROCNAME : str = "xmrig"
    wallet_address = ""
    balance : str = "0"
    hashrate : str = "0"
    mining_pools = {
        'Ravenpool' : MiningPool(name = "Ravenpool", url = "https://www.ravenminer.com/api/wallet?address=", balance_field = "balance", hashrate_field = ""),
        '2miners' : MiningPool(name = "2miners", url = "https://btg.2miners.com/api/accounts/", balance_field = "balance", hashrate_field = ""),
    }
    mining_pool : MiningPool

    # TODO: Questionable that this should be included in this class.
    def save_settings(self):
        a_file = open("data.pkl", "wb")
        dictionary_data = {
            'wallet' : self.wallet_address, 
            'miningpoolname' : self.mining_pool.name,
            'minerpath' : self.miner_path,
            }
        pickle.dump(dictionary_data, a_file)
        a_file.close()

    def check_address(self, wallet_address : str):
        if not wallet_address:
            return False
        return True

    def start_mining(self, wallet_address : str):
        if not self.check_address(wallet_address):
            print("Invalid wallet")
            return
        #getminingdata(  )
        
        p = subprocess.Popen(self.miner_path + self.PROCNAME + " --url=cryptonote.social:2222 --user {} --threads=1 --pass='email=runforestrun@airmail.cc'".format(wallet_address), shell=True)
        print("Mining started!")

    def stop_mining(self):
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            os.system('pkill '+ self.PROCNAME)
        elif platform == "win32":
            os.system("taskkill /f /im {}.exe".format(self.PROCNAME))