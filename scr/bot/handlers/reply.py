import scr.bot.transport_data as transport_data
from aiogram import Router, types
import asyncio


router = Router()

async def show_vehicles(message: types.Message, transport_type, init_cache_func, cached_data):
    await init_cache_func()

    vehicles = cached_data
    vehicle_keys = list(vehicles.keys())

    vehicle_list = "\n".join(
        [" | ".join(vehicle_keys[i:i + 5]) for i in range(0, len(vehicle_keys), 5)]
    )

    await message.answer(f"🚍 Доступные {transport_type}:\n{vehicle_list}")


@router.message(lambda msg: msg.text == "🚌 Автобусы")
async def show_all_buses(message: types.Message):
    await show_vehicles(message, "автобусы", transport_data.init_cache_bus, transport_data.cached_bus)


@router.message(lambda msg: msg.text == "🚎 Троллейбусы")
async def show_all_trolleybuses(message: types.Message):
    await show_vehicles(message, "троллейбусы", transport_data.init_cache_trolleybus, transport_data.cached_trolleybus)


@router.message(lambda msg: msg.text == "🚊 Трамваи")
async def show_all_trams(message: types.Message):
    await show_vehicles(message, "трамваи", transport_data.init_cache_tram, transport_data.cached_tram)
