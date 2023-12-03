import sys
import time

import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher

import proto_struct.vss_data_pb2 as vss_data_pb2


ecal_core.initialize(sys.argv, "Python Protobuf")

pub = ProtoPublisher("vss_data_python_protobuf_topic_1", vss_data_pb2.VssData)
# pub = ProtoPublisher("vss_data_python_protobuf_topic_2", vss_data_pb2.VssData)

cnt = 1

while ecal_core.ok():
  with open("mock_data/mock_data.txt", 'r', encoding='utf-8') as file:
    for line in file:
      vss_code, data = line.rstrip().split()

      protobuf_message = vss_data_pb2.VssData()
      protobuf_message.vss_code = vss_code
      protobuf_message.data = int(data)

      print("Sending message ({})".format(cnt))

      pub.send(protobuf_message)
      
      time.sleep(1)
      
      cnt += 1

ecal_core.finalize()
