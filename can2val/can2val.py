#! /usr/bin/env python3

########################################################################
# Copyright (c) 2023 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License 2.0 which is available at
# http://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
########################################################################

'''
Feeder processing CAN data and sending to KUKSA.val
'''

import can

from kuksa_client.grpc import VSSClient
from kuksa_client.grpc import Datapoint


'''Matching CAN ID to corresponding VSS.
   This is an arbitrary example'''
can_vss_mapping = {0x0F6 : 'Vehicle.Speed',
                   0x0F7 : 'Vehicle.Powertrain.ElectricMotor.Temperature',
                   0x0F8 : 'Vehicle.Chassis.SteeringWheel.Angle'}


def process_can_message(message):
    '''This function processes data from a CAN message
       and writes it to the data broker through the client.'''
    can_id = message.arbitration_id
    byte_array = message.data
    dlc = message.dlc

    '''Reassemble data based on dlc.
       Additional procedure may be required to match the VSS data types.'''
    data = sum(byte_array[i] * (256 ** (dlc - i - 1)) for i in range(dlc))

    with VSSClient('127.0.0.1', 55555) as client:
        client.set_current_values({
            can_vss_mapping[can_id]: Datapoint(data),
        })


def receive_can_data(interface, channel):
    '''This function continuously receives messages from the CAN bus.'''
    bus = can.interface.Bus(channel=channel, bustype=interface)

    try:
        while True:
            message = bus.recv()
            process_can_message(message)
            
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    '''The main function as entry point for the CAN data feeder.'''
    receive_can_data("socketcan", "can0")
