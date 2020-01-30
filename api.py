from flask_api import FlaskAPI, exceptions, status
import twitter, json, os

#Global Vars
app = FlaskAPI(__name__)
given_tags = ["openbanking", "apifirst", "devops", "cloudfirst", "microservices", "apigateway", "oauth", "swagger", "raml", "openapis"]
G_MAX_SEARCH = "100"
G_MAX_USERS = 5

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
        print("Error Empty Tag!")
        raise exceptions.NotFound()
        return '', status.HTTP_204_NO_CONTENT

    try:
        result_json = api.GetSearch(raw_query="q="+search_tag+"&result_type=recent&count="+G_MAX_SEARCH, return_json=True)
    except:
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

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
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR            

    #Top 5 followed users
    top_users_json = sorted(data, key = lambda usr: usr['followers'], reverse=True)[:G_MAX_USERS] 

    return { 'result': top_users_json }, status.HTTP_200_OK           
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')    