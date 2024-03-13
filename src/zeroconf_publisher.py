import asyncio
import threading
import socket
import logging
from zeroconf import Zeroconf, ServiceInfo

class ZeroconfPublisher:
  """
  Based on https://stackoverflow.com/questions/37512182/how-can-i-periodically-execute-a-function-with-asyncio
  """

  def __init__(self):
    
    def run_loop(loop: asyncio.AbstractEventLoop, task: asyncio.Task):
      asyncio.set_event_loop(loop)
      loop.run_until_complete(task)
    
    event_loop = asyncio.new_event_loop()
    task = event_loop.create_task(self.__service_registration())

    # daemon=True indicates that thread will finalize when main process finalizes
    self.__executor_thread = threading.Thread(target=lambda : run_loop(event_loop, task), daemon=True)


  def start(self):
    self.__executor_thread.start()
  
  async def __service_registration(self):
    logger = logging.getLogger(__name__)
    while True:
      try:
        zeroconf = Zeroconf()
        # Defines a custom service name '_websocket._http._tcp.local.' and a server (hostname) 'rpi.local' (.local suffix  is mandatory)
        service = ServiceInfo(
          '_http._tcp.local.', 
          '_websocket._http._tcp.local.', 
          8080, 
          addresses=[socket.inet_aton("192.168.0.102")], 
          server="rpi.local",
          host_ttl=10
        )
        await zeroconf.async_register_service(service)
        logger.info('asdasd')
        await asyncio.sleep(10)
      except Exception as ex:
        logger.exception(ex)
        # Prevent infinite loop when: 1: fails to register service 2: fails re-trying it again too soon 3: repeat same scenario
        await asyncio.sleep(10)
