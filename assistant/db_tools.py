from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from datetime import datetime
from .models import Chat, Table

@tool
def history() -> list:
    """
    history of conversation between user and ai

    Returns:
        list: each item in the list represent the user input and the presponse of ai on that user input
    """
    chats = list(Chat.objects.values('datetime', 'user', 'ai').order_by("datetime"))
    return chats

history.name = "history"
history.description = "All the conversation details between user and ai"

@tool
def schedule_table() -> list:
    """
    schedule details on the schedule table
    
    Returns:
        list: each item of the list is a schedule set by ai on request of user
    """
    schedules = list(Table.objects.values('id','date','start_time','end_time','user_name','topic').order_by("date", "start_time"))
    return schedules

schedule_table.name = "schedule_table"
schedule_table.description = "schedule details on schedule table"

@tool
def add_schedule(date_str: str, start_time_str: str, end_time_str: str, user_name: str, topic: str):
    """
    add new schedule to schedule table
    
    Args:
        date_str (str): date input in str form maintaining '%Y-%m-%d' format (e.g. '2024-08-07')
        start_time_str (str): start time input in str form maintaining '%H:%M:%S' format (e.g. '14:30:00')
        end_time_str (str): end time input in str form maintaining '%H:%M:%S' format (e.g. '15:00:00')
        user_name (str): user name input
        topic (str): topic of schedule input
    """
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        schedule_item = Table(date=date, start_time=start_time, end_time=end_time, user_name=user_name, topic=topic)
        schedule_item.save()
        return "schedule added successfully"
    except Exception as e:
        return e

class add_schedule_inputs(BaseModel):
    date_str: str = Field("date of the scedule")
    start_time_str: str = Field("start time of the scedule")
    end_time_str: str = Field("end time of the scedule")
    user_name: str = Field("name of the person who want to set the scedule")
    topic: str = Field("topic or reason for the setting the scedule")

add_schedule.name = "add_schedule"
add_schedule.description = "Tool to add new schedule to the schedule table"
add_schedule.args_schema = add_schedule_inputs

@tool
def update_schedule(id: int, date_str: str=None, start_time_str: str=None, end_time_str: str=None, user_name: str=None, topic: str=None):
    """
    updating existing schedule on schedule table
    
    Args:
        id (int): id input
        date_str (str): date input in str form maintaining '%Y-%m-%d' format (e.g. '2024-08-07')
        start_time_str (str): start time input in str form maintaining '%H:%M:%S' format (e.g. '14:30:00')
        end_time_str (str): end time input in str form maintaining '%H:%M:%S' format (e.g. '15:00:00')
        user_name (str): user name input
        topic (str): topic of schedule input
    """
    try:
        id = int(id)
        item = Table.objects.get(id=id)
    except Exception as e:
        return e
    if date_str: date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else: date = item.date
    if start_time_str: start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
    else: start_time = item.start_time
    if end_time_str: end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
    else: end_time = item.end_time
    if not user_name: user_name = item.user_name
    if not topic: topic = item.topic

    try:
        item.date = date
        item.start_time = start_time
        item.end_time = end_time
        item.user_name = user_name
        item.topic = topic
        item.save()
        return "schedule updated successfully"
    except Exception as e:
        return e

class update_schedule_inputs(BaseModel):
    id: int = Field("id of the schedule which you want to update")
    date_str: str = Field("update date of the scedule")
    start_time_str: str = Field("update start time of the scedule")
    end_time_str: str = Field("update end time of the scedule")
    user_name: str = Field("update name of the person who want to set the scedule")
    topic: str = Field("update topic or reason for the setting the scedule")

update_schedule.name = "update_schedule"
update_schedule.description = "Tool to update existing schedule on the schedule table"
update_schedule.args_schema = update_schedule_inputs

@tool
def delete_schedule(id: int):
    """
    deleting existing schedule on schedule table
    
    Args:
        id (int): id input
    """
    try:
        id = int(id)
        item = Table.objects.get(id=id)
        item.delete()
        print("schedule deleted successfully")
    except Exception as e:
        print(e)

class delete_schedule_inputs(BaseModel):
    id: int = Field("id of the schedule which you want to delete")

delete_schedule.name = "delete_schedule"
delete_schedule.description = "Tool to delete existing schedule on the schedule table"
delete_schedule.args_schema = delete_schedule_inputs

TOOLS = [history, schedule_table, add_schedule, update_schedule, delete_schedule]
TOOLS_DETAILS = """
You have multiple tools to see exixting schedules, add new schedules, update schedules and delete schedules. Date should be always follow this format '%Y-%m-%d' (e.g. '2024-08-07'). Time should be always follow this format '%H:%M:%S' (e.g. '14:30:00')
Below are some instructions to use those tools.

schedule_table:
to check schedules on the schedule table, use this tool, and make sure you don't mixup the ids of each schedules. Each have an unique one and it's auto added to the table. Use this id to make other operations on existing schedules.

add_schedule:
Don't let any field blank. Before calling this tool, confirm all the requirment info to add the scedule.

update_schedule:
To use this tool you need all the fields on the table, if all the fields aren't need to change then use the previous value of those fields.

delete_schedule:
id must be an integer, and check the id is exist on the sceduler table or not. You can't delete multiple items at once, you have to delete each item at a time. Confirm specificly before deleting any schedule from the user.
"""