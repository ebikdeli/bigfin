# This Project included e-exchange currencies with tutorials and blog app about money and economy

We use two scripts: The 'price_request' script, requests price of the wanted currencies and
save them into 'redis' every 15 minutes time period. 'into_db' script run every 1 hour and
store every given currency price into database.
