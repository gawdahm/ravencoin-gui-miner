from miningpool import MiningPool

class RavenMiner :
    PROCPATH : str = "./"
    PROCNAME : str = "xmrig"
    balance : str = "0"
    hashrate : str = "0"
    mining_pool : MiningPool
    mining_pools = {
        'Ravenpool' : MiningPool(name = "Ravenpool", url = "https://www.ravenminer.com/api/wallet?address=", balance_field = "balance", hashrate_field = ""),
        '2miners' : MiningPool(name = "2miners", url = "https://btg.2miners.com/api/accounts/", balance_field = "balance", hashrate_field = ""),
    }