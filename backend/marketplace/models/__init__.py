print("Marketplace package initialized!")  # ✅ Runs when the package is imported

from .user import CustomUser  # ✅ Ensure CustomUser is imported first
from .vehicle import Vehicle, VehicleBrand, VehicleModel
from .chat import Chat, Message
from .favorite import Favorite
from .notification import Notification
from .review import Review
