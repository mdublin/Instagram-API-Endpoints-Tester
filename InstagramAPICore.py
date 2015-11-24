import json
import requests
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Automating the login and grabbing access code
driver = webdriver.Chrome()

# passing Instagram authorization URL with your client id and redirect uri inserted to drive.get()
# Instagram authorization URL =
# https://api.instagram.com/oauth/authorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=code


# takes user input for creds
def get_creds(userCreds):
    # store user creds in json file
    with open('creds.json', 'r+') as f:
        json.dump(userCreds, f)

    user_name = userCreds.get('user_name')
    password = userCreds.get('password')
    client_id = userCreds.get('client_id')
    client_secret = userCreds.get('client_secret')
    redirect_uri = userCreds.get('redirect_uri')

    # automate final token grab
    CODE = grab_token(user_name, password)
    print ("this is CODE: %s" % CODE)
    final_token, id = Instagram_Request_Access(
        client_id, client_secret, CODE, redirect_uri)
    # store final token and id in json file
    final_token_dict = {'final_token': final_token, 'id': id}
    with open('finalToken.json', 'r+') as ft:
        json.dump(final_token_dict, ft)
        print ("final token and id stored in finalToken.json file")

    return (final_token, id)


def refresh_token():
    """ get new token for session using same creds """
    with open('creds.json') as json_data:
        d = json.load(json_data)

    user_name = d.get('user_name')
    password = d.get('password')
    client_id = d.get('client_id')
    client_secret = d.get('client_secret')
    redirect_uri = d.get('redirect_uri')

    # automate final token grab
    CODE = grab_token(user_name, password)
    print "this is CODE: %s" % CODE
    final_token, id = Instagram_Request_Access(
        client_id, client_secret, CODE, redirect_uri)
    # store final token and id in json file
    final_token_dict = {'final_token': final_token, 'id': id}
    with open('finalToken.json', 'r+') as ft:
        json.dump(final_token_dict, ft)
        print ("final token and id stored in finalToken.json file")

    return (final_token, id)

# when script runs final_token is always grabbed and assigned to current_token
try:
    with open('finalToken.json') as json_data:
        d = json.load(json_data)
        current_token = d.get('final_token')
        user_id = d.get('id')
except:
    pass

# start token grab process from browser


def grab_token(user_name, password, client_id, redirect_uri):
    grab_url = "https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code" % (
        client_id, redirect_uri)
    driver = webdriver.Chrome()
    driver.get(grab_url)

    element = driver.find_element_by_name("username")
    element.send_keys(user_name)
    element = driver.find_element_by_name("password")
    element.send_keys(password)

    driver.find_element_by_xpath('//input[@value = "Log in"]').click()
    print "This is the current response URL: %s" % driver.current_url
    print("\n")
    print("\n")
    access_code_url = driver.current_url
    # split the response URL with the access code @ "="
    access_code_url_split = access_code_url.split('=')
    access_code = access_code_url_split[1]
    print (access_code)
    return access_code


grant_type = 'authorization_code'


def Instagram_Request_Access(
        client_id,
        client_secret,
        CODE,
        authorization_redirect_uri):
    """ requests final access token for the current session as well as user_id. The first string of numbers for the access token is typically the user_id, however this function digs out the user_id from the post response instead of the token """
    global final_token  # always hearing that using global variables is bad, is there another way to make final_token available globally?
    print client_id
    print client_secret
    print CODE
    print authorization_redirect_uri
    print grant_type
    instaOAuthUrl = 'https://api.instagram.com/oauth/access_token'
    payload = {
        'client_id': '%s' % (client_id),
        'client_secret': '%s' % (client_secret),
        'grant_type': 'authorization_code',
        'redirect_uri': '%s' % (authorization_redirect_uri),
        'code': '%s' % (CODE)}
    flag = requests.post(instaOAuthUrl, data=payload).text
    print flag
    json.loads(flag)['access_token']
    final_token = json.loads(flag)['access_token']
    innerDict = json.loads(flag)['user']
    for key, value in innerDict.iteritems():
        id = innerDict['id']
    print "Here's the final Access Token for this session: %s" % final_token
    print "Here's the current User ID for this session: %s" % id
    return (final_token, id)


# USERS ENDPOINTS


def user_info(user_id):
    user_info_url = "https://api.instagram.com/v1/users/%s/?access_token=%s" % (
        user_id, current_token)
    r = requests.get(user_info_url).text
    print(r)
    return r


def user_feed():
    user_feed_url = "https://api.instagram.com/v1/users/self/feed?access_token=%s" % current_token
    r = requests.get(user_feed_url).text
    print(r)
    return r


def recent_media(user_id):
    recent_media_url = "https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s" % (
        user_id, current_token)
    r = requests.get(recent_media_url).text
    print(r)
    return r


def liked_media(*args):
    if not args:
        liked_media_url = "https://api.instagram.com/v1/users/self/media/liked?access_token=%s" % (
            current_token)
    else:
        for i in args:
            max_id = i
            count = i
        payload = {'max_like_id': '%s' % max_id, 'count': '%s' % count}
        liked_media_url = "https://api.instagram.com/v1/users/self/media/liked?access_token=%s" % (
            current_token)
        r = requests.get(liked_media_url, params=payload).text
    print(r)
    return r


def search_for_user(username, *args):
    if not args:
        user_search_url = "https://api.instagram.com/v1/users/search?q=%s&access_token=%s" % (
            username, current_token)
        r = requests.get(user_search_url).text
    else:
        for item in args:
            count = item
        payload = {'COUNT': '%s' % count}
        r = requests.get(user_search_url, params=payload).text
    print(r)
    return r

# NOTE: To request access to this endpoint, please complete this form:
# The ability to POST and DELETE likes, follows and comments is restricted to applications that offer business services
# and not consumer facing apps. Please do not submit a request at this time.https://help.instagram.com/contact/185819881608116
# Modify the relationship between the current user and the target user
#requests.post("https://api.instagram.com/v1/users/{user-id}/relationship?access_token=%s" % current_token)

# MEDIA ENDPOINTS


def get_media_info(media_id):
    get_media_url = "https://api.instagram.com/v1/media/%s?access_token=%s" % (
        media_id, current_token)
    r = requests.get(get_media_url).text
    print(r)
    return r


def get_media_short_code():
    media_short_url = "https://api.instagram.com/v1/media/shortcode/D?access_token=%s" % current_token
    r = requests.get(media_short_url).text
    print(r)
    return r


def get_media_search(LAT, LNG, MIN_TIME, MAX_TIME, *args):
    if not args:
        media_search_url = "https://api.instagram.com/v1/media/search?lat=%s&lng=%s&access_token=%s" % (
            LAT, LNG, current_token)
        payload = {
            'MIN_TIMESTAMP': '%s' % (MIN_TIME),
            'MAX_TIMESTAMP': '%s' % (MAX_TIME)}
    else:
        media_search_url = "https://api.instagram.com/v1/media/search?lat=%s&lng=%s&access_token=%s" % (
            LAT, LNG, current_token)
        for item in args:
            DISTANCE = item
        payload = {
            'MIN_TIMESTAMP': '%s' % (MIN_TIME),
            'MAX_TIMESTAMP': '%s' % (MAX_TIME),
            'DISTANCE': '%s' % (DISTANCE)}
    r = requests.get(media_search_url, params=payload).text
    print(r)
    return r


def popular_media():
    popular_url = "https://api.instagram.com/v1/media/popular?access_token=%s" % current_token
    r = requests.get(popular_url).text
    print(r)
    return r


# COMMENTS ENDPOINTS
# Please note: POST and DELETE requests are restricted to applications
# that offer business services and not consumer facing apps. To see if
# your app meets the qualifications and to apply for POST and DELETE
# permissions, go here: https://instagram.com/developer/review/


def get_comments(media_id):
    comments_url = 'https://api.instagram.com/v1/media/%s/comments?access_token=%s' % (
        media_id, current_token)
    r = requests.get(comments_url).text
    print(r)
    return r

# POST a comment to a media object


def post_comment(comment, media_id):
    comment_url = 'https://api.instagram.com/v1/media/%s/comments' % media_id
    comment = comment.replace(" ", "+")
    text = comment
    payload = {'access_token': '%s' % (current_token), 'text': '%s' % (text)}
    r = requests.post(comment_url, data=payload).text
    print(r)
    return r

# DELETE a comment


def delete_comment(media_id, comment_id):
    del_comment_url = 'https://api.instagram.com/v1/media/%s/comments/%s?access_token=%s' % s(
        media_id, comment_id, current_token)
    r = requests.delete(del_comment_url).text
    print(r)
    return r

# LIKES ENDPOINTS


def likes(media_id):
    likes_url = 'https://api.instagram.com/v1/media/%s/likes?access_token=%s' % (
        media_id, current_token)
    r = requests.get(likes_url).text
    print(r)
    return r


def like_this(media_id):
    like_url = 'https://api.instagram.com/v1/media/%s/likes' % media_id
    payload = {'access_token': '%s' % (current_token)}
    r = requests.post(like_url, data=payload).text
    print(r)
    return r


def unlike_this(media_id):
    dislike_url = 'https://api.instagram.com/v1/media/%s/likes?access_token=%s' % (
        media_id, current_token)
    r = requests.delete(dislike_url).text
    print(r)
    return r


# RELATIONSHIPS ENDPOINTS
def who_user_follows(user_id):
    follows_url = 'https://api.instagram.com/v1/users/%s/follows?access_token=%s' % (
        user_id, current_token)
    r = requests.get(follows_urL).text
    print(r)
    return r


def followers(user_id):
    followers_url = 'https://api.instagram.com/v1/users/%s/followed-by?access_token=%s' % (
        user_id, current_token)
    r = requests.get(followers_url).text
    print(r)
    return r


def follow_requests_by():
    follow_requests_url = 'https://api.instagram.com/v1/users/self/requested-by?access_token=%s' % current_token
    r = requests.get(follow_requests_url).text
    print(r)
    return r


def relationship(user_id):
    relationship_url = 'https://api.instagram.com/v1/users/%s/relationship?access_token=%s' % (
        user_id, current_token)
    r = requests.get(relationship_url).text
    print(r)
    return r


# Modify the relationship between the current user and the target user.
# target_user_id = target_user_id
# class ModifyRelationship(object):
    """ Request access to this endpoint by completing the form for app approval granting POST and DELETE requests modify """
#    modify_url = 'https://api.instagram.com/v1/users/%s/relationship?access_token=%s' % (target_user_id, current_token)

    # def __init__(self, name):
    #    self.name = name

#    def follow(self):
#        url = ModifyRelationship.modify_url
#        payload = {'action': 'follow'}
#        r = requests.post(url, params=payload).text
#        print (r)
#        return r

#    def unfollow(self):
#        url = ModifyRelationship.modify_url
#        payload = {'action': 'unfollow'}
#        r = requests.post(url, params=payload).text
#        print (r)
#        return r

#    def block(self):
#        url = ModifyRelationship.modify_url
#        payload = {'action': 'block'}
#        r = requests.post(url, params=payload).text
#        print (r)
#        return r

#    def approve(self):
#        url = ModifyRelationship.modify_url
#        payload = {'action': 'approve'}
#        r = requests.post(url, params=payload).text
#        print (r)
#        return r

#    def ignore(self):
#        url = ModifyRelationship.modify_url
#        payload = {'action': 'ignore'}
#        r = requests.post(url, params=payload).text
#        print (r)
#        return r


# Modify = ModifyRelationship()
# Modify.follow()
# Modify.unfollow()
# Modify.block()
# Modify.approve()
# Modify.ignore()


# TAGS ENDPOINTS
def tag_info(tag_name):
    tag_info_url = 'https://api.instagram.com/v1/tags/%s?access_token=%s' % (
        tag_name, current_token)
    r = requests.get(tag_info_url).text
    print(r)
    return r


def recently_tagged(tag_name, **kwargs):
    if not kwargs:
        recent_tag_url = 'https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s' % (
            tag_name, current_token)
        r = requests.get(recent_tag_url).text
    else:
        count = kwargs.get('MEDIA_COUNT')
        min_tag = kwargs.get('MIN_TAG_ID')
        max_tag = kwargs.get('MAX_TAG_ID')
        payload = {
            'COUNT': '%s' % count,
            'MIN_TAG_ID': '%s' % min_tag,
            'MAX_TAG_ID': '%s' % max_tag}
        recent_tag_url = 'https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s' % (
            tag_name, current_token)
        r = requests.get(recent_tag_url, params=payload).text
    print(r)
    return r


def tag_search(**kwargs):
    if not kwargs:
        print("Please enter some tags after current_token when calling recently_tagged()")
    else:
        for key, value in kwargs.iteritems():
            tags = value.strip().split(",")
            if len(tags) == 1:
                tag = tags[0]
                tag_search_url = "https://api.instagram.com/v1/tags/search?q=%s&access_token=%s" % (
                    tag, current_token)
                r = requests.get(tag_search_url).text
            else:
                tagslist = []
                for item in tags:
                    item = 'q=' + item + '&'
                    tagslist.append(item)
                    tags = ""
                    for tag in tagslist:
                        tags += tag
                        tag_search_url = "https://api.instagram.com/v1/tags/search?" + tags
                        tag_search_url = tag_search_url + "access_token=" + current_token
                        r = requests.get(tag_search_url).text
    print(r)
    return r

# LOCATIONS ENDPOINTS


def get_location(location_id):
    location_url = "https://api.instagram.com/v1/locations/%s?access_token=%s" % (
        location_id, current_token)
    r = requests.get(location_url).text
    print (r)
    return r


def recent_media_by_location(location_id, *kwargs):
    if not kwargs:
        recent_media_location_url = "https://api.instagram.com/v1/locations/%s/media/recent?access_token=%s" % (
            location_id, current_token)
        r = requests.get(recent_media_location_url)
    else:
        if len(kwargs) < 4:
            print ("Please enter all four parameters when you call this function: MIN_TIMESTAMP, MAX_TIMESTAMP, MIN_ID, MAX_ID")
        else:
            recent_media_location_url = "https://api.instagram.com/v1/locations/%s/media/recent?access_token=%s" % (
                location_id, current_token)
            MIN_TIMESTAMP = kwargs.get('MIN_TIMESTAMP')
            MIN_ID = kwargs.get('MIN_ID')
            MAX_ID = kwargs.get('MAX_ID')
            MAX_TIMESTAMP = kwargs.get('MAX_TIMESTAMP')
            payload = {
                'MIN_TIMESTAMP': '%s' % (MIN_TIMESTAMP),
                'MIN_ID': '%s' % (MIN_ID),
                'MAX_ID': '%s' % (MAX_ID),
                'MAX_TIMESTAMP': '%s' % (MAX_TIMESTAMP)}
            r = requests.get(recent_media_location_url, params=payload).text
    print (r)
    return r


def location_by_coordinate(LAT, LNG, **kwargs):
    if not kwargs:
        coordinate_url = "https://api.instagram.com/v1/locations/search?lat=%s&lng=%s&access_token=%s" % (
            LAT, LNG, current_token)
        r = requests.get(coordinate_url).text
    else:
        coordinate_url = "https://api.instagram.com/v1/locations/search?lat=%s&lng=%s&access_token=%s" % (
            LAT, LNG, current_token)
        for key, value in kwargs.iteritems():
            if 'DISTANCE' in kwargs:
                distance = kwargs.get('DISTANCE')
                if distance > 5000:
                    print (distance)
                    print (
                        "max distance is 5000m, value is reassigned to default of 1000m")
                    distance = 1000
                    coordinate_url = "https://api.instagram.com/v1/locations/search?lat=%s&lng=%s&access_token=%s" % (
                        LAT, LNG, current_token)
                    r = requests.get(coordinate_url).text
                else:
                    pass
                    coordinate_url = "https://api.instagram.com/v1/locations/search?lat=%s&lng=%s&access_token=%s" % (
                        LAT, LNG, current_token)
                    r = requests.get(coordinate_url).text
            if 'FACEBOOK_PLACES_ID' in kwargs:
                fb_places_id = kwargs.get('FACEBOOK_PLACES_ID')
                payload = {
                    'FACEBOOK_PLACES_ID': '%s' % (fb_places_id),
                    'DISTANCE': '%s' % (DISTANCE)}
                r = requests.get(coordinate_url, params=payload).text
            if 'FOURSQUARE_ID' in kwargs:
                foursquare_id = kwargs.get('FOURSQUARE_ID')
                payload = {
                    'FOURSQUARE_ID': '%s' % (foursquare_id),
                    'DISTANCE': '%s' % (DISTANCE)}
                r = requests.get(coordinate_url, params=payload).text
            if 'FOURSQUARE_V2_ID' in kwargs:
                foursquare_v2_id = kwargs.get('FOURSQUARE_V2_ID')
                payload = {
                    'FOURSQUARE_V2_ID': '%s' % (foursquare_v2_id),
                    'DISTANCE': '%s' % (DISTANCE)}
                r = requests.get(coordinate_url, params=payload).text
    print (r)
    return r


# main function
def main():
    """ Main function """
    parser = argparse.ArgumentParser(
        description="Instaram API Core Tester with OAuth automation")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    # USER ENDPOINTS
    # subparser for the user_info command
    user_info_parser = subparsers.add_parser(
        "user_info", help="Get basic information about a user")
    user_info_parser.add_argument(
        "user_id",
        help="The user id of the user you would like to get information about")
    # subparser for the user_feed command
    user_feed_parser = subparsers.add_parser(
        "user_feed", help="View the authenticated user's feed.")
    # subparser for the recent_media command
    recent_media_parser = subparsers.add_parser(
        "recent_media",
        help="Get the most recent media published by a user. To get the most recent media published by the owner of the access token, you can use self instead of the user-id.")
    recent_media_parser.add_argument("user_id", help="user's unique id")
    # subparser for liked_media command
    liked_media_parser = subparsers.add_parser(
        "liked_media",
        help="See the list of media liked by the authenticated user. Private media is returned as long as the authenticated user has permission to view that media. Liked media lists are only available for the currently authenticated user. Optionals for this command are (in this order) max_id and count --> max_id = returns media liked before that id and count = number of media to return.")
    liked_media_parser.add_argument(
        "--max_id",
        type=int,
        help="returns media liked before that id and count = number of media to return")
    liked_media_parser.add_argument(
        "--count", type=int, help="number of media to return")
    # Search for a user by name.
    search_for_user_parser = subparsers.add_parser(
        "search_for_user", help="Search for a user by name")
    search_for_user_parser.add_argument("username", help="username")
    search_for_user_parser.add_argument(
        "--count", type=int, help="number of media to return")

    # MEDIA ENDPOINTS
    # subparser for the get_media_info command
    get_media_info_parser = subparsers.add_parser(
        "get_media_info",
        help="Get information about a media object. The returned type key will allow you to differentiate between image and video media. Note: if you authenticate with an OAuth Token, you will receive the user_has_liked key which quickly tells you whether the current user has liked this media item.")
    get_media_info_parser.add_argument("media_id", help="media object id")
    # subparser for the get_media_short_code command
    get_media_short_code = subparsers.add_parser(
        "get_media_short_code",
        help="This endpoint returns the same response as GET /media/media-id. A media object's shortcode can be found in its shortlink URL. An example shortlink is http://instagram.com/p/D/ -- > Its corresponding shortcode is D.")
    # subparser for get_media_search command
    get_media_search_parser = subparsers.add_parser(
        "get_media_search",
        help="Search for media in a given area. The default time span is set to 5 days. The time span must not exceed 7 days. Defaults time stamps cover the last 5 days. Can return mix of image and video types.")
    get_media_search_parser.add_argument(
        "LAT", help="Latitude of the center search coordinate.")
    get_media_search_parser.add_argument(
        "LNG", help="Longitude of the center search coordinate.")
    get_media_search_parser.add_argument(
        "MIN_TIMESTAMP",
        help="A unix timestamp. All media returned will be taken later than this timestamp.")
    get_media_search_parser.add_argument(
        "MAX_TIMESTAMP",
        help="A unix timestamp. All media returned will be taken earlier than this timestamp.")
    get_media_search_parser.add_argument(
        "--distance",
        type=int,
        help="This is an optional argument. Default is 1km (distance=1000), max distance is 5km.")
    # subparser for popular_media
    popular_media_parser = subparsers.add_parser(
        "popular_media",
        help="Get a list of what media is most popular at the moment. Can return mix of image and video types.")

    # COMMENTS ENDPOINTS
    # subparser for get_comments command
    get_comments_parser = subparsers.add_parser(
        "get_comments",
        help="GET a list of comments on a media object with provided media_id")
    get_comments_parser.add_argument("media_id", help="id of media object")
    # subparser for post_comment command
    # tk
    # subparser for delete_comment command
    # tk

    # LIKES ENDPOINTS
    # subparser for likes command
    likes_parser = subparsers.add_parser(
        "likes", help="Get a list of users who have liked a specific media object.")
    likes_parser.add_argument("media_id", help="id of media object")
    # subparser for like_this command
    # tk
    # subparser for unlike_this command
    # tk

    # TAGS ENDPOINTS
    # subparser for tag_info command
    tag_info_parser = subparsers.add_parser(
        "tag_info", help="Get a list of users who have liked a specific media object.")
    tag_info_parser.add_argument("tag_name", help="any tag with the '#' ")
    # subparser for recently_tagged command
    recently_tagged_parser = subparsers.add_parser(
        "recently_tagged",
        help="Get a list of recently tagged media. Use the optionals max_tag_id and min_tag_id parameters in the pagination response to paginate through these objects and count to specify the number of tagged items return. Example call with optionals: $ python argstest.py recently_tagged brooklyn --MEDIA_COUNT=20 --MIN_TAG_ID=1119308990592751135 --MAX_TAG_ID=1119309019525588848")
    recently_tagged_parser.add_argument("tag_name", help="tag without the '#'")
    recently_tagged_parser.add_argument(
        "--MEDIA_COUNT",
        type=int,
        help="This is an optional. It's the number of media to return")
    recently_tagged_parser.add_argument(
        "--MIN_TAG_ID",
        type=str,
        help="Return media before this min_tag_id.")
    recently_tagged_parser.add_argument(
        "--MAX_TAG_ID",
        type=str,
        help="Return media after this max_tag_id.")
    # subparser for tag_search command
    tag_search_parser = subparsers.add_parser(
        "tag_search",
        help="Search for tags by name - A valid tag name without a leading #. Example call: $python argstest.py tag_search --tag=brooklyn,dogs,music")
    tag_search_parser.add_argument(
        "--tags", help="comma separated tags if more than on tag")

    # LOCATIONS ENDPOINTS
    # subparser for get_location command
    get_location_parser = subparsers.add_parser(
        "get_location", help="Get information about a location.")
    get_location_parser.add_argument("location_id", help="location id string")
    # subparser for recent_media_by_location command
    recent_media_by_location_parser = subparsers.add_parser(
        "recent_media_by_location",
        help="Get a list of recent media objects from a given location.")
    recent_media_by_location_parser.add_argument(
        "location_id", help="location id string")
    recent_media_by_location_parser.add_argument(
        "MIN_TIMESTAMP", help="Return media after this UNIX timestamp")
    recent_media_by_location_parser.add_argument(
        "MAX_TIMESTAMP", help="Return media before this UNIX timestamp")
    recent_media_by_location_parser.add_argument(
        "MIN_ID", help="Return media before this min_id")
    recent_media_by_location_parser.add_argument(
        "MAX_ID", help="Return media after this max_id")
    # subparser for location_by_coordinate command
    location_by_coordinate_parser = subparsers.add_parser(
        "location_by_coordinate",
        help="Search for a location by geographic coordinate. Positional arguments: LAT and LNG (e.g. $ python InstagramAPICore.py location_by_coordinate 40.5949799 -73.9495148). Optional arguments are: --FACEBOOK_PLACES_ID, --FOURSQUARE_ID, --FOURSQUARE_V2_ID, --DISTANCE")
    location_by_coordinate_parser.add_argument(
        "LAT", help="Latitude of the center search coordinate. If used, lng is required.")
    location_by_coordinate_parser.add_argument(
        "LNG", help="Longitude of the center search coordinate. If used, lat is required.")
    location_by_coordinate_parser.add_argument(
        "--FACEBOOK_PLACES_ID",
        help="Returns a location mapped off of a Facebook places id. If used, a Foursquare id and lat, lng are not required.")
    location_by_coordinate_parser.add_argument(
        "--FOURSQUARE_ID",
        help="Returns a location mapped off of a foursquare v1 api location id. If used, you are not required to use lat and lng. Note that this method is deprecated; you should use the new foursquare IDs with V2 of their API.")
    location_by_coordinate_parser.add_argument(
        "--FOURSQUARE_V2_ID",
        help="Returns a location mapped off of a foursquare v2 api location id. If used, you are not required to use lat and lng.")
    location_by_coordinate_parser.add_argument(
        "--DISTANCE", help="Default is 1000m (distance=1000), max distance is 5000.")

    # oauth commands

    refresh_token_parser = subparsers.add_parser(
        "refresh_token",
        help="Get another token for this session using the same client/user credentials.")

    creds_parser = subparsers.add_parser(
        "get_creds",
        help="Command to store your Instagram username, password, client ID, client secret, and redirect URI.")
    creds_parser.add_argument(
        "--user_name",
        help="Instagram username",
        default=None)
    creds_parser.add_argument(
        "--password",
        help="Instagram password for user account.",
        default=None)
    creds_parser.add_argument(
        "--client_id",
        help="app client id",
        default=None)
    creds_parser.add_argument(
        "--client_secret",
        help="app client secret",
        default=None)
    creds_parser.add_argument(
        "--redirect_uri",
        help="redirect URI registered with your client",
        default=None)

    # parsing command line arguments
    arguments = parser.parse_args(sys.argv[1:])

    command_check = arguments.command

    # get_creds command check:
    if command_check == 'get_creds':
        print True
        args = parser.parse_args()

        print "this is args inside get_creds check: %s" % args

        user_name = args.user_name if args.user_name else raw_input(
            "Please submit Instagram username: ")
        password = args.password if args.password else raw_input(
            "Please submit Instagram password: ")
        client_id = args.client_id if args.client_id else raw_input(
            "Please submit client_id: ")
        client_secret = args.client_secret if args.client_secret else raw_input(
            "Please submit client_secret: ")
        redirect_uri = args.redirect_uri if args.redirect_uri else raw_input(
            "Please submit redirect_uri: ")
        user_input_submissions = (
            user_name,
            password,
            client_id,
            client_secret,
            redirect_uri)
        if len(user_input_submissions) > 0:
            userCreds = {
                'user_name': user_name,
                'password': password,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri}
            print "This is userCreds dict: %s" % userCreds
            get_creds(userCreds)

    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "user_info":
        userinfo = user_info(**arguments)
    elif command == "user_feed":
        userfeed = user_feed(**arguments)
    elif command == "recent_media":
        recentmedia = recent_media(**arguments)
    elif command == "liked_media":
        likedmedia = liked_media(**arguments)
    elif command == "search_for_user":
        searchfor_user == search_for_user(**arguments)
    elif command == "get_media_id":
        mediaid = get_media_id(**arguments)
    elif command == "get_media_info":
        mediainfo = get_media_info(**arguments)
    elif command == "get_media_short_code":
        mediashort_code = get_media_short_code(**arguments)
    elif command == "get_media_search":
        mediasearch = get_media_search(**arguments)
    elif command == "popular_media":
        popularmedia = popular_media(**arguments)
    elif command == "get_comments":
        getcomments = get_comments(**arguments)
    # insert elif for COMMENTS and LIKES ENDPOINTS POST and DELETE requests
    elif command == "tag_info":
        taginfo = tag_info(**arguments)
    elif command == "recently_tagged":
        recentlytagged = recently_tagged(**arguments)
    elif command == "tag_search":
        tagsearch = tag_search(**arguments)
    elif command == "get_location":
        getlocation = get_location(**arguments)
    elif command == "recent_media_by_location":
        recentmedia_by_location = recent_media_by_location(**arguments)
    elif command == "location_by_coordinate":
        locationbycoordinate = location_by_coordinate(**arguments)
    # oauth checks
    elif command == "get_creds":
        pass
    elif command == "refresh_token":
        refreshtoken = refresh_token(**arguments)

if __name__ == "__main__":
    main()
