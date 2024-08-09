from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from datetime import datetime
from .models import Chat, Table
from django.contrib.auth.models import User

@tool
def history() -> list:
    """
    history of conversation between user and ai

    Returns:
        list: each item in the list represent the user input and the presponse of ai on that user input
    """
    chats = list(Chat.objects.values('datetime', 'user_text', 'ai_text').order_by("datetime"))
    return chats

history.name = "history"
history.description = "All the conversation details between user and ai"

@tool
def today_schedules() -> list:
    """
    Today's schedules' details
    
    Returns:
        list: each item of the list is a schedule set by ai on request of user
    """
    schedules = list(Table.objects.filter(date=datetime.now().date()).values('id','date','start_time','end_time','user_name','topic').order_by("date", "start_time"))
    return schedules

today_schedules.name = "today_schedules"
today_schedules.description = "schedule details of today"

@tool
def all_schedules() -> list:
    """
    All schedules' details
    
    Returns:
        list: each item of the list is a schedule set by ai on request of user
    """
    schedules = list(Table.objects.values('id','date','start_time','end_time','user_name','topic').order_by("date", "start_time"))
    return schedules

all_schedules.name = "all_schedules"
all_schedules.description = "schedule details on schedule table"

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

    try:
        if date_str: date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else: date = item.date
        if start_time_str: start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        else: start_time = item.start_time
        if end_time_str: end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        else: end_time = item.end_time
        if not user_name: user_name = item.user_name
        if not topic: topic = item.topic
    except Exception as e:
        return e

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

TOOLS = [history, today_schedules, all_schedules, add_schedule, update_schedule, delete_schedule]
TOOLS_DETAILS = """**Tools at Your Disposal:**
1. **today_schedules:** Provides details of all meetings scheduled for today.
2. **all_schedules:** Lists all scheduled meetings.
3. **add_schedule:** Use this tool to add a new meeting. Ensure all required information is confirmed before adding a schedule. No fields should be left blank.
4. **update_schedule:** Update an existing meeting by referencing its ID using the 'all_schedules' tool. If some fields do not need changes, retain their previous values.
5. **delete_schedule:** Delete an existing meeting by referencing its ID using the 'all_schedules' tool. Confirm with the user before deleting, as only one schedule can be deleted at a time. Ensure the ID exists before proceeding.

**Formatting Requirements:**
- **Date Format:** Dates should be in the format '%Y-%m-%d' (e.g., '2024-08-07').
- **Time Format:** Times should follow the format '%H:%M:%S' (e.g., '14:30:00').
"""