=====
Usage
=====

Before using `datawrapper` in a project you'll need to get an access token from Datawrapper. See https://app.datawrapper.de/account/api-tokens

To use datawrapper in a project::

    from datawrapper import Datawrapper

    dw = Datawrapper(access_token = "INSERT_YOUR_ACCESS_TOKEN_HERE)

Now you have access to your Datawrapper account.

To view your account info run::
    dw.account_info()


