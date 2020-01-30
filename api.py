from flask_api import FlaskAPI, exceptions, status
import twitter, json, os

app = FlaskAPI(__name__)

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
        result_json = api.GetSearch(raw_query="q="+search_tag+"&result_type=recent&count=100", return_json=True)
    except:
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

    return result_json, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')    