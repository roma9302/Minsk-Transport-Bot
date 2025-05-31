from aiogram import Router, types
from scr.bot.keyboards.reply import main_menu
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


router = Router()

@router.message(CommandStart())  
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет. Это трансортный бот Минска", reply_markup=main_menu)
    
