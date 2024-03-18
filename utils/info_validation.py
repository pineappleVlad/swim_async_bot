from datetime import datetime, date, time

months_ru = {
    "January": "января",
    "February": "февраля",
    "March": "марта",
    "April": "апреля",
    "May": "мая",
    "June": "июня",
    "July": "июля",
    "August": "августа",
    "September": "сентября",
    "October": "октября",
    "November": "ноября",
    "December": "декабря"
}


def valid_training_date_check(date_time_string, trainings_list_of_dict):
    date_time_list = date_time_string.split()
    date = date_time_list[0] + " " + date_time_list[1] + " " + date_time_list[2]
    time = date_time_list[3]
    text = ''
    for training in trainings_list_of_dict:
        if (training["date"] == date) and (training["time"] == time):
            text += f"Дата: {training['date']} \n"
            text += f"Время: {training['time']} \n"
            text += f"Тип бассейна: {training['pool_type']} \n"
            text += f"Тренер: {training['trainer_name']}"
    return text


def valid_training_message_text(text_message):
    text_list = text_message.split("\n")
    for text in text_list:
        if 'Дата' in text:
            date_str = text.split(': ')[1].strip()
        elif 'Время' in text:
            time_str = text.split(': ')[1].strip()

    for en_month, ru_month in months_ru.items():
        if ru_month in date_str:
            date_str = date_str.replace(ru_month, en_month)
            break
    date_obj = datetime.strptime(date_str, "%d %B %Yг.")
    date_result = date_obj.date()

    time_obj = datetime.strptime(time_str, "%H:%M")
    time_result = time_obj.time()
    return date_result, time_result
