import argparse
import requests
from utilities.readable_number import readable_number


""" We are so thankful of https://www.ompfinex.com for providing api to us.
"""

""" This part of code will add arguments to our project.
    For example if you want to see the price of something you can use '-p {symbol}' command.
"""

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--price', 
                    metavar="SYMBOL",
                    type=str, 
                    help="Usage: -p [coin-symbol] (e.g -p BTC, -p ETH, etc).")

parser.add_argument('-a', '--all',
                    action="store_true",
                    help="This gives you all of the coins symbols.")

parser.add_argument('-c', '--convert',
                    nargs=3,
                    metavar=("VALUE", "FROM", "TO"),
                    help="This will convert two coins to each other. Usage: -c 100 BTC BNB")

args = parser.parse_args()


if args.all:
    """ This part of code will ask all of the coin symbols from the api.
    """
    lists = "https://api.ompfinex.com/v2/currencies"
    list_response = requests.get(lists)
    list_content = list_response.json()
    symbols = [id["id"] for id in list_content["data"]]
    counter = 0
    for coin in symbols:
        print(coin, end=", ") # we are spliting every 10 symbols with ','
        counter += 1
        if counter % 10 == 0:
            print("\n")
    print("\n")
    
    
if args.price:
    price = f"https://api.ompfinex.com/v3/currency/{args.price}"
    
    price_response = requests.get(price)
    price_content = price_response.json()
    price_status = price_response.status_code
    
    if price_status == 200:
        markets = price_content["data"]["markets"]
        has_usdt = "USDT" in markets
        # We are checking this because some coins doesn't any markets! (e.g IRR)
        if markets:
            if has_usdt:
                print(f"The price of {args.price} is:", readable_number(markets["USDT"]['last_price']['buy']))
        
            # some coins doesn't have usdt price (like USDT itself or USDC, this is because
            # of that api we are using.)
            elif args.price.upper() == "USDT":
                print(f"The price of USDT is: {readable_number(markets['IRR']["last_price"]['buy'][:-1])}")
                
            else:
                print("We couldn't find any usdt price for this coin...")
    
        else:
            print(f"We don't have any markets for {args.price} :)")
    
    elif price_status == 422:
        print("We couldn't find your coin. For more information use -a command.")
    
    elif price_status == 500:
        print("Opps! the api is down, please try again few minutes later. or check: https://www.ompfinex.com/")
    
    else:
        print("Something unknown happend. Please try again.")



if args.convert:
    # don't forget our request is something like -c 100 BNB BTC
    from_coin = f"https://api.ompfinex.com/v3/currency/{args.convert[1]}"
    to_coin = f"https://api.ompfinex.com/v3/currency/{args.convert[2]}"
    
    from_coin_response, to_coin_response = requests.get(from_coin), requests.get(to_coin)
    from_coin_content, to_coin_content = from_coin_response.json(), to_coin_response.json()
    from_markets, to_markets = from_coin_content["data"]["markets"], to_coin_content["data"]["markets"]
    
    from_has_usdt = "USDT" in from_markets
    to_has_usdt = "USDT" in to_markets
    
    
    if from_coin_response.status_code == 200 and to_coin_response.status_code == 200:
        if from_markets and to_markets:
            if from_has_usdt and to_has_usdt:
                # this part will give us this knowledge how much of the first coin equals to second coin.
                fromcoin_per_tocoin = float(from_markets["USDT"]["last_price"]["buy"]) / float(to_markets["USDT"]["last_price"]['buy'])
                # 100 {first symbol} equals to how much {second symbol}? this part will tell us this.
                converted = fromcoin_per_tocoin * float(args.convert[0])
                print(f"{readable_number(args.convert[0])} {args.convert[1]} equals to {readable_number(str(converted))} {args.convert[2]}.")
            
            elif args.convert[1].upper() == "USDT" and to_has_usdt:
                converted = float(args.convert[0]) / float(to_markets["USDT"]["last_price"]['buy'])
                print(f"{readable_number(args.convert[0])} USDT equals to {readable_number(str(converted))} {args.convert[2]}.")
                
            elif from_has_usdt and args.convert[2].upper() == "USDT":
                converted = float(args.convert[0]) * float(from_markets["USDT"]["last_price"]['buy'])
                print(f"{readable_number(args.convert[0])} {args.convert[1]} equals to {readable_number(str(converted))} USDT.")
        
            elif args.convert[1].upper() == "USDT" and args.convert[2].upper() == "IRR":
                # This part is specially for the Iranian people to see, how much dollar is in IRT price.
                # We are using "[:-1]" for convert IRR(Rial) to IRT(Toman)
                converted = float(args.convert[0]) * float(from_markets["IRR"]["last_price"]['buy'][:-1])
                print(f"{readable_number(args.convert[0])} USDT equals to {readable_number(str(converted))} IRT.")
            
            
            elif args.convert[1].upper() == "IRR" and args.convert[2].upper() == "USDT":
                converted = float(args.convert[0]) / float(to_markets["IRR"]["last_price"]['buy'][:-1])
                print(f"{readable_number(args.convert[0])} IRT equals to {readable_number(str(converted))} USDT.")
                
                
            elif args.convert[1].upper() == args.convert[2].upper():
                print(f"You can't convert {args.convert[1]} to itself :).")
                
            else:
                print("We are sorry but something bad happend or we can't convert this coin...")
        else:
            print("These coins doesn't have market :).")
    else:
        print("Something bad happend please try again later.")