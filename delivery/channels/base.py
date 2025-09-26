from abc import ABC, abstractmethod
from typing import List

class NotificationChannel(ABC):
    """Abstract base class for notification channels - Strategy Pattern"""
    
    @abstractmethod
    def send_notification(self, alert, users: List) -> List:
        """Send notification to users through this channel"""
        pass
    
    @abstractmethod
    def get_channel_type(self) -> str:
        """Return the channel type identifier"""
        pass