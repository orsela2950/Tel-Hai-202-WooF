import threading
from queue import Queue
import fastapi
import hashlib
import json

class Ddos():
    def __init__(self):
        self._size = 10
        self._timeout = 5 #sec before request delete from queue
        
        self._lock = threading.Lock() #lock for keep the shared varibles safe
        self._packetsQueue = Queue(maxsize = self._size)
        self._timers = {}

    async def packet_into_stuck(self, request: fastapi.Request):
        """Get request and check if the request is part of Ddos attack

        Args:
            request (fastapi.Request): the request to check (as recieved from client)

        Returns:
            (Bool,String): true if there is a Ddos attack,false if isn't. string for info about the attack
        """

        
        
        with self._lock:
            if not self._packetsQueue.empty(): #check if queue is empty
                # Convert the queue to a list
                list_queue = list(self._packetsQueue.queue)
                
                # Iterate over the reversed list (from newest to oldest)
                for packet in reversed(list_queue):
                    try:
                        # Check if the body is not empty
                        if await packet.body():
                            diff = await self.compare_payloads(packet.json(), request.json())
                            print(diff[1])
                            return (True,f"Payloads are identical: {json.dumps(await request.json(), sort_keys=True)}") if diff[0] else (False,None) 
                    except Exception as e:
                        print(f"Error processing packet: {str(e)}")
            
            #if queue is full pop the first in queue, first in first out
            if self._packetsQueue.full():
                self._packetsQueue.get()
            
            self._packetsQueue.put(request)

            # Set a timer for other packets with a delay of "self._timeout" seconds
            timer = threading.Timer(self._timeout, self.handle_packet_lifetime, args=(request,))
            self._timers[request] = timer
            timer.start()
            return False,None

    def handle_packet_lifetime(self, request: fastapi.Request):
        with self._lock:
            try:
                # Remove the specific packet from the queue
                self._packetsQueue.queue.remove(request)
            except ValueError:
                pass

            # Remove the specific timer from the dictionary
            if request in self._timers:
                timer = self._timers.pop(request)
                timer.cancel()
                
    async def compare_payloads(self,request_body1, request_body2):

        try:
            body1 = await request_body1
            body2 = await request_body2
        except Exception as e:
            # Handle the exception
            return f"Error getting JSON: {str(e)}"

        # Convert dictionaries to JSON strings
        json_body1 = json.dumps(body1, sort_keys=True)
        json_body2 = json.dumps(body2, sort_keys=True)

        # Hash the JSON strings
        hash1 = hashlib.sha256(json_body1.encode()).hexdigest()
        hash2 = hashlib.sha256(json_body2.encode()).hexdigest()

        # Compare the hash values
        if hash1 == hash2:
            return True,"Payloads are identical."
        else:
            return False,"Payloads are different."
        
            