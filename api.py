from flask_api import FlaskAPI, status
import twitter, json, os, graypy, logging, time

#Global Vars
app = FlaskAPI(__name__)
given_tags = ["openbanking", "apifirst", "devops", "cloudfirst", "microservices", "apigateway", "oauth", "swagger", "raml", "openapis"]
G_MAX_SEARCH = "100"
G_MAX_USERS = 5

#Loggin Setup (GrayLog)
logger = logging.getLogger('logger')
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s')
logger.setLevel(logging.INFO)
handler = graypy.GELFTCPHandler('graylog', 12201)
logger.addHandler(handler)

#Twitter Setup
api = twitter.Api(consumer_key=os.getenv('consumer_key'),
                  consumer_secret=os.getenv('consumer_secret'),
                  access_token_key=os.getenv('access_token_key'),
                  access_token_secret=os.getenv('access_token_secret'))

# GET THE LAST 100 TWEETS BY GIVEN TAG
# Example GET /tag/devops
@app.route("/tag/<string:search_tag>/")
def GetByTag(search_tag):

    if search_tag is None:
        logger.error("Empty", extra={'function': 'GetByTag', 'latency': 0})
        return '', status.HTTP_204_NO_CONTENT

    try:
        result_json = api.GetSearch(raw_query="q="+search_tag+"&result_type=recent&count="+G_MAX_SEARCH, return_json=True)
    except:
        logger.error("Unknown", extra={'function': 'GetByTag', 'latency': 0})
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

    logger.info(search_tag, extra={'function': 'GetByTag', 'latency': 0})

    return result_json, status.HTTP_200_OK

# GET REQUEST
# Example /highfollower
@app.route("/highfollower")
def HighFollower():

    data = []

    try:
        for tag in given_tags :    
            result_json = api.GetSearch(raw_query="q="+tag+"&result_type=recent&count="+G_MAX_SEARCH, return_json=True)

            for tweet in result_json['statuses'] :
                data.append({
                    "name": tweet['user']['name'],
                    "screen_name": tweet['user']['screen_name'],
                    "followers": tweet['user']['followers_count'],
                    "location": tweet['user']['location'],
                    "created_at": tweet['created_at'],
                    "tweet": tweet['text'],
                    "tag": tag
                })
    except:
        logger.error("Unknown", extra={'function': 'HighFollower', 'latency': 0})
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR            

    #Top 5 followed users
    top_users_json = sorted(data, key = lambda usr: usr['followers'], reverse=True)[:G_MAX_USERS] 

    logger.info(top_users_json, extra={'function': 'HighFollower', 'latency': 0})

    return { 'result': top_users_json }, status.HTTP_200_OK           
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')    