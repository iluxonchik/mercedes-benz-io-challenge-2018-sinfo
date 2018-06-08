# Mercedes Benz IO 2018 Challenge (SINFO) - Winner Solution

Mercedes-Benz IO 2018 challenge given at the SINFO conference.

This is the winner solution of the competition.

I've implemented all of the features, including the two marked as "improvement suggestions".

I ran and tested the application on Linux OS only: `4.14.13-1-ARCH #1 SMP PREEMPT Wed Jan 10 11:14:50 UTC 2018 x86_64 GNU/Linux`.

## Dependencies

This program has no external dependencies. It's implemented in `Python 3`
using only the constructs and functions provided by its standard library.

I purposefully avoided using the (new formatted string literals)[https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-pep498] introduced in `Python 3.6`, so **any** version of `Python 3` should work.

To determine if your local version of `Python 3` is supported, simply run the
tests (described below). If they pass without issues, everything should
work fine.

On my machine, I was using

```
Python 3.6.4 (default, Dec 23 2017, 19:07:07)
[GCC 7.2.1 20171128] on linux
```

## Building/Running The application

```
usage: python3 run.py [-h] -f FILE [-p PORT]

Mercedes-Benz IO TestDrive application. Developed as part of the MB IO
challenge at SINFO 25.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the file containing the JSON dataset.
  -p PORT, --port PORT  Port on which to start the HTTP Server.

```

For example, run the application using the provided datase, simply execute the following command from the project's
root directory:

`python3 run.py -f ./tests/resources/dataset_full.json -p 8081`

After that, you can start making requests to the endpoints at `http://localhost:<port>`

## Running Tests

To run the application tests, simply execute the following command from the project's
root directory:

`python3 -m unittest discover tests`

Note: the tests at `test/test_server.py` use the port `1234`, so either make sure you have that port free or change it to some other value at the `test.test_server.RESTServerTestCase.SERVER_PORT`.

### Checking Test Coverage

If you want to check the coverage, you can use the `coverage.py` tool.
You can install it with `pip`:

```
pip3 install coverage
```

After that, you can use the following one-liner to run all of the
tests and print the coverage summary:

```
coverage run -m unittest discover tests; coverage report -m
```

I recommend you installing `coverage.py` in a virtual environment.

## Additional Comments

I decided to implement the solutions using only what the `Python 3` distribution provides out of the box, without using any external dependencies.

I did this not because I don't know how to to use `pip` or don't know any
libraries that could've helped me, but rather as a result of the motivation that I got from my conversation
with the `MB IO` representative at `SINFO 25`.

What he told me was that many of the front-end developers that they
used to have/interviewed only knew the frameworks (`AngularJS`, `ReactJS`)
and not the language itself (`JavaScript`). He told me that they would fail
at the most basic questions about it (like `==` vs `===`).

Even though using external libraries was explicitly allowed for the back-end
challenge, I decided to go "raw" and only use what Python comes with.

For the most part, I followed the `TDD` approach.

Unfortunately, due to lack of time I did not have enough time (master thesis work and other errands) to implement
more tests. The coverage is good: `97%+`, but if I had more time I would've added more server tests and improve them. The domain test coverage is `100%`.

The distance computation
between two coordinates, as well as the coordinate in polygon test does not take Earth's curvature into consideration.

The last run showed the following coverage:

```
Ran 82 tests in 8.698s

OK
Name                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------
mbio/__init__.py                             0      0   100%
mbio/date/bookingdate.py                    47      0   100%
mbio/date/utils.py                           4      0   100%
mbio/exceptions.py                          18      0   100%
mbio/geo/__init__.py                         0      0   100%
mbio/geo/coordinate.py                      59      0   100%
mbio/geo/exceptions.py                       2      0   100%
mbio/server/__init__.py                      0      0   100%
mbio/server/decorators.py                   20     10    50%   19-30
mbio/server/endpoint.py                      8      0   100%
mbio/server/server.py                      234     36    85%   114, 168-170, 196-197, 212-213, 217-218, 229-232, 249-250, 265-266, 278-282, 293-294, 298-301, 308-309, 327, 332-335, 348
mbio/testdrive.py                          158      0   100%
mbio/utils.py                               14      0   100%
tests/test_bookings.py                     111      0   100%
tests/test_cooridinates.py                  63      0   100%
tests/test_date.py                          85      0   100%
tests/test_list_dealers_by_distance.py     158      0   100%
tests/test_listing.py                      169      0   100%
tests/test_server.py                       146      0   100%
tests/test_test_drive.py                    10      0   100%
tests/test_utils.py                         15      0   100%
----------------------------------------------------------------------
TOTAL                                     1321     46    97%
```

# REST API

All of the endpoint names are located in the `server/enpoint.py` file. The server tests are located at `tests/test_server.py`.

In case I made mistakes in the documentation, please check those two files for relevant information or just contact me.

## List Vehicles
  Fetch a list of vehicles which match a specific `model`, `fuel`, `transmission`, `dealer` or any combination of those.

* **URL**

  `/api/vehicles?dealer=:dealer_id&model=:model&fuel=:fuel&transmission=:transmission`

* **Method:**

  `GET`

*  **URL Params**

   **Optional:**
   `dealer_id=[string]`
   `model=[string]`
   `fuel=[string]`
   `transmission=[string]`

* **Success Response:**
  * **Code:** 200 <br />
    **Content:** List of zero or more vehicles.
    ```
    {
    	"vehicles": [{
    		"id": "768a73af-4336-41c8-b1bd-76bd700378ce",
    		"model": "E",
    		"fuel": "ELECTRIC",
    		"transmission": "AUTO",
    		"availability": {
    			"tuesday": ["1000", "1030"],
    			"monday": ["1000", "1030"]
    		}
    	}, {
    		"id": "875f00fa-9f67-44ea-bb26-75ff375fdd3f",
    		"model": "E",
    		"fuel": "ELECTRIC",
    		"transmission": "AUTO",
    		"availability": {
    			"tuesday": ["1000", "1030"],
    			"monday": ["1000", "1030"]
    		}
    	}]
}
```

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Error message content here" }`

* **Sample Calls:**

```
curl -X GET \
  'http://localhost:8081/api/vehicles?model=E&fuel=electric&transmission=auto&dealer=846679bd-5831-4286-969b-056e9c89d74c'
```
Response:
```
{
    "vehicles": [
        {
            "id": "768a73af-4336-41c8-b1bd-76bd700378ce",
            "model": "E",
            "fuel": "ELECTRIC",
            "transmission": "AUTO",
            "availability": {
                "tuesday": [
                    "1000",
                    "1030"
                ],
                "monday": [
                    "1000",
                    "1030"
                ]
            }
        }
    ]
}
```

```
curl -X GET \
  'http://localhost:8081/api/vehicles?model=E&fuel=electric'
```

```
curl -X GET \
  'http://localhost:8081/api/vehicles/'
```


## Find Closest Dealer With Vehicle
  Return the closest dealer closest to a specified location that has a
  vehicle with cerntain attributes.

* **URL**

  `/api/dealers/closest?latitude=:latitude&longitude=:longitude&model=:model&fuel=:fuel&transmission=:transmission`

* **Method:**

  `GET`

*  **URL Params**

   **Required:**
   `latitude=[float]`
   `longitude=[float]`

   **Optional:**
   `model=[string]`
   `fuel=[string]`
   `transmission=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**  single dealer or `null`

    ```
    {
    "dealer": {
        "id": "bbcdbbad-5d0b-45ef-90ac-3581b997e063",
        "name": "MB Lisboa",
        "latitude": 38.746721,
        "longitude": -9.229837,
        "closed": [
            "sunday",
            "monday"
        ],
        "vehicles": [
            {
                "id": "778a04fd-0a6a-4dc7-92bb-a7517608efc2",
                "model": "A",
                "fuel": "ELECTRIC",
                "transmission": "AUTO",
                "availability": {
                    "tuesday": [
                        "1000",
                        "1030"
                    ],
                    "wednesday": [
                        "1000",
                        "1030"
                    ]
                }
            },
            {
                "id": "893d97bf-5a9d-4926-ace3-39ad0585c912",
                "model": "AMG",
                "fuel": "ELECTRIC",
                "transmission": "AUTO",
                "availability": {
                    "tuesday": [
                        "1000",
                        "1030"
                    ],
                    "wednesday": [
                        "1000",
                        "1030"
                    ]
                }
            },
            {
                "id": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
                "model": "E",
                "fuel": "GASOLINE",
                "transmission": "MANUAL",
                "availability": {
                    "tuesday": [
                        "1000",
                        "1030"
                    ],
                    "wednesday": [
                        "1000",
                        "1030"
                    ]
                }
            },
            {
                "id": "d723b0bd-8eb0-4826-bf5d-44754005d174",
                "model": "AMG",
                "fuel": "GASOLINE",
                "transmission": "AUTO",
                "availability": {
                    "tuesday": [
                        "1000",
                        "1030"
                    ],
                    "wednesday": [
                        "1000",
                        "1030"
                    ]
                }
            }
        ]
    }
}
    ```

    OR

    ```
    {
        "dealer": null
    }
    ```

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Message content here" }`


* **Sample Call:**

  ```
  curl -X GET \
  'http://localhost:8081/api/dealers/closest?latitude=38.187787&longitude=-8.104157&model=amg&fuel=gasoline&transmission=manual'
  ```

  Response:
  ```
  {
    "dealer": {
        "id": "846679bd-5831-4286-969b-056e9c89d74c",
        "name": "MB Albufeira",
        "latitude": 37.104404,
        "longitude": -8.236308,
        "closed": [
            "friday",
            "wednesday"
        ],
        "vehicles": [
            {
                "id": "768a73af-4336-41c8-b1bd-76bd700378ce",
                "model": "E",
                "fuel": "ELECTRIC",
                "transmission": "AUTO",
                "availability": {
                    "tuesday": [
                        "1000",
                        "1030"
                    ],
                    "monday": [
                        "1000",
                        "1030"
                    ]
                }
            },
            {
                "id": "d5d0aabc-c0de-4f38-badc-759f96f5fca3",
                "model": "AMG",
                "fuel": "ELECTRIC",
                "transmission": "AUTO",
                "availability": {
                    "tuesday": [
                        "1000",
                        "1030"
                    ],
                    "monday": [
                        "1000",
                        "1030"
                    ]
                }
            },
            {
                "id": "1cd6eae7-5f6f-42a7-a4ca-de7e498d9ce4",
                "model": "AMG",
                "fuel": "GASOLINE",
                "transmission": "MANUAL",
                "availability": {
                    "tuesday": [
                        "1000",
                        "1030"
                    ],
                    "monday": [
                        "1000",
                        "1030"
                    ]
                }
            }
        ]
    }
}
```

## Get Dealers With Vehicle In A Polygon
  Get the dealers within a polygon that have a vehicle with the specified
  attributes. The polygon can have any shape, and can be any `n-polygon`,
  with `n>=3` (as per its definition).

* **URL**

  `/api/dealers/polygon/`
  ``

  Body:
  ```
  {
  "coordinates": [list],
   "model": [string]
   "fuel": [string],
   "transmission": [string]
}
  ```

Example body:
```
{
  "coordinates": [
                [42.203891, -9.525033],
                [36.800254, -9.349252],
                [37.203849, -5.899545],
                [42.268963, -6.031381]
        ],
   "model": "E",
   "fuel": "gasoline",
   "transmission":"manual"
}
```

Where

```

"coordinates": [
                [42.203891, -9.525033],
                [36.800254, -9.349252],
                [37.203849, -5.899545],
                [42.268963, -6.031381]
        ]


```

Are the vertices of the polygon. In this case, the polygon is composed of 4
vertices: [42.203891, -9.525033], [36.800254, -9.349252], [37.203849, -5.899545] and [42.268963, -6.031381]. The format is the following: `[latitude, longitude]`. So `[42.203891, -9.525033]` means that `latitude = 42.203891` and `longitude = -9.525033`.

* **Method:**

  `POST`

*  **Data Params**

  **Required:**
  `coordinates=[list]` - list of lists. Each list element is a polygon point.


  **Optional:**
  `model=[string]`
  `fuel=[string]`
  `transmission=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** List of dealers wit the specified vehicle inside the polygon or empty list.

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Message content here" }`

* **Sample Calls:**

  ```
  curl -X POST \
    http://localhost:8081/api/dealers/polygon/ \
    -d '{
    "coordinates": [
                  [42.203891, -9.525033],
                  [36.800254, -9.349252],
                  [37.203849, -5.899545],
                  [42.268963, -6.031381]
          ],
     "model": "E",
     "fuel": "gasoline",
     "transmission":"manual"
  }'
  ```

```
{
    "dealers": [
        {
            "id": "bbcdbbad-5d0b-45ef-90ac-3581b997e063",
            "name": "MB Lisboa",
            "latitude": 38.746721,
            "longitude": -9.229837,
            "closed": [
                "sunday",
                "monday"
            ],
            "vehicles": [
                {
                    "id": "778a04fd-0a6a-4dc7-92bb-a7517608efc2",
                    "model": "A",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "893d97bf-5a9d-4926-ace3-39ad0585c912",
                    "model": "AMG",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
                    "model": "E",
                    "fuel": "GASOLINE",
                    "transmission": "MANUAL",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "d723b0bd-8eb0-4826-bf5d-44754005d174",
                    "model": "AMG",
                    "fuel": "GASOLINE",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                }
            ]
        }
    ]
}
```

```
curl -X POST \
  http://localhost:8081/api/dealers/polygon/ \
  -d '{
  "coordinates": [
				        [37.401249, -9.025150],
                [37.431196, -7.463079],
                [36.929082, -8.982059],
                [37.028052, -7.290712]
        ]
}'
```

The polygon formed by coordinates ```[37.401249, -9.025150], [37.431196, -7.463079], [36.929082, -8.982059], [37.028052, -7.290712]``` delimits the Algarve area and the only dealer in that area in the provided dataset is `MB Albufeira`, so the the response will be:

```
{
    "dealers": [
        {
            "id": "846679bd-5831-4286-969b-056e9c89d74c",
            "name": "MB Albufeira",
            "latitude": 37.104404,
            "longitude": -8.236308,
            "closed": [
                "friday",
                "wednesday"
            ],
            "vehicles": [
                {
                    "id": "768a73af-4336-41c8-b1bd-76bd700378ce",
                    "model": "E",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "d5d0aabc-c0de-4f38-badc-759f96f5fca3",
                    "model": "AMG",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "1cd6eae7-5f6f-42a7-a4ca-de7e498d9ce4",
                    "model": "AMG",
                    "fuel": "GASOLINE",
                    "transmission": "MANUAL",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                }
            ]
        }
    ]
}
```
## Find Closest Dealers With Vehicle (Sorted)
  Return the closest dealer closest to a specified location that has a
  vehicle with certain attributes.

* **URL**

  `/api/dealers?latitude=:latitude&longitude=:longitude&model=:model&fuel=:fuel&transmission=:transmission`


* **Method:**

  `GET`

*  **URL Params**

  **Required:**
  `latitude=[float]`
  `longitude=[float]`

  **Optional:**
  `model=[string]`
  `fuel=[string]`
  `transmission=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** List of dealers wit the specified vehicle, sorted from
    the closest one to the the furthest one or empty list.

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Message content here" }`

* **Sample Calls:**

  ```
  curl -X GET \
  'http://localhost:8081/api/dealers?latitude=38.187787&longitude=-8.104157&model=amg&fuel=gasoline'
  ```

```
{
    "dealers": [
        {
            "id": "bbcdbbad-5d0b-45ef-90ac-3581b997e063",
            "name": "MB Lisboa",
            "latitude": 38.746721,
            "longitude": -9.229837,
            "closed": [
                "sunday",
                "monday"
            ],
            "vehicles": [
                {
                    "id": "778a04fd-0a6a-4dc7-92bb-a7517608efc2",
                    "model": "A",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "893d97bf-5a9d-4926-ace3-39ad0585c912",
                    "model": "AMG",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "44a36bfa-ec8f-4448-b4c2-809203bdcb9e",
                    "model": "E",
                    "fuel": "GASOLINE",
                    "transmission": "MANUAL",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "d723b0bd-8eb0-4826-bf5d-44754005d174",
                    "model": "AMG",
                    "fuel": "GASOLINE",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "wednesday": [
                            "1000",
                            "1030"
                        ]
                    }
                }
            ]
        },
        {
            "id": "846679bd-5831-4286-969b-056e9c89d74c",
            "name": "MB Albufeira",
            "latitude": 37.104404,
            "longitude": -8.236308,
            "closed": [
                "friday",
                "wednesday"
            ],
            "vehicles": [
                {
                    "id": "768a73af-4336-41c8-b1bd-76bd700378ce",
                    "model": "E",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "d5d0aabc-c0de-4f38-badc-759f96f5fca3",
                    "model": "AMG",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "1cd6eae7-5f6f-42a7-a4ca-de7e498d9ce4",
                    "model": "AMG",
                    "fuel": "GASOLINE",
                    "transmission": "MANUAL",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                }
            ]
        }
    ]
}
```

```
curl -X GET \
  'http://localhost:8081/api/dealers?latitude=38.187787&longitude=-8.104157&model=amg&fuel=gasoline&transmission=manual'
```

Response:

```
{
    "dealers": [
        {
            "id": "846679bd-5831-4286-969b-056e9c89d74c",
            "name": "MB Albufeira",
            "latitude": 37.104404,
            "longitude": -8.236308,
            "closed": [
                "friday",
                "wednesday"
            ],
            "vehicles": [
                {
                    "id": "768a73af-4336-41c8-b1bd-76bd700378ce",
                    "model": "E",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "d5d0aabc-c0de-4f38-badc-759f96f5fca3",
                    "model": "AMG",
                    "fuel": "ELECTRIC",
                    "transmission": "AUTO",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                },
                {
                    "id": "1cd6eae7-5f6f-42a7-a4ca-de7e498d9ce4",
                    "model": "AMG",
                    "fuel": "GASOLINE",
                    "transmission": "MANUAL",
                    "availability": {
                        "tuesday": [
                            "1000",
                            "1030"
                        ],
                        "monday": [
                            "1000",
                            "1030"
                        ]
                    }
                }
            ]
        }
    ]
}
```

* **Notes**

I decided to go with `POST` instead of `GET`, because the list of coordinates
can get fairly long and `RFC 2616 Section 9.5` suggests this too.

## Create Booking
  Creates a new booking for a vehicle. This request only succeeds if the vehicle is available for booking at the selected time , it's not already booked for that time and it exists.


* **URL**

  `/api/bookings/create/`

  Body:

  ```
  {
  "first_name": :first_name,
  "last_name": :last_name,
  "vehicle_id": :vehicle_id,
  "pickup_date": :pickup_date
}
  ```

* **Method:**

  `POST`

* **Data Params**

  **Required**:
  `first_name=[string]`
  `last_name=[string]`
  `vehicle_id=[string]`
  `pickup_date=[string]`<br />
  `pickup_date` is date in ISO format.



* **Success Response:**

  * **Code:** 201 <br />
    **Content:** the newly created booking

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Error message here." }`

* **Sample Call:**

```
curl -X POST \
  http://localhost:8081/api/bookings/create/ \
  -d '{
  "first_name": "Jayceon",
  "last_name": "Taylor",
  "vehicle_id": "136fbb51-8a06-42fd-b839-c01ab87e2c6c",
  "pickup_date": "2019-04-08T10:30:00"
} '
```

Response:

```
{
    "id": "04e18713-49f5-4022-b1b3-32ed0371dcaa",
    "firstName": "Jayceon",
    "lastName": "Taylor",
    "vehicleId": "136fbb51-8a06-42fd-b839-c01ab87e2c6c",
    "pickupDate": "2019-04-08T10:30:00",
    "createdAt": "2018-03-13T22:06:54.454664"
}
```
## Cancel Booking
Cancel an existing vehicle booking. This requests only succeeds if the booking exists and has not already been canceled. After canceling a booking the vehicle becomes available for that time slot again.

* **URL**

  `/api/bookings/cancel/`

  Body:

  ```
  {
    "booking_id": :booking_id,
    "reason": :reason
  }
  ```

  Example body:

  ```
  {
    "booking_id": "b00d3e76-9605-49c7-910b-03b51679f6d6",
    "reason": "It's my cat's birthday."
  }
  ```

* **Method:**

  `PUT`

* **Data Params**

  **Required**:
  `booking_id=[string]`
  `reason=[string]`

  Example


* **Success Response:**


  * **Code:** 200 <br />
    **Content:** the cancelled booking object

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Error message here." }`

* **Sample Call:**

```
curl -X PUT \
  http://localhost:8081/api/bookings/cancel/ \
  -d '{
  "booking_id": "b00d3e76-9605-49c7-910b-03b51679f6d6",
  "reason": "It'\''s my cat'\''s birthday."
}'
```

Response:

```
{
    "id": "04e18713-49f5-4022-b1b3-32ed0371dcaa",
    "firstName": "Jayceon",
    "lastName": "Taylor",
    "vehicleId": "136fbb51-8a06-42fd-b839-c01ab87e2c6c",
    "pickupDate": "2019-04-08T10:30:00",
    "createdAt": "2018-03-13T22:06:54.454664"
}
```
