from kuksa_client.grpc import VSSClient
from kuksa_client.grpc import Datapoint
import can


speed_filter_weight = 0.6

pre_speed_data = 0


def process_can_message(message):
    global speed_filter_weight
    global pre_speed_data
    
    can_id = message.arbitration_id
    byte_array = message.data
    data = byte_array[0] * 256 + byte_array[1]

    with VSSClient('127.0.0.1', 55555) as client:
        if can_id == 0x0F6:  # speed data (id: 0x0F6)
            # sending speed data [mm/s]
            speed_data = int((1-speed_filter_weight) * pre_speed_data + speed_filter_weight * data)
            
            client.set_current_values({
            'Vehicle.Speed': Datapoint(speed_data),
            })
            
            # sending acceleration data [mm/s^2]
            acceleration_data = (speed_data - pre_speed_data) // 0.1
            
            client.set_current_values({
            'Vehicle.Acceleration.Longitudinal': Datapoint(acceleration_data),
            })
            
            # set pre speed data
            pre_speed_data = speed_data
            

        elif can_id == 0x0D4:  # distance data (id: 0x0D4)
            # sending distance data [cm]
            client.set_current_values({
            'Vehicle.Powertrain.CombustionEngine.Displacement': Datapoint(data),
            })
            
            # sending contact data [TF]
            contact = not bool(data)
        
            client.set_current_values({
            'Vehicle.ADAS.ObstacleDetection.IsWarning': Datapoint(contact),
            })
        

def receive_can_data(interface, channel):
    bus = can.interface.Bus(channel=channel, bustype=interface)

    try:
        while True:
            message = bus.recv()
            process_can_message(message)
            
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    receive_can_data("socketcan", "can0")

