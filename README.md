# Crypto Coin Converter

A command-line tool to check cryptocurrency prices and convert between coins using the Ompfinex API.

# API provider
Our API provider is [https://www.ompfinex.com/](https://www.ompfinex.com/).
We are very thankful of them, but there are several issues in this API, but don't worry we handled them in our code :).

## How to Use

### Clone the repo
```bash
git clone https://github.com/mohammadsobhanst/crypto-coin-converter/ && cd crypto-coin-converter
```

### Install the requirements
```bash
pip install -r requirements.txt
```

### Check a coin price
```bash
python3 main.py -p {symbol}
```
### Convert a coin to another
```bash
python3 main.py -c {value} {coin} {another_coin}
```
### List of all symbols
```bash
python3 main.py -a
```
