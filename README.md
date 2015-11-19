# Instagram-API-Endpoints-Tester
Command line interface with oauth automation for testing Instagram's API during development process


# Why use this when Instagram already has a Python library available?

This is in no way intended to replace Instagram's Python library, which is available on Github. The reason I devised this script initially was because I was unable to get the access token script that's included in the Instagram Python library repository to work properly. I played with it for about a day or so then decided to write my own oauth script for grabbing the final authorization access token necessary for making API calls to the various endpoints. 

# What does this script actually do? 

Probably the primary value proposition of this script is that the entire oauth process is automated using Selenium. Unlike the access token script included in the Instagram Python library, the oauth token procurment process here is entirely automated. The automation is intended to streamline the development process so that you don't have to bother with the semi-manual process of getting a new oauth token for every session, but instead can just focus on calling the endpoints and exploring the responses you get back. To that end, the script is a command line interface for Instagram's API and of course all of the request functions included therein are easily extensible and can be adapted to whatever Python-based application you're integrating with Instagram.

**A few things before you get started:** 


1. You need to create and register an app with Instagram. To do that, go here: https://instagram.com/developer/clients/register/
2. Make sure you have Selenium installed. This script has been tested with Selenium version 2.46.0. For more info, go here: http://www.seleniumhq.org/download/
3. The script defaults to Chrome for the oauth automation procedure. If you would like to use another browser supported by Selenium, feel free, but you will have to change the following in the script on line 10: `driver = webdriver.Chrome()` 
    

**Using the script:**

The help option is as follows: 
`$ python InstagramAPICore.py --help`

Will return the following help menu: 

{user_info,user_feed,recent_media,liked_media,search_for_user,get_media_info,get_media_short_code,get_media_search,popular_media,get_comments,likes,tag_info,recently_tagged,tag_search,get_location,recent_media_by_location,location_by_coordinate}
                              ...

Instaram API Core Tester with OAuth automation

positional arguments:
  {user_info,user_feed,recent_media,liked_media,search_for_user,get_media_info,get_media_short_code,get_media_search,popular_media,get_comments,likes,tag_info,recently_tagged,tag_search,get_location,recent_media_by_location,location_by_coordinate}
                        Available commands
    user_info           Get basic information about a user
    user_feed           View the authenticated user's feed.
    recent_media        Get the most recent media published by a user. To get
                        the most recent media published by the owner of the
                        access token, you can use self instead of the user-id.
    liked_media         See the list of media liked by the authenticated user.
                        Private media is returned as long as the authenticated
                        user has permission to view that media. Liked media
                        lists are only available for the currently
                        authenticated user. Optionals for this command are (in
                        this order) max_id and count --> max_id = returns
                        media liked before that id and count = number of media
                        to return.
    search_for_user     Search for a user by name
    get_media_info      Get information about a media object. The returned
                        type key will allow you to differentiate between image
                        and video media. Note: if you authenticate with an
                        OAuth Token, you will receive the user_has_liked key
                        which quickly tells you whether the current user has
                        liked this media item.
    get_media_short_code
                        This endpoint returns the same response as GET /media
                        /media-id. A media object's shortcode can be found in
                        its shortlink URL. An example shortlink is
                        http://instagram.com/p/D/ -- > Its corresponding
                        shortcode is D.
    get_media_search    Search for media in a given area. The default time
                        span is set to 5 days. The time span must not exceed 7
                        days. Defaults time stamps cover the last 5 days. Can
                        return mix of image and video types.
    popular_media       Get a list of what media is most popular at the
                        moment. Can return mix of image and video types.
    get_comments        GET a list of comments on a media object with provided
                        media_id
    likes               Get a list of users who have liked a specific media
                        object.
    tag_info            Get a list of users who have liked a specific media
                        object.
    recently_tagged     Get a list of recently tagged media. Use the optionals
                        max_tag_id and min_tag_id parameters in the pagination
                        response to paginate through these objects and count
                        to specify the number of tagged items return. Example
                        call with optionals: $ python argstest.py
                        recently_tagged brooklyn --MEDIA_COUNT=20
                        --MIN_TAG_ID=1119308990592751135
                        --MAX_TAG_ID=1119309019525588848
    tag_search          Search for tags by name - A valid tag name without a
                        leading #. Example call: $python argstest.py
                        tag_search --tag=brooklyn,dogs,music
    get_location        Get information about a location.
    recent_media_by_location
                        Get a list of recent media objects from a given
                        location.
    location_by_coordinate
                        Search for a location by geographic coordinate.
                        Positional arguments: LAT and LNG. Optional arguments
                        are: --FACEBOOK_PLACES_ID, --FOURSQUARE_ID,
                        --FOURSQUARE_V2_ID, --DISTANCE

optional arguments:
  -h, --help            show this help message and exit
