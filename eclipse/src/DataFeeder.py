import time

from kuksa_client.grpc import VSSClient
from kuksa_client.grpc import Datapoint

cnt = 1

while True:
    with VSSClient('127.0.0.1', 55555) as client:
        client.set_current_values({
            "Vehicle.Speed": Datapoint(cnt),
        })

        cnt += 1
        print("feed")
        time.sleep(1)
