import pytest
from app.streaming.event_bus import event_bus

def test_sse_event_bus_ingress_publishing():
    ingress = event_bus.publish_ingress_event("Jupiter", old_rashi=2, new_rashi=3, longitude=90.01)

    assert ingress["event_type"] == "PLANETARY_INGRESS"
    assert ingress["planet"] == "Jupiter"
    assert ingress["old_rashi"] == 2
    assert ingress["new_rashi"] == 3
    assert ingress["exact_longitude"] == 90.01

def test_sse_event_bus_kakshya_publishing():
    kakshya = event_bus.publish_kakshya_entry_event("Saturn", rashi=10, kakshya_lord="Jupiter", has_bindu=True)

    assert kakshya["event_type"] == "KAKSHYA_SUBZONE_ENTRY"
    assert kakshya["planet"] == "Saturn"
    assert kakshya["kakshya_lord"] == "Jupiter"
    assert kakshya["has_bav_bindu"] is True
