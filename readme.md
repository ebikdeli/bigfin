# This Project included e-exchange currencies with tutorials and blog app about money and economy

We use two scripts: The 'price_request' script, requests price of the wanted currencies and
save them into 'redis' every 15 minutes time period. 'into_db' script run every 1 hour and
store every given currency price into database.

We prioritize 'TokenBasedAuthentication' to authenticate users to use our 'API's. But this method does not
authenticate users in oridnary django views. Django views - unlike restframework views = needs to authenticate
'users' by 'session' data.
From above note we should remembre 'DRF documents' that says: "requests in DRF views are not same as default
django views requests".
** But session data could be passed between 'django requests' and 'DRF requests'!
