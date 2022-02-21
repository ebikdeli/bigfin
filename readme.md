# This Project included e-exchange currencies with tutorials and blog app about money and economy

We use two scripts: The 'price_request' script, requests price of the wanted currencies and
save them into 'redis' every 15 minutes time period. 'into_db' script run every 1 hour and
store every given currency price into database.

We prioritize 'TokenBasedAuthentication' to authenticate users to use our 'API's. But this method does not
authenticate users in oridnary django views. Django views - unlike restframework views = needs to authenticate
'users' by 'session' data.
From above note we should remember 'DRF documents' that says: "requests in DRF views are not same as default
django views requests".
** But session data could be passed between 'django requests' and 'DRF requests'!

Although by default 'DRF authtokens' could not used to authenticate users in regular django views, we implemented
a process in 'accounts.logins' module to authenticate users with 'DRF tokens'.

We implemented diffrent methods to add and show 'Ticketing' and 'Answer' in 'ticketing.serializer' module. It's a comperhensive method to be able list, post, retreive and update objects platform-independent.

For test, we simulate 'request' object using RequestFactory and APIRequestFactory.

If we are using 'HyperlinkedModelSerializer' or 'HyperlinkedFields' so we need to send 'request' to
'serializer context', we can access to context data via 'self.context' dictionary in the serializer.
for that purpose it's recommended to override or define 'list' method of VIEWs to be able to always
send 'request' object via Serializer context.

We have used very simple and primitive chat server in this project in the 'chat' app so we are using
'ASGI' as web gateway interface.
