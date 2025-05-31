from aiogram import Router, types
from scr.bot.data_update import get_time
from scr.bot.states.vehicle_search import VehicleSearch
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import StateFilter

router = Router()


@router.callback_query(lambda c: c.data.startswith("stops"), StateFilter(VehicleSearch.show_schedule))
async def times(callback_query: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    transport_type = data.get("transport_type")
    vehicle_number = data.get("vehicle_number")
    
    if transport_type == "bus":
        transport_type = "avtobus"
        
    elif transport_type == "troll":
        transport_type = "trollejbus"
        
    elif transport_type == "tram":
        transport_type = "tramvaj"
            
    stops_link = "https://minsk.btrans.by/"+ transport_type + "/" + vehicle_number + "/" + callback_query.data.split("_")[1] 
    parsed_schedule = await get_time(stops_link)

    format_schedule = "\n".join(
        f"🚌 {hours}: " + " | ".join(
            f"{day}: {', '.join(times)}"
            for day, times in schedule.items() if times
        )
        for hours, schedule in parsed_schedule.items()
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚏 К остановкам 🚏", callback_data="back_stops")]
    ])
    
    await callback_query.message.edit_text(f"🔍 Расписание:\n{format_schedule}", reply_markup = keyboard)
    
    
