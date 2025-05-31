from aiogram.fsm.state import State, StatesGroup

class VehicleSearch(StatesGroup):
    choosing_route = State()
    choosing_stop = State()
    show_schedule = State()
    
    
    
