#!/usr/bin/python
# Filename: openEMSstim.py
"""
    openems is a python module that handles
    the creation of EMS stimulation commands
    and connection via USB to an openEMSstim
"""

import serial
from time import sleep
import EMSCommand
import bluepy.btle as btle
version = '0.1'

mac = "00:1E:C0:32:59:AD"
service_uuid = '454d532d-5365-7276-6963-652d424c4531'


class openEMSstim():

    def __init__(self, serial_port, baudrate=9600):
            self.serial_port = serial_port
            self.baudrate = baudrate
            self.sleep_wait = 10
            self.ems_device = None

            # open the connection
            try:
                p = btle.Peripheral(mac)
                srvs = p.getServices()
                srv = next((s for s in srvs if str(s.uuid) == service_uuid), None)
                if srv is not None:
                    # print srv
                    # print str(srv.uuid)
                    self.ems_device = srv.getCharacteristics()[0]
                else:
                    print("Uh oh! I couldn't find the EMS device!")
            except Exception as e:
                print("Looks like something went wrong")

    def send(self, ems_stimulation_command):
            if self.ems_device and ems_stimulation_command:
                self.ems_device.write(str(ems_stimulation_command))
            else:
                print("Problem with command: " + ems_stimulation_command)

    def shutdown(self):
        self.ems_device.close()

# End of openEMSstim.py
