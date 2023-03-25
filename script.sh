echo "$(date +'%Y-%m-%d %H:%M:%S'),
$(curl -s 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&ids=bitcoin&order=market_cap_desc&per_page=100&page=1&sparkline=false' | grep -oE '"current_price":[0-9]+(\.[0-9]+)?' | grep -oE '[0-9]+(\.[0-9]+)?')" >>/home/ec2-user/Projet/bitcoin_price.csv
