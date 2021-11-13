import requests
from requests import Session
import schedule
import time
import tweepy


# LAUNCH FUNCTION, TO KNOW BOT IS PROPERLY RUNNING

def launch():
    requests.get(https://api.telegram.org/bot:MY_BOT_TOKEN/sendMessage?chat_id=MY_CHAT_ID&text={}"
                    .format("gasPrice bot ✅"))
    print('Bot Running ...')


    
# GETTING PRICE OF ETHEREUM WITH CoinMarketCap API

def getPrice():
    global eth_price
    headers, session = {'Accepts': 'application/json',
                        'X-CMC_PRO_API_KEY': 'MY_API_KEY'}, Session()
    session.headers.update(headers)
    parameters = {'symbol': 'ETH', 'convert': 'USD'}
    response = session.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
                           params=parameters).json()
    price = round(response['data']['ETH']['quote']['USD']['price'], 2)
    eth_price = price

    
# SENDIND REQUESTS TO ETHERSCAN API TO GET CURRENT GASPRICE AND CHECKING IF UNDER OUR SET ALERT


def getGas():
    global twitter_count, tg_count
    try:
        API_KEY = 'MY_API_KEY'
        API_KEY_SECRET = 'MY_API_KEY'
        ACCESS_TOKEN = 'MY_API_KEY'
        ACCESS_TOKEN_SECRET = 'MY_API_KEY'
        
        ETHERSCAN_API_KEY = ''
        
        r = requests.get('https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey'+ETHERSCAN_API_KEY).json()

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

        if averageGasPrice <= 50 and averageGasPrice > 15 and twitter_count != 1:
            auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            api.update_status(f"✅ #ETH / #USD  {eth_price} $\n"
                              f"\n#ETHgasPrice ⤵️"
                              f"\n\n{lowGasPriceString}\n\n"
                              f"{averageGasPriceString}\n\n"
                              f"{fastGasPriceString}\n\n"
                              f"💵 #Basefee   -  {round(int(suggestBaseFee), 0)} gwei ~ {round(BaseCost, 2)} $\n"
                              f"\n\n➡️ Check also @DeFi_Protocols\n\n"
                              f"📲️ 40 #gwei alerts on Telegram ⤵️\n\nhttps://bit.ly/3iyf6vU")
            
            print("Tweet sent, block N°",r['result']['LastBlock'])
            twitter_count = 1

        if averageGasPrice <= 40 and averageGasPrice > 15 and tg_count != 1:
            requests.get(
                "https://api.telegram.org/botMy_Bot_TOKEN/sendMessage?chat_id=MY_CHAT_ID&text={}"
                    .format(f"✅ ETH / USD  {eth_price} $\n\n{lowGasPriceString}\n\n{averageGasPriceString}\n\n"
                            f"{fastGasPriceString}\n\n{suggestBaseFeeString}"))
            tg_count = 1
    except:
        requests.get(
            "https://api.telegram.org/botMy_Bot_TOKEN/sendMessage?chat_id=MY_CHAT_ID&text={}"
                    .format("⚠️ gasPrice bot error, could be Etherscan endpoint or Twitter API"))
        time.sleep(60)


# CREATING A FUNCTION TO RESET TWITTER ALERT COUNT IN ORDER NOT TO SEND MULTIPLE ALERTS
def resetTwitter():
    global twitter_count
    twitter_count = 0

    
# CREATING A FUNCTION TO RESET TELEGRAM ALERT COUNT IN ORDER NOT TO SEND MULTIPLE ALERTS
def reset_Tg():
    global tg_count
    tg_count = 0



tg_count, twitter_count, eth_price = 0, 0, 0

launch(), getPrice()


# EXECUTING FUNCTIONS EVERY X MINUTES

schedule.every(10).seconds.do(getGas)
schedule.every(5).minutes.do(getPrice)
schedule.every(4).hours.do(resetTwitter)
schedule.every(10).minutes.do(reset_Tg)

while True:
    schedule.run_pending()
    time.sleep(1)
