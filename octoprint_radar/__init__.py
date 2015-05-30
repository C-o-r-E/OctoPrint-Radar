# coding=utf-8
from __future__ import absolute_import

import threading
import socket
from uuid import getnode
from time import sleep

import octoprint.plugin

class Radar(octoprint.plugin.StartupPlugin, octoprint.plugin.ShutdownPlugin):
        sentinel = threading.Event()
        t = None

        def run_radar(self, stop):
                bcast_ip = "255.255.255.255"
                bcast_port = 2050
                bcast_info = (bcast_ip, bcast_port)
                
                mac = getnode()

                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

                self._logger.info("start broadcast")
                
                while(not stop.is_set()):
                        s.sendto("Print Radar " + str(mac), bcast_info)
                        stop.wait(2.0)

                self._logger.info("finished broadcast")

                
        
        def on_after_startup(self):
                self.t = threading.Thread(target=self.run_radar, args=(self.sentinel,))
                self.t.start()
                self._logger.info("started radar")

        def on_shutdown(self):
                self.sentinel.set()
                self._logger.info("shutdown radar")


__plugin_name__ = "Radar"
__plugin_implementation__ = Radar()
