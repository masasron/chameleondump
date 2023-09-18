from abc import ABC, abstractmethod

class BaseDevice(ABC):

    DEFAULT_PIN = None  # Default PIN, should be overridden in child class

    @abstractmethod
    async def exploit(self, client):
        """Exploit method that each device must implement."""
        pass
