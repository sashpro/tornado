#TORNADO SERVER

##Task

Implement a web service that given a request with plain text containing urls returns json with urls' titles. See example below. The service should handle 1000 concurrent requests.

Request:
POST /analyze
"Olympics are starting soon; http://www.nbcolympics.com. See more at https://www.olympic.org"

Response:
{
  "links": [
    {
      "url": "http://www.nbcolympics.com",
      "title": "2016 Rio Olympic Games | NBC Olympics"
    },
    {
      "url": "https://www.olympic.org",
      "title": "Olympics | Rio 2016 Schedule, Medals, Results &amp; News"
    }
  ]
}

##Installation

git clone https://github.com/sashpro/tornado
cd tornado
docker-compose up

By defaut server listens at 9000 port


# Testing
Tests execution is done with Tornado's testing framework:
```
docker exec -it tornado python3 -m tornado.testing test
'''
##Result
Hardware: CPU Intel® Core™ i5-7200U CPU @ 2.50GHz × 4, OM 8Gb
Test execution time (1000 connections, 1 link per connection) : ~50s
  
