import asyncio
import datetime
from database.db_connection import execute_query
from utils.info_validation import months_ru

async def fio_check(name):
    query = "SELECT name FROM backend_child WHERE name = $1"
    result = await execute_query(query, (name,))
    return bool(result)

async def parent_id_update(chat_id, name): #перезапись айдишника чата
    query = """
    UPDATE backend_child
    SET parent_chat_id = $1
    WHERE name = $2 AND (parent_chat_id IS NULL OR parent_chat_id <> $1);
    """
    result = await execute_query(query, [chat_id, name])
    return bool(result)

async def parent_exists(chat_id):
    query = "SELECT parent_chat_id FROM backend_child WHERE parent_chat_id = $1"
    result = await execute_query(query, (chat_id,))
    return bool(result)

async def child_name_id_write(current_id, child_name): #перезапись имени ребенка к айдишнику чата в отдельной таблице
    query = """
    INSERT INTO backend_childid (parent_chat_id, name)
    VALUES ($1, $2)
    ON CONFLICT (parent_chat_id) DO UPDATE
    SET parent_chat_id = EXCLUDED.parent_chat_id,
        name = EXCLUDED.name;
    """
    result = await execute_query(query, [current_id, child_name])
    return bool(result)

async def get_child_balance(child_name):
    query = "SELECT paid_training_count FROM backend_child WHERE name = $1"
    result = await execute_query(query, (child_name,))
    return result

async def get_child_trainings(child_name):
    query = """
    SELECT t.date, t.time, tr.name AS trainer_name,
    CASE
        WHEN t.pool_type = '1' THEN 'Большой бассейн'
        WHEN t.pool_type = '2' THEN 'Малый бассейн'
    END AS pool_type
    FROM backend_training_children AS tc
    INNER JOIN backend_training AS t ON tc.training_id = t.id
    INNER JOIN backend_child AS c ON tc.child_id = c.id
    INNER JOIN backend_trainers AS tr ON t.trainer_id = tr.id
    WHERE c.name = $1
    """
    result = await execute_query(query, (child_name,))
    formatted_result = []
    for record in result[:9]:
        not_form_date = record['date'].strftime('%Y-%m-%d')
        date_object = datetime.datetime.strptime(not_form_date, "%Y-%m-%d")
        month_rus = months_ru[date_object.strftime("%B")]
        formatted_date = date_object.strftime(f"%d {month_rus} %Yг.")
        formatted_record = {
            'date': formatted_date,
            'time': record['time'].strftime("%H:%M"),
            'pool_type': record['pool_type'],
            'trainer_name': record['trainer_name'],
        }
        formatted_result.append(formatted_record)
    return formatted_result

async def get_child_name(chat_id, table_name):
    query = f"SELECT name FROM {table_name} WHERE parent_chat_id = $1"
    result = await execute_query(query, (chat_id,))
    names = [record['name'] for record in result]
    if len(names) == 1:
        names = names[0]
    return names

async def get_trainings_list(child_name):
    query = """
    SELECT t.date, t.time, tr.name AS trainer_name,
    CASE
        WHEN t.pool_type = '1' THEN 'Большой бассейн'
        WHEN t.pool_type = '2' THEN 'Малый бассейн'
    END AS pool_type
    FROM backend_training AS t
    INNER JOIN backend_trainers AS tr ON t.trainer_id = tr.id
    WHERE t.training_status = '1'
    AND NOT EXISTS (
        SELECT 1
        FROM backend_training_children AS tc
        INNER JOIN backend_child AS c ON tc.child_id = c.id
        WHERE tc.training_id = t.id AND c.name = $1
    )
    """
    training_list = await execute_query(query, (child_name,))
    formatted_result = []
    for record in training_list[:20]:
        not_form_date = record['date'].strftime('%Y-%m-%d')
        date_object = datetime.datetime.strptime(not_form_date, "%Y-%m-%d")
        month_rus = months_ru[date_object.strftime("%B")]
        formatted_date = date_object.strftime(f"%d {month_rus} %Yг.")
        formatted_record = {
            'date': formatted_date,
            'time': record['time'].strftime("%H:%M"),
            'pool_type': record['pool_type'],
            'trainer_name': record['trainer_name'],
        }
        formatted_result.append(formatted_record)
    return formatted_result




async def view_all():
    query = "SELECT * FROM backend_child"
    result = await execute_query(query)
    for row in result:
        print(row)


async def table_clear():
    query = """
    DELETE FROM backend_childid;
    """
    result = await execute_query(query)

# asyncio.run(table_clear())
# asyncio.run(view_all())

