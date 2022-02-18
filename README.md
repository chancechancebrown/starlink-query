

# Blue Onion Data Engineering Takehome
> This application injests data from Starlink API (flat files, not directly) and creates a queryable database
## Running the app
```
docker-compose up --build
```
## Querying the data
>There are 2 different methods currently available for query: Finding the position of a satellite and finding a satellite closest to a given set of latitude, longitude coordinates. With both, you may specify a time when querying via the API

The examples we will use here are ID = 5eed7716096e590006985803, date = 2021-13-18 16:54 for the satellite position and position = (-51,44), date = 2021-13-18 16:54 for closest satellite.

Using curl:

```
curl -X GET "localhost:3333/satellite/5eed7716096e590006985803" (most recent time)
curl -X GET "localhost:3333/satellite/5eed7716096e590006985803/2021-13-18%16:54"

curl -X GET "localhost:3333/position/(-51,44)"
curl -X GET "localhost:3333/position/(-51,44)/2021-13-18%16:54"
```

Using a browser:
```
http://localhost:3333/satellite/5eed7716096e590006985803 (most recent time)
http://localhost:3333/satellite/5eed7716096e590006985803/2022-02-18%2016:54:31.514316

http://localhost:3333/position/(-51,44)
http://localhost:3333/position/(-51,44)/2021-13-18%16:54
```


