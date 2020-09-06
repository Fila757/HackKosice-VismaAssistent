import voice_recog.text_to_speech as ts
import re, datetime

def say_event(event):
    time = ['start', 'end']
    rest = ['location', 'reminders', 'attendees']
    string = ""
    string += "SUMMARY: " + event['summary'] + "\n"
    string += "DESCRIPTION: " + event['description'] + "\n"
    
    start = str(datetime.datetime(*map(int, re.split('[^\d]', event['start']['dateTime'])[:-1])))
    end = str(datetime.datetime(*map(int, re.split('[^\d]', event['end']['dateTime'])[:-1])))
    string += "START: " + start + "\n"
    string += "END: " + end + "\n"
    
    ts.bag3.punch(string)
    ts.bag2.punch("I will tell you more about one of the events I found:")
    ts.bag2.punch("Summary of the event is '" + event['summary'] + "' the description of the event is '" + event['description'] + "'.")
    ts.bag2.punch("Do you want to add this great event to your calendar?")
