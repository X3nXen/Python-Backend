import json

class EventFileManager():

    FILE_PATH = "./event.json" 

    def read_events_from_file():
        try:
            resultlist = json.load(open(EventFileManager.FILE_PATH))
            return resultlist
        except Exception:
            return []

    def write_events_to_file(events):
        try:
            filecontent = json.load(open(EventFileManager.FILE_PATH))
        except:
            filecontent = []
        for item in events:
            event = {}
            event["id"] = item.id
            event["name"] = item.name
            event["date"] = item.date
            event["organizer"] = {}
            event["organizer"]["name"] = item.organizer.name
            event["organizer"]["email"] = item.organizer.email
            event["status"] = item.status
            event["type"] = item.type
            event["joiners"] = []
            for joiner in item.joiners:
                joinee = {}
                joinee["name"] = joiner.name
                joinee["email"] = joiner.email
                joinee["country"] = joiner.country
                event["joiners"].append(joinee)
            event["location"] = item.location
            event["max_attendees"] = item.max_attendees
            filecontent.append(event)
        with open(EventFileManager.FILE_PATH, 'w') as f:
            f.seek(0)
            json.dump(filecontent, f, indent = 4)
