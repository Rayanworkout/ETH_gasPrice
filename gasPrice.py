import time
import json
from datetime import datetime
import requests
import tweepy
import schedule


class Notify:
    def __init__(self, twitter_timestamp=False, tg_timestamp=False):
        self.twitter_timestamp = twitter_timestamp
        self.tg_timestamp = tg_timestamp


# Notify class is used to have class attributes instead of global variables
notify = Notify()


def time_delta(now):
    """Function to check how much time
    has passed since last alert"""
    
    return int((time.time() - now) // 60)


def telegram_message(chat_id, message):
    """Function to easily send a message on telegram"""
    
    requests.get("https://api.telegram.org/MY_BOT_TOKEN/sendMessage?chat_id={}&text={}".format(chat_id, message))


def alerts():
    """Getting alerts from the alerts file"""
    with open('alert.json', 'r', encoding='utf8') as file:
        content = json.loads(file.read())
    twitter_alert = content['twitter']
    tg_alert = content['telegram']
    return twitter_alert, tg_alert


def getGas():
    twitter_alert = alerts()[0]
    tg_alert = alerts()[1]
    try:
        # Getting current ethereum price
        request = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd').json()
        eth_price = request['ethereum']['usd']

        API_KEY = 'MY_API_KEY'
        API_KEY_SECRET = 'MY_API_KEY'
        ACCESS_TOKEN = 'MY_API_KEY'
        ACCESS_TOKEN_SECRET = 'MY_API_KEY'

        gasPrice = requests.get('https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey'
                                '=ETHERSCAN_API_KEY').json()

        suggestBaseFee = float(gasPrice['result']['suggestBaseFee'])
        BaseCost = ((suggestBaseFee * 21000) * 0.000000001) * eth_price
        suggestBaseFeeString = f"💵 Base fee   -  {round(int(suggestBaseFee), 0)} gwei ~ {round(BaseCost, 2)} $"

        lowGasPrice = gasPrice['result']['SafeGasPrice']
        lowCost = ((int(lowGasPrice) * 21000) * 0.000000001) * eth_price
        lowGasPriceString = f"🐢  > > > >  {lowGasPrice} gwei ~ {round(lowCost, 2)} $"

        averageGasPrice = int(gasPrice['result']['ProposeGasPrice'])
        averageCost = ((averageGasPrice * 21000) * 0.000000001) * eth_price
        averageGasPriceString = f"🚗️  > > > >  {averageGasPrice} gwei ~ {round(averageCost, 2)} $"

        fastGasPrice = gasPrice['result']['FastGasPrice']
        fastCost = ((int(fastGasPrice) * 21000) * 0.000000001) * eth_price
        fastGasPriceString = f"🚀  > > > >  {fastGasPrice} gwei ~ {round(fastCost, 2)} $"

        if averageGasPrice <= twitter_alert >= 15 and time_delta(notify.twitter_timestamp) >= 300:
            auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            api.update_status(f"✅ #ETH / #USD  {eth_price} $"
                              f"\n\n{lowGasPriceString}\n\n"
                              f"{averageGasPriceString}\n\n"
                              f"{fastGasPriceString}\n\n"
                              f"💵 #Basefee   -  {round(int(suggestBaseFee), 0)} gwei ~ "
                              f"{round(BaseCost, 2)} $\n"
                              f"\n\n➡️ Check also @DefiLlamaBOT\n\n"
                              f"📲️ {tg_alert} #gwei alerts on Telegram ⤵️\n\nhttps://bit.ly/3iyf6vU")

            notify.twitter_timestamp = time.time()

        if averageGasPrice <= tg_alert >= 15 and time_delta(notify.tg_timestamp) >= 120:
            telegram_message("YOUR_TELEGRAM_CHAT_ID", f'✅ ETH / USD  {eth_price} $\n\n{lowGasPriceString}'
                             f'\n\n{averageGasPriceString}\n\n{fastGasPriceString}\n\n'
                             f'{suggestBaseFeeString}')

            notify.tg_timestamp = time.time()

    except Exception as err:
        # Getting exception sent on telegram
        telegram_message("YOUR_TELEGRAM_CHAT_ID", err)
        time.sleep(30)
        pass


telegram_message("YOUR_TELEGRAM_CHAT_ID", f"gasPrice bot ✅ \n\nAlert set on {alerts()[0]} and {alerts()[1]} gwei.")


schedule.every(1).minutes.do(getGas)

while True:
    schedule.run_pending()
    time.sleep(1)
