#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from backend.service.event_service import get_event, get_events_by_day, get_events_by_filter
from flask import abort


def get_single_event(event_id: int):
    event = get_event(event_id)
    if event == {}:
        abort(404, "Event not found for Id: {}".format(event_id))
    else:
        return event


def get_day_events(date: str):
    try:
        real_day = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        abort(400, "Could not convert date, please use YYYY-MM-DD")
    else:
        events = get_events_by_day(real_day.date())
        if not events:
            abort(404, "No events found for that day")
        else:
            return events


def get_filtered_events(page: int, per_page: int, from_datetime: str = ""):
    if from_datetime == "":
        from_dt=datetime.now()
    else:

        try:
            from_dt=datetime.fromisoformat(from_datetime.replace("Z", "+00:00"))
        except ValueError:
            abort(400, "Incorrect from_datetime")
            return
    events = get_events_by_filter(from_dt=from_dt, page=page, count=per_page)
    if not events:
        abort(404, "No events found for selected filter")
    else:
        return events

