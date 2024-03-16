from aiogram import Bot
from aiogram.fsm import state
from database.db_query_funcs import child_name_id_write, get_child_balance, get_child_name, get_child_trainings, get_trainings_list
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline import back_button, trainig_booking_keyboard, trainig_booking_confirm_keyboard, booking_accept_keyboard, booking_cancel_choose_keyboard, booking_cancel_info_keyboard
from handlers.basic import main_menu_handler
from utils.states import MainStates

async def current_child_save(call: CallbackQuery, bot: Bot, state: FSMContext):
    child_name = call.data
    tg_chat_id = call.message.chat.id
    await child_name_id_write(tg_chat_id, child_name)
    await state.set_state(MainStates.menu_open)
    await main_menu_handler(call.message, state)
    await call.message.delete()

async def back_button_callback(call: CallbackQuery, bot: Bot, state: FSMContext):
    current_state = await state.get_state()
    if current_state == MainStates.confirm_booking:
        await training_booking(call, bot, state)
    elif current_state == MainStates.booking_cancel_confirm:
        await booking_cancel_choose(call, bot, state)
    else:
        await state.set_state(MainStates.menu_open)
        await main_menu_handler(call.message, state)
        await call.message.delete()

async def view_stats(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.view_stats)
    child_name = await get_child_name(call.message.chat.id, table_name='backend_childid')
    trainings_info = await get_child_trainings(child_name)
    text = ''
    for training in trainings_info:
        text += f"Тренировка {training['date']}\n"
        text += f"Время: {training['time']}\n"
        text += f"Тип бассейна: {training['pool_type']}\n"
        text += f"Тренер: {training['trainer_name']}\n\n"
    await call.message.answer(text=f'Информация по последним тренировкам, на которые вы записаны (максимум 10) \n \n{text}', reply_markup=back_button())
    await call.message.delete()

async def view_balance(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.view_balance)
    child_name = await get_child_name(chat_id=call.message.chat.id, table_name='backend_childid')
    result = await get_child_balance(child_name)
    user_balance = result[0]['paid_training_count']
    await call.message.answer(text=f'Остаток оплаченных тренировок на балансе - {user_balance}', reply_markup=back_button())
    await call.message.delete()


async def training_booking(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.choose_training_date)
    child_name = await get_child_name(call.message.chat.id, table_name='backend_childid')
    trainings_list_of_dict = await get_trainings_list(child_name)
    trainings_list = []
    for training in trainings_list_of_dict:
        text = ''
        text += f"{training['date']} "
        text += f"{training['time']} "
        trainings_list.append(text)
    await call.message.answer(text='Выберите тренировку из списка', reply_markup=trainig_booking_keyboard(trainings_list))
    await call.message.delete()


async def booking_info_confirm(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.confirm_booking)
    info = ''
    await call.message.answer(text=f'Полная информация по тренировке \n'
                                   f'{info}', reply_markup=trainig_booking_confirm_keyboard())
    await call.message.delete()


async def booking_accept(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.booking_accept)
    info = ''
    await call.message.answer(text=f'Вы успешно записаны на тренировку \n'
                                   f'{info}',
                              reply_markup=booking_accept_keyboard())
    await call.message.delete()


async def booking_cancel_choose(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.booking_cancel_choose)
    await call.message.answer(text='Выберите тренировку из списка', reply_markup=booking_cancel_choose_keyboard())
    await call.message.delete()


async def booking_cancel_info(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.booking_cancel_confirm)
    info = ''
    await call.message.answer(text=f'Полная информация по тренировке \n'
                                   f'{info}', reply_markup=booking_cancel_info_keyboard())
    await call.message.delete()

async def booking_cancel_confirm(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(MainStates.booking_cancel_result)
    await call.message.answer(text='Запись успешно удалена', reply_markup=booking_accept_keyboard())
    await call.message.delete()
