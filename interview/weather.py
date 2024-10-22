from typing import Any, Iterable, Generator
import time
import json

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    station_stat = {}
    for line in events:
        if line['type'] == 'sample':
            station_name = line['stationName']
            timestamp = line['timestamp']
            temp = line['temperature']
            if station_name not in station_stat:
                station_stat[station_name] = (float('-inf'), float('inf'), 0)
            new_max = max(station_stat[station_name][0], temp)
            new_min = min(station_stat[station_name][1], temp)
            new_timestamp = max(station_stat[station_name][2], timestamp)
            station_stat[line['stationName']] = (new_max, new_min, new_timestamp)
            continue

        if line['type'] == 'control':
            if line['command'] != 'snapshot' and line['command'] != 'reset':
                raise ValueError('Please verify input.')

            if not station_stat:
                continue

            if line['command'] == 'snapshot':
                curr_time = time.time()
                snapshot = {}
                latest_timestamp = 0

                for station_name, (max_temp, min_temp, timestamp) in station_stat.items():
                    if timestamp <= curr_time:
                        snapshot[station_name] = {
                            'high': max_temp,
                            'low': min_temp
                        }
                        latest_timestamp = max(latest_timestamp, timestamp)

                response = {
                    'type': 'snapshot',
                    'asOf': latest_timestamp,
                    'stations': snapshot
                }

                yield json.loads(json.dumps(response))
            elif line['command'] == 'reset':
                latest_timestamp = 0
                for _, (_, _, timestamp) in station_stat.items():
                    if timestamp <= curr_time:
                        latest_timestamp = max(latest_timestamp, timestamp)

                station_stat = {}

                response = {
                    'type': 'reset',
                    'asOf': latest_timestamp
                }

                yield json.loads(json.dumps(response))

            continue

        raise ValueError('Please verify input.')
