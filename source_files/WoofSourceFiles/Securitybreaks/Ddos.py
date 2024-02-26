import time
import fastapi
import hashlib
from urllib.parse import urlparse, urlunparse, urlunsplit
from Securitybreaks.SecurityBreak import SecurityBreak


async def remove_url_parameters(request_url):
    parsed_url = urlparse(str(request_url))

    # Extract scheme, netloc, path, params, query, fragment
    scheme, netloc, path, params, query, fragment = parsed_url

    # Reconstruct the URL without query parameters
    new_url = str(urlunparse((scheme, netloc, path, '', '', '')))

    return new_url


async def calculate_combined_hash(request: fastapi.Request):
    # Calculate the hash of the request URL
    url = await remove_url_parameters(request.url)
    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()

    # Calculate the hash of the request payload
    payload_hash = hashlib.sha256(await request.body()).hexdigest()

    # Combine the two hash values
    combined_hash_input = f"{url_hash}{payload_hash}".encode('utf-8')

    # Calculate the hash of the combined input
    combined_hash = hashlib.sha256(combined_hash_input).hexdigest()

    return combined_hash


class Ddos(SecurityBreak):
    def __init__(self):
        super().__init__()  # Call parent's constructor
        self._name = "Ddos"
        self._size = 10
        self._timeout = 2  # sec before removing hash from map

        self._hash_time_map = {}  # Map to store hashes and timestamps

    async def check_threats(self, request: fastapi.Request, clientIp: str):
        """Checks for potential DDoS attack using a hash-time map.

        Args:
            request (fastapi.Request): The incoming request to check.

        Returns:
            (bool, str): True and a message if a potential DDoS is detected,
                        False and None otherwise.
        """
        combined_hash = await calculate_combined_hash(request)

        # Check if the hash is already in the maprequest.body()
        if combined_hash in self._hash_time_map:
            if (time.time() - self._hash_time_map[combined_hash]) <= self._timeout:
                await self.add_to_map(combined_hash)
                return True, f"identical payloads and url"
            else:
                del self._hash_time_map[combined_hash]

        await self.add_to_map(combined_hash)
        return False, None

    async def add_to_map(self, combined_hash):
        # Check if the map is full
        if len(self._hash_time_map) >= self._size:
            # If full, remove the least recently used entry (LRU)
            lru_hash = min(self._hash_time_map, key=self._hash_time_map.get)
            del self._hash_time_map[lru_hash]

        # Add the hash and current timestamp to the map
        self._hash_time_map[combined_hash] = time.time()

    def get_name(self):
        return self._name

    def get_json_name(self):  # json type name, and not the name for displaying
        return 'DDOS'
