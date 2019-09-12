#!/usr/bin/env python3

import requests
from influxdb import InfluxDBClient
import time

# this script calls the dockerapi to
# get information about running containers
# and puts it in an InfluxDB database


# calling docker api and printing response
def logging(url, api):

    # get request and turn result into json
    dockerApiResult = requests.get(url + api)
    dockerApiJson = dockerApiResult.json()

    # for every container running
    for containers in dockerApiJson:

        # take interesting results and make it a string
        id = containers['Id']
        image = containers['Image']
        state = containers['State']
        status = containers['Status']

        # create valid json to insert. use interesting strings from above
        dump = [
                {
                    "measurement": "docker_image",
                    "tags": {
                        "Id": id,
                        "Image": image
                    },
                    "fields": {
                        "State": state,
                        "Status": status
                    }
                }
            ]

        # write result into influxDB
        influx.write_points(dump)


# dockerhost information
dockerhost = 'http://0.0.0.0:5555/'
apicall = 'containers/json'

# InfluxDB information
influx = InfluxDBClient('localhost', 8086, 'root', 'root', 'docker')

# log every second into a database
if __name__ == '__main__':
    while True:
        logging(dockerhost, apicall)
        time.sleep(1)