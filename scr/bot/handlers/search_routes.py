from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router, types
from scr.bot.states.vehicle_search import VehicleSearch
from scr.bot.keyboards.inline import generate_routes_keyboard

router = Router()

@router.message(Command("search_bus"))
async def search_bus(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(transport_type="bus")
    await message.answer("🔍 Введите номер автобуса:")
    await state.set_state(VehicleSearch.choosing_route)
    
@router.message(Command("search_troll"))
async def search_troll(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(transport_type="troll") 
    await message.answer("🔍 Введите номер троллейбуса:")
    await state.set_state(VehicleSearch.choosing_route)
    
@router.message(Command("search_tram"))
async def search_tram(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(transport_type="tram") 
    await message.answer("🔍 Введите номер трамвая:")
    await state.set_state(VehicleSearch.choosing_route)

@router.message(VehicleSearch.choosing_route)
async def routes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if (message.text.strip() != "🔍 Доступные остановки:"):
        vehicle_number = message.text.strip()
        await state.update_data(vehicle_number=vehicle_number)
    else:
        vehicle_number = data.get("vehicle_number")
        await message.delete() 
        
    transport_type = data.get("transport_type")
    await state.update_data(vehicle_number=vehicle_number)
    await message.answer(f"🔍 Доступные маршруты: ", reply_markup= await generate_routes_keyboard(vehicle_number,transport_type))
    await state.set_state(VehicleSearch.choosing_stop)
    
