from databases.models import *
from databases.methods import *



bd = DatabaseManager("databases/transport.db")

cached_bus = {}
cached_trolleybus = {}
cached_tram = {}

cached_bus_routes = {}
cached_troll_routes = {}
cached_tram_routes = {}

async def load(vehicle_type, class_object):
    vehicles = await bd.load_data_from_db(vehicle_type, class_object)
    return {vehicle.number: vehicle for vehicle in vehicles}

async def init_cache_bus():
    global cached_bus
    if not cached_bus: 
        cached_bus = await load("bus", Vehicle) 
        
async def init_cache_trolleybus():
    global cached_trolleybus
    if not cached_trolleybus: 
        cached_trolleybus = await load("trolleybus", Vehicle)

async def init_cache_tram():
    global cached_tram
    if not cached_tram: 
        cached_tram = await load("tram", Vehicle)
        

async def init_cache_bus_routes():
    global cached_bus_routes
    if not cached_bus_routes: 
        cached_bus_routes = await load("bus_routes", Routes)
        
async def init_cache_troll_routes():
    global cached_troll_routes
    if not cached_troll_routes: 
        cached_troll_routes = await load("troll_routes", Routes)
        
        
async def init_cache_tram_routes():
    global cached_tram_routes
    if not cached_tram_routes: 
        cached_tram_routes = await load("tram_routes", Routes)
        
