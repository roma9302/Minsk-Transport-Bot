from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import scr.bot.transport_data as transport_data
import json


async def generate_routes_keyboard(vehicle_number,transport_type):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[],row_width=1) 
    
    if transport_type == "bus":
        await transport_data.init_cache_bus_routes() 
        vehicle = transport_data.cached_bus_routes
    elif transport_type == "troll":
        await transport_data.init_cache_troll_routes() 
        vehicle = transport_data.cached_troll_routes
    elif transport_type == "tram":
        await transport_data.init_cache_tram_routes() 
        vehicle = transport_data.cached_tram_routes
    
    current_vehicle = vehicle.get(vehicle_number)

    if current_vehicle:
        if current_vehicle.route1 != "None":
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=current_vehicle.route1, callback_data=f"route_1")])  
        if current_vehicle.route2 != "None":
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=current_vehicle.route2, callback_data=f"route_2")])  
    else:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text="❌ Маршруты не найдены", callback_data="no_routes")])  

    return keyboard


async def generate_stops_keyboard(vehicle_number, transport_type, route_number, current_page=1, items_per_page=5):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[], row_width=1)
    
    if transport_type == "bus":
        await transport_data.init_cache_bus_routes() 
        vehicle = transport_data.cached_bus_routes
    elif transport_type == "troll":
        await transport_data.init_cache_troll_routes() 
        vehicle = transport_data.cached_troll_routes
    elif transport_type == "tram":
        await transport_data.init_cache_tram_routes() 
        vehicle = transport_data.cached_tram_routes
    
    current_vehicle = vehicle.get(vehicle_number)
    
    if current_vehicle:
        if current_vehicle.route1 and route_number == "1":
            stops_list = json.loads(current_vehicle.stops1)
        elif current_vehicle.route2 and route_number == "2":
            stops_list = json.loads(current_vehicle.stops2) if current_vehicle.stops2 else json.loads(current_vehicle.stops1)

        start_index = (current_page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_stops = stops_list[start_index:end_index]

        for stop in paginated_stops:
            for stop_name, stop_link in stop.items():
                stop_id = stop_link.split("/")[-1]
                keyboard.inline_keyboard.append(
                    [InlineKeyboardButton(text=stop_name, callback_data=f"stops_{stop_id}")]
                )
        
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text="⬅ Назад", callback_data=f"page_{current_page - 1}") if current_page > 1 else None,
            InlineKeyboardButton(text="Вперед ➡", callback_data=f"page_{current_page + 1}") if end_index < len(stops_list) else None
        ])


        keyboard.inline_keyboard.append([InlineKeyboardButton(text="🗺️ К маршрутам 🗺️", callback_data="back_routes")])

    return keyboard
