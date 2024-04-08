from fastapi import APIRouter, HTTPException
from typing import List
from .models import *
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer
import json

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    ew = EventFileManager
    return ew.read_events_from_file()


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    ew = EventFileManager
    data = ew.read_events_from_file()
    resultlist = []
    for item in data:
        if item["date"] == data or item["organizer"]["name"] == organizer or item["status"] == status or item["type"] == event_type:
            resultlist.append(item)
    return resultlist


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    ew = EventFileManager
    data = ew.read_events_from_file()
    for item in data:
        if item["id"] == event_id:
            return item
    raise HTTPException(status_code=422, detail="Event not found")


@router.post("/events", response_model=Event)
async def create_event(event: Event):
    ew = EventFileManager
    data = ew.read_events_from_file()
    for item in data:
        if item["id"] == event.id:
            raise HTTPException(status_code=422, detail="Event ID already exists")
    writelist = []
    writelist.append(event)
    ew.write_events_to_file(writelist)
    return event



@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    ew = EventFileManager
    data = ew.read_events_from_file()
    write_list = []
    found = False
    for item in data:
        if item["id"] == event_id:
            write_list.append(event)
            found = True
        else:
            data_as_event = Event
            data_as_event.id = item["id"]
            data_as_event.name = item["name"] 
            data_as_event.date = item["date"]
            org = Organizer
            org.name = item["organizer"]["name"]
            org.email = item["organizer"]["email"]
            data_as_event.organizer = org
            data_as_event.status = item["status"]
            data_as_event.type = item["type"]
            data_as_event.joiners = []
            for obj in item["joiners"]:
                joinee = Joiner
                joinee.name = obj["name"]
                joinee.email = obj["email"]
                joinee.country = obj["country"]
                data_as_event.joiners.append(joinee)
            data_as_event.location = item["location"]
            data_as_event.max_attendees = item["max_attendees"]
            write_list.append(data_as_event)
    if not found:
        raise HTTPException(status_code=422, detail="Event not found")
    open(EventFileManager.FILE_PATH, 'w').close()
    ew.write_events_to_file(write_list)
    return event


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    ew = EventFileManager
    data = ew.read_events_from_file()
    write_list = []
    found = False
    for item in data:
        if item["id"] == event_id:
            found = True
            continue
        else:
            data_as_event = Event
            data_as_event.id = item["id"]
            data_as_event.name = item["name"] 
            data_as_event.date = item["date"]
            org = Organizer
            org.name = item["organizer"]["name"]
            org.email = item["organizer"]["email"]
            data_as_event.organizer = org
            data_as_event.status = item["status"]
            data_as_event.type = item["type"]
            data_as_event.joiners = []
            for obj in item["joiners"]:
                joinee = Joiner
                joinee.name = obj["name"]
                joinee.email = obj["email"]
                joinee.country = obj["country"]
                data_as_event.joiners.append(joinee)
            data_as_event.location = item["location"]
            data_as_event.max_attendees = item["max_attendees"]
            write_list.append(data_as_event)
    if not found:
        raise HTTPException(status_code=422, detail="Event not found")
    open(EventFileManager.FILE_PATH, 'w').close()
    ew.write_events_to_file(write_list)


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    data = EventFileManager.read_events_from_file()
    events = []
    for item in data:
        data_as_event = Event
        data_as_event.id = item["id"]
        data_as_event.name = item["name"] 
        data_as_event.date = item["date"]
        org = Organizer
        org.name = item["organizer"]["name"]
        org.email = item["organizer"]["email"]
        data_as_event.organizer = org
        data_as_event.status = item["status"]
        data_as_event.type = item["type"]
        data_as_event.joiners = []
        for obj in item["joiners"]:
            joinee = Joiner
            joinee.name = obj["name"]
            joinee.email = obj["email"]
            joinee.country = obj["country"]
            data_as_event.joiners.append(joinee)
        data_as_event.location = item["location"]
        data_as_event.max_attendees = item["max_attendees"]
        events.append(data_as_event)
    multiple = EventAnalyzer.get_joiners_multiple_meetings_method(events)
    if len(multiple) == 0:
        return "No joiners attending at least 2 meetings"
    
