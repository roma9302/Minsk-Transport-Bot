from aiogram import Router, types
from scr.bot.keyboards.inline import generate_stops_keyboard
from scr.bot.states.vehicle_search import VehicleSearch
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


router = Router()

@router.callback_query(lambda c: c.data.startswith("route_"), StateFilter(VehicleSearch.choosing_stop))
async def stops(callback_query: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    transport_type = data.get("transport_type")
    vehicle_number = data.get("vehicle_number")
    
    route_number = callback_query.data.split("_")[1]
    await state.update_data(route_number=route_number)

    await callback_query.message.edit_text("🔍 Доступные остановки: ", reply_markup = await generate_stops_keyboard(vehicle_number, transport_type, route_number))
    await state.set_state(VehicleSearch.show_schedule)
    
    
@router.callback_query(lambda c: c.data.startswith("page_"))
async def pagination(callback_query: types.CallbackQuery, state: FSMContext):
    new_page = int(callback_query.data.split("_")[1])
    
    data = await state.get_data()
    vehicle_number = data.get("vehicle_number")
    transport_type = data.get("transport_type")
    route_number = data.get("route_number")
    
    keyboard = await generate_stops_keyboard(vehicle_number, transport_type, route_number, new_page)
    
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
