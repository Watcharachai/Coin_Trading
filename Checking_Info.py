class Info:

    def setKey(self):
        from binance.client import Client
        import config
        import sys
        client = Client(config.api_key, config.api_secret)
        return client

    def getting_info(self):
        status = self.setKey().get_account_status()
        print(status)
        info = self.setKey().get_account()
        print(info)
        balance = self.setKey().get_asset_balance(asset='GBP')
        print(balance)
        status = self.setKey().get_account_status()
        print(status)

    def getting_port(self):
        print(self.setKey().get_all_tickers())

myInfo = Info()
print(myInfo.getting_info())
print(myInfo.getting_port())