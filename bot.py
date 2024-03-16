import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from handlers.callback import view_stats, view_balance, back_button_callback, training_booking, booking_info_confirm, booking_accept, booking_cancel_choose, booking_cancel_info, booking_cancel_confirm, current_child_save
from handlers.basic import start, main_menu_handler, cancel
from utils.states import MainStates
from config import TOKEN




async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.message.register(start, Command('start'))
    dp.message.register(cancel, Command('cancel'))
    dp.message.register(main_menu_handler, MainStates.menu_close)

    dp.callback_query.register(current_child_save, MainStates.child_choose)
    dp.callback_query.register(view_stats, F.data.startswith('training_info'), MainStates.menu_open)
    dp.callback_query.register(view_balance, F.data.startswith('balance'), MainStates.menu_open)
    dp.callback_query.register(training_booking, F.data.startswith('training_register'), MainStates.menu_open)
    dp.callback_query.register(booking_cancel_choose, F.data.startswith('booking_delete'), MainStates.menu_open)
    dp.callback_query.register(back_button_callback, F.data.startswith('back'))

    dp.callback_query.register(booking_info_confirm, F.data.startswith('training_add_1'), MainStates.choose_training_date)
    dp.callback_query.register(booking_accept, F.data.startswith('confirm_training'), MainStates.confirm_booking)

    dp.callback_query.register(booking_cancel_info, F.data.startswith('training_del_1'), MainStates.booking_cancel_choose)
    dp.callback_query.register(booking_cancel_confirm, F.data.startswith('booking_cancel'), MainStates.booking_cancel_confirm)




    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())