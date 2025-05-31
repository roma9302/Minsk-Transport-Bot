from aiogram import Router, types
from scr.bot.handlers.search_stops import stops
from scr.bot.handlers.search_routes import routes
from scr.bot.states.vehicle_search import VehicleSearch
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


router = Router()

@router.callback_query(lambda c: c.data.startswith("back_stops"))
async def back_stops(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    route_number = data.get("route_number")
    back_callback = CallbackQuery(
        id=callback_query.id,
        from_user=callback_query.from_user,
        message=callback_query.message, 
        chat_instance=callback_query.chat_instance, 
        data=f"route_{route_number}" 
    )
    await state.set_state(VehicleSearch.choosing_stop)
    await stops(back_callback, state) 

@router.callback_query(lambda c: c.data.startswith("back_routes"))
async def back_routes(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(VehicleSearch.choosing_route)
    await routes(callback_query.message, state)



