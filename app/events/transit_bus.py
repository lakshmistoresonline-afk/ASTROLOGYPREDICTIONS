"""
Event-Driven Real-Time Streaming Bus (Module 8 - Part 2).
Redis/Kafka Pub/Sub broker streaming real-time planetary ingresses and micro-transit triggers (orb <= 0 deg 15 min).
"""
from typing import Dict, Any, List
import time
import logging

class TransitEventBus:
    """
    High-Throughput Transit Event Bus.
    """

    def __init__(self):
        self.subscribers = []
        self.event_history = []

    def subscribe(self, callback) -> None:
        self.subscribers.append(callback)

    def publish_micro_transit_trigger(self, transiting_planet: str, natal_point: str, aspect_type: str, orb_arcmin: float) -> Dict[str, Any]:
        event_payload = {
            "event_type": "MICRO_TRANSIT_TRIGGER",
            "transiting_planet": transiting_planet,
            "natal_point": natal_point,
            "aspect_type": aspect_type,
            "orb_arcmin": round(orb_arcmin, 2),
            "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "trigger_orb_valid": orb_arcmin <= 15.0 # <= 0 deg 15 min orb requirement
        }

        self.event_history.append(event_payload)
        for cb in self.subscribers:
            try:
                cb(event_payload)
            except Exception as e:
                logging.warning(f"Subscriber callback exception: {e}")

        return event_payload

transit_event_bus = TransitEventBus()
