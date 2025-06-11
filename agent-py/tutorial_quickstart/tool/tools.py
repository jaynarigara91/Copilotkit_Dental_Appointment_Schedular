from langchain.tools import tool
from langchain_google_community.calendar.create_event import CalendarCreateEvent
from langchain_google_community.calendar.search_events import CalendarSearchEvents
from langchain_google_community.calendar.delete_event import CalendarDeleteEvent
from langchain_google_community.calendar.update_event import CalendarUpdateEvent
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)
from datetime import datetime
from typing import List, Optional
import json

credentials = get_google_credentials(
    token_file="tutorial_quickstart/credentials/token.json",
    scopes=["https://www.googleapis.com/auth/calendar"],
    client_secrets_file="tutorial_quickstart/credentials/credentials.json",
)
api_resource = build_resource_service(credentials=credentials)

def format_date_with_ordinal(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    day = date_obj.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    return date_obj.strftime(f"%B {day}{suffix} %Y")

def format_time_to_ampm(time_str):
    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    hour = time_obj.hour
    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12  # Convert 0 to 12
    return f"{display_hour} {period}"

@tool
def CREATE_CALENDAR_EVENT(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    description: str,
    timezone: str = "Asia/Kolkata",
    location: Optional[str] = None,
    reminders: Optional[List[dict]] = None,
    conference_data: bool = False,
    color_id: Optional[str] = None,
):
    """Create a calendar event with specified details. use this date formate '%Y-%m-%d %H:%M:%S' """
    event = CalendarCreateEvent(api_resource=api_resource)
    response = event.invoke({
        "summary": summary,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "timezone": timezone,
        "location": location,
        "description": description,
        "reminders": reminders,
        "conference_data": conference_data,
        "color_id": color_id,
    })
    
    other = {
        "Event":response,
        "summary": summary,
        "date": format_date_with_ordinal(start_datetime),
        "time": format_time_to_ampm(start_datetime),
        "timezone": timezone,
        "description": description}
    
    return other

# @tool
# def CREATE_CALENDAR_EVENT(
#     summary: str,
#     start_datetime: str,
#     end_datetime: str,
#     timezone: str = "Asia/Kolkata",
#     location: Optional[str] = None,
#     description: Optional[str] = None,
#     reminders: Optional[List[dict]] = None,                               #Dummy create_event tool
#     conference_data: bool = False,
#     color_id: Optional[str] = None,
# ):
#     """Create a calendar event with specified details. use this date formate '%Y-%m-%d %H:%M:%S' """
 
#     return {
#         "summary": "dental appointment",
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "link": "https://calendar.google.com"
#     }


@tool
def SEARCH_CALENDAR_EVENT(
    query: str,
    min_datetime: str,
    max_datetime: str,
    timezone: str = "Asia/Kolkata"
):
    """Search for calendar events by query and datetime range.this is the date formate '%Y-%m-%d %H:%M:%S' """
    event = CalendarSearchEvents(api_resource=api_resource)
    return event.invoke({
        "query": query,
        "min_datetime": min_datetime,
        "max_datetime": max_datetime,
        "timezone": timezone,
        "calendars_info": json.dumps([
            {"id": "primary", "summary": "Primary Calendar"}
        ])
    })


@tool
def DELETE_CALENDAR_EVENT(
    query: str,
    min_datetime: str,
    max_datetime: str,
    timezone: str = "Asia/Kolkata"):
    
    """Search for calendar events by query and datetime range for delete event.this is the date formate '%Y-%m-%d %H:%M:%S' """
    event = CalendarSearchEvents(api_resource=api_resource)
    response = event.invoke({
        "query": query,
        "min_datetime": min_datetime,
        "max_datetime": max_datetime,
        "timezone": timezone,
        "calendars_info": json.dumps([
            {"id": "primary", "summary": "Primary Calendar"}
        ])
    })
    
    for i in response:
        event_id = i.get("id")
        
        delete = CalendarDeleteEvent(api_resource=api_resource)
        result = delete.invoke({
            "event_id": event_id,
            "calendar_id": "primary"
        })
        return {"status": "deleted", "event_id": event_id, "result": result}


@tool
def UPDATE_CALENDAR_EVENT(
    query: str,
    min_datetime: str,
    max_datetime: str,
    timezone: str = "Asia/Kolkata",
    updated_start_datetime: Optional[str] = "2025-05-22 16:00:00",
    updated_end_datetime: Optional[str] = "2025-05-22 17:00:00",
):
    """Search for calendar events by query and datetime range.this is the date formate '%Y-%m-%d %H:%M:%S' """
    event = CalendarSearchEvents(api_resource=api_resource)
    response = event.invoke({
        "query": query,
        "min_datetime": min_datetime,
        "max_datetime": max_datetime,
        "timezone": timezone,
        "calendars_info": json.dumps([
            {"id": "primary", "summary": "Primary Calendar"}
        ])
    })
    
    for i in response:
        event_id = i.get("id")
    
        event = CalendarUpdateEvent(api_resource=api_resource)
        return event.invoke({
            "event_id": event_id,
            "calendar_id": "primary",
            "start_datetime": updated_start_datetime,
            "end_datetime": updated_end_datetime,
            })
        
        
  