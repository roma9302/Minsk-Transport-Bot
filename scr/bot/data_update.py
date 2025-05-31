from scr.transport.parser import *
from databases.models import *
import re
from databases.methods import *
import asyncio
from config.settings import url_bus,url_tram,url_trolleybus
import json

bd = DatabaseManager("databases/transport.db")

transport_urls = {1: url_bus, 2: url_trolleybus, 3: url_tram}

bus = []
tram = []
troll = []

async def delete_data():
    await bd.delete_values("tram")
    await bd.delete_values("trolleybus")
    await bd.delete_values("bus")
    await bd.delete_values("bus_routes")
    await bd.delete_values("tram_routes")
    await bd.delete_values("troll_routes")
    

async def append_vehicle(link_num,table_num):
    parser = await TransportParser.create(transport_urls[link_num])
    routes = {title: link for title, link in zip(await parser.get_titles("li", "hexagon"), await parser.get_link("a","hexagon-link"))}
    for number, link in routes.items():
        await bd.add_new(f"{table_num}" ,(f"{number}", f"{link}"))


async def load_vehicle(vehicle_list, table_name):
    data = await bd.load_data_from_db(table_name, Vehicle)
    vehicle_list.extend(data)


async def append_stops(vehicle,table_name):
    parser = await TransportParser.create(vehicle.link)
    
    trip_container_0 = await parser.get_child_titles("h2", parent_tag="div", parent_class="direction", parent_id = "napravlenie-0")
    trip_container_1 = await parser.get_child_titles("h2", parent_tag="div", parent_class="direction", parent_id="napravlenie-1")
    
    try:
        route2 = trip_container_1[0]
    except(IndexError):
        route2 = "None"
        
    try:
        if len(trip_container_0) == 1:
            route1 = trip_container_0[0]
        else:
            route1 = trip_container_1[0]
            route2 = trip_container_1[1]
    except IndexError:
        route1 = "None"
    
    titles_1 = await parser.get_child_titles("li", "stop", "div", "direction", "napravlenie-0")
    titles_2 = await parser.get_child_titles("li", "stop", "div", "direction", "napravlenie-1")
    links = await parser.get_link("a", "stop-link")
    
    if len(titles_1) == 0:
        try:
            titles_1 = await parser.get_element_info_by_index("li","stop","div","direction", 0)
            titles_2 = await parser.get_element_info_by_index("li","stop","div","direction", 1)
        except IndexError:
            titles_1 = []

    data1_json = json.dumps([{title: link} for title, link in zip(titles_1, links[:len(titles_1)])], ensure_ascii=False)
    data2_json = json.dumps([{title: link} for title, link in zip(titles_2, links[len(titles_1):])], ensure_ascii=False)
    
    await bd.add_new(f"{table_name}", (vehicle.number, route1, route2, data1_json, data2_json))


async def start_func_stops(vehicles_data,table_name):
    tasks = [append_stops(vehicle,table_name) for vehicle in vehicles_data]
    await asyncio.gather(*tasks)


async def get_time(link):
    parser_ts1 = await TransportParser.create(link)
    trip_time = await parser_ts1.get_titles("tr", "schedule-section")
    
    parsed_data = {}
    last_hour = None

    pattern = re.compile(r'^(\d*)([А-Яа-яЁё.]+)(\d*)$')
    
    for entry in trip_time:
        entry = entry.strip()
        m = pattern.match(entry)
        if not m:
            continue
        num, marker, digits = m.groups()
        if num:
            hour = int(num)
            last_hour = hour
        else:
            if last_hour is None:
                continue
            hour = last_hour
        
        minutes = [digits[i:i+2] for i in range(0, len(digits), 2)] if digits else []
        
        if hour not in parsed_data:
            parsed_data[hour] = {}
        parsed_data[hour][marker] = minutes
        
    return parsed_data



asyncio.run(delete_data())

asyncio.run(append_vehicle(1,"bus"))
asyncio.run(append_vehicle(2,"trolleybus"))
asyncio.run(append_vehicle(3,"tram"))

asyncio.run(load_vehicle(bus,"bus"))
asyncio.run(load_vehicle(tram,"tram"))
asyncio.run(load_vehicle(troll,"trolleybus"))

asyncio.run(start_func_stops(bus,"bus_routes"))
asyncio.run(start_func_stops(tram, "tram_routes"))
asyncio.run(start_func_stops(troll, "troll_routes"))
