import threading
import time
import fastapi
import hashlib
import json

class Ddos():
    def __init__(self):
        self._size = 10
        self._timeout = 5  # sec before removing hash from map

        self._hash_time_map = {}  # Map to store hashes and timestamps


    async def packet_into_stuck(self, request: fastapi.Request):
        """Checks for potential DDoS attack using a hash-time map.

        Args:
            request (fastapi.Request): The incoming request to check.

        Returns:
            (bool, str): True and a message if a potential DDoS is detected,
                        False and None otherwise.
        """
        
        # Calculate the hash of the request payload
        payload_hash = hashlib.sha256(await request.body()).hexdigest()

        # Check if the hash is already in the maprequest.body()
        if (payload_hash in self._hash_time_map):
            if (time.time() - self._hash_time_map[payload_hash]) <= self._timeout:
                await self.add_to_map(payload_hash)
                return True, f"identical payloads"
            else:
                del self._hash_time_map[payload_hash]

        await self.add_to_map(payload_hash)
        return False, None

    async def add_to_map(self,payload_hash):
        # Check if the map is full
        if len(self._hash_time_map) >= self._size:
            # If full, remove the least recently used entry (LRU)
            lru_hash = min(self._hash_time_map, key=self._hash_time_map.get)
            del self._hash_time_map[lru_hash]
        
        # Add the hash and current timestamp to the map
        self._hash_time_map[payload_hash] = time.time()