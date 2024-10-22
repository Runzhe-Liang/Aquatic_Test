from . import weather

events_1 = [
    {
      "type": "sample",
      "stationName": "Foster Weather Station",
      "timestamp": 42,
      "temperature": 37.1
    },
    {
        "type": "sample",
        "stationName": "Foster Weather Station",
        "timestamp": 42,
        "temperature": 32.5
    },
    {
      "type": "control",
      "command": "snapshot"
    },
    {
      "type": "control",
      "command": "reset"
    }
]

result_1 = [
    {
      "type": "snapshot",
      "asOf": 42,
      "stations": {
        "Foster Weather Station": {"high": 37.1, "low": 32.5}
      }
    },
    {
      "type": "reset",
      "asOf": 42
    }
]

events_2 = [
    {
      "type": "sample",
      "stationName": "Foster Weather Station",
      "timestamp": 42,
      "temperature": 37.1
    },
    {
        "type": "sample",
        "stationName": "Foster Weather Station",
        "timestamp": 43,
        "temperature": 32.5
    },
    {
        "type": "sample",
        "stationName": "Millennium Station",
        "timestamp": 52,
        "temperature": 34.1
    },
    {
        "type": "control",
        "command": "snapshot"
    },
    {
        "type": "sample",
        "stationName": "Millennium Station",
        "timestamp": 53,
        "temperature": 38.5
    },
    {
        "type": "control",
        "command": "snapshot"
    },
    {
      "type": "control",
      "command": "reset"
    },
    {
      "type": "sample",
      "stationName": "Lake Drive Station",
      "timestamp": 62,
      "temperature": 33.1
    },
    {
        "type": "control",
        "command": "snapshot"
    },
]

result_2 = [
    {
      "type": "snapshot",
      "asOf": 52,
      "stations": {
        "Foster Weather Station": {"high": 37.1, "low": 32.5},
        "Millennium Station": {"high": 34.1, "low": 34.1}
      }
    },
    {
      "type": "snapshot",
      "asOf": 53,
      "stations": {
        "Foster Weather Station": {"high": 37.1, "low": 32.5},
        "Millennium Station": {"high": 38.5, "low": 34.1}
      }
    },
    {
      "type": "reset",
      "asOf": 53
    },
    {
        "type": "snapshot",
        "asOf": 62,
        "stations": {
            "Lake Drive Station": {"high": 33.1, "low": 33.1}
        }
    }
]

def test_1():
    assert result_1 == list(weather.process_events(events_1))

def test_2():
    assert result_2 == list(weather.process_events(iter(events_2)))
