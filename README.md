# Instagram-API-Endpoints-Tester
Command line interface with OAuth automation for testing Instagram's API during development process


# Why use this when there's the Instagram Python library available?

This is in no way intended to replace Instagram's Python library, which is available on Github. The reason I devised this script initially was because I was unable to get the access token script that's included in the Instagram Python library repository to work properly. I played with it for about a day or so then decided to write my own OAuth script for grabbing the final authorization access token necessary for making API calls to the various endpoints. 

# What does this script actually do? 

The primary value proposition of this script is that the entire OAuth process is automated using Selenium. Unlike the access token script included in the Instagram Python library, the OAuth token procurement process here is entirely automated. The automation is intended to streamline the development process so that you don't have to bother with the semi-manual process of getting a new OAuth token for every session, but instead can just focus on calling the endpoints and exploring the responses you get back. To that end, the script is a command line interface for Instagram's API and of course all of the request functions included therein are easily extensible and can be adapted to whatever Python-based application you're integrating with Instagram.

**A few things before you get started:** 


1. You need to create and register an app with Instagram. To do that, go here: https://instagram.com/developer/clients/register/
2. Make sure you have Selenium installed. This script has been tested with Selenium version 2.46.0. For more info, go here: http://www.seleniumhq.org/download/
3. The script defaults to Chrome for the OAuth automation procedure. If you would like to use another browser supported by Selenium, feel free, but you will have to change the following in the script on line 10: `driver = webdriver.Chrome()` 
4. This script uses Instagram's Server-side (Explicit) Flow to obtain an access token using the [OAuth 2.0 protocol](http://tools.ietf.org/html/draft-ietf-oauth-v2-12). To learn more about permissions scope, go here: https://instagram.com/developer/authentication/

**Setting up your user and client credentials for OAuth token-grab process:**

1. Initial setup for this script requires you to provide the following credentials: 
    1. username
    2. password
    3. client id
    4. client secret 
    5. authorization uri

2. Run `$ python InstagramAPICORE.py get_creds` and submit all of the above at the appropriate prompts. The `get_creds` command will store your credentials in the `creds.json` file and trigger Selenium to open an instance of Chrome in order to grab the final OAuth token for your session. The final access token for this session will be stored the `finalToken.json` file. 
3. Instagram's access tokens do not specify an expiration time but typically a token will at least last 24 hours, sometimes longer. When you eventually get an API response that contains `error_type=OAuthAccessTokenError`, run the following command: `$ python InstagramAPICORE.py refresh_token` to obtain a new access token with your original credentials.

**Using the script:**

The help option is as follows: 
`$ python InstagramAPICore.py --help`

An example using the `tag_info` command: 

`$ python InstagramAPICore.py tag_info seattle`

This returns some basic information on the tag "seattle": 

`{"meta":{"code":200},"data":{"media_count":7482177,"name":"seattle"}}`
