# CleanResponseServer
Minimal static webserver for testing etc.


## Example


### Send request to server with CURL
```
curl -d '{"username":"lippe8211"}' -X POST "http://localhost:8080/user/login"
```

### Server responds with following JSON
```
{"message": "OK mister, you are in"}
```

## Configuration (method.url.response)
```
METHOD (post, get, put, delete)
  |
  |-----URL MAPPING (e.g login)
            |
            |------- response (JSON response body)
            |------- responseCode (reponse code)
            |------- responseFile (read JSON response from file instead)
```

Example configuration has some post and get examples. To define a response, you simple define the METHOD follwed by URL matching like a login request url (/login).

Last you define the response body and response code. 

```
{
    "post" : {
        "login": {
            "response": {
                "message": "OK mister, you are in"
            },
            "responseCode": 200
        }
    }
}
```
