import requests
from requests import Session
import schedule
import time
import tweepy

# SENDIND REQUESTS TO ETHERSCAN API TO GET CURRENT GASPRICE AND CHECKING IF UNDER OUR SET ALERT


def getGas():
    try:  # GET ETH PRICE WITH COINGECK API
        request = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd').json()
        eth_price = request['ethereum']['usd']

        API_KEY = 'MY_API_KEY'
        API_KEY_SECRET = 'MY_API_KEY'
        ACCESS_TOKEN = 'MY_API_KEY'
        ACCESS_TOKEN_SECRET = 'MY_API_KEY'

        etherscan_api_key = 'MY_API_KEY'

        r = requests.get(f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey"
                         f"={etherscan_api_key}").json()

        suggestBaseFee = float(r['result']['suggestBaseFee'])
        BaseCost = ((suggestBaseFee * 21000) * 0.000000001) * eth_price
        suggestBaseFeeString = f"💵 Base fee   -  {round(int(suggestBaseFee), 0)} gwei ~ {round(BaseCost, 2)} $"

        lowGasPrice = r['result']['SafeGasPrice']
        lowCost = ((int(lowGasPrice) * 21000) * 0.000000001) * eth_price
        lowGasPriceString = f"🐢  > > > >  {lowGasPrice} gwei ~ {round(lowCost, 2)} $"

        averageGasPrice = int(r['result']['ProposeGasPrice'])
        averageCost = ((averageGasPrice * 21000) * 0.000000001) * eth_price
        averageGasPriceString = f"🚗️  > > > >  {averageGasPrice} gwei ~ {round(averageCost, 2)} $"

        fastGasPrice = r['result']['FastGasPrice']
        fastCost = ((int(fastGasPrice) * 21000) * 0.000000001) * eth_price
        fastGasPriceString = f"🚀  > > > >  {fastGasPrice} gwei ~ {round(fastCost, 2)} $"

        if averageGasPrice <= gas_twitter_alert >= 15:
            auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            api.update_status(f"✅ #ETH / #USD  {eth_price} $\n"
                              f"\n#ETHgasPrice ⤵️"
                              f"\n\n{lowGasPriceString}\n\n"
                              f"{averageGasPriceString}\n\n"
                              f"{fastGasPriceString}\n\n"
                              f"💵 #Basefee   -  {round(int(suggestBaseFee), 0)} gwei ~ {round(BaseCost, 2)} $\n"
                              f"\n\n➡️ Check also @DefiLlamaBOT\n\n"
                              f"📲️ {gas_telegram_alert} #gwei alerts on Telegram ⤵️\n\nhttps://bit.ly/3iyf6vU")

            if averageGasPrice <= gas_telegram_alert >= 15:
                requests.get(
                    "https://api.telegram.org/botMy_Bot_TOKEN/sendMessage?chat_id=MY_CHAT_ID&text={}"
                        .format(f"✅ ETH / USD  {eth_price} $\n\n{lowGasPriceString}\n\n{averageGasPriceString}\n\n"
                                f"{fastGasPriceString}\n\n{suggestBaseFeeString}"))
            time.sleep(18000)  # WAIT IN ORDER NOT TO SPAM
    except Exception:
        time.sleep(60)

# EXECUTING FUNCTION EVERY X MINUTES


schedule.every(5).minutes.do(getGas)

while True:
    schedule.run_pending()
    time.sleep(1)
