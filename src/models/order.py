"""
Order Model for Food Delivery
"""

from datetime import datetime
from typing import Optional


class Order:
    """
    Represents a delivery order in the system
    """
    
    def __init__(self, order_id: str, source: str, destination: str, 
                 delivery_time: float = 0, status: str = 'Pending'):
        """
        Initialize an Order
        
        Args:
            order_id: Unique order identifier
            source: Starting location node ID
            destination: Delivery location node ID
            delivery_time: Estimated delivery time in minutes
            status: Order status (Pending, Assigned, In Transit, Delivered)
        """
        self.order_id = order_id
        self.source = source
        self.destination = destination
        self.delivery_time = delivery_time
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.route = []
        self.distance = 0
    
    def update_status(self, new_status: str) -> None:
        """
        Update order status
        
        Args:
            new_status: New status value
        """
        valid_statuses = ['Pending', 'Assigned', 'In Transit', 'Delivered', 'Cancelled']
        
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        self.status = new_status
        self.updated_at = datetime.now()
    
    def set_route(self, route: list, distance: float) -> None:
        """
        Set the optimized route for this order
        
        Args:
            route: List of node IDs representing the route
            distance: Total distance in km
        """
        self.route = route
        self.distance = distance
    
    def to_dict(self) -> dict:
        """
        Convert order to dictionary
        
        Returns:
            Dictionary representation of the order
        """
        return {
            'order_id': self.order_id,
            'source': self.source,
            'destination': self.destination,
            'delivery_time': self.delivery_time,
            'status': self.status,
            'distance': self.distance,
            'route': self.route,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self) -> str:
        """String representation of the order"""
        return (f"Order(id={self.order_id}, source={self.source}, "
                f"destination={self.destination}, status={self.status}, "
                f"time={self.delivery_time})")
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return (f"Order {self.order_id}: {self.source} → {self.destination} "
                f"({self.status}) - {self.delivery_time} mins")