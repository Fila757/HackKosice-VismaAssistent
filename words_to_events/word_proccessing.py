import json
import nltk
import sys
import os
import re

from google_calendar.list_events import list_events
from google_calendar.add_event import add_event
from voice_recog.event_to_speech import say_event
import voice_recog.text_to_speech as ts
from voice_recog.speech_to_text import speech_to_text

sep=';|\.|\?|!| |\n'
affirmative_words=['yes', 'all right', 'alright', 'very well', 'of course', 'by all means', 'sure', 'certainly', 'absolutely', 'indeed', 'affirmative', 'in the affirmative', 'agreed', 'roger', 'aye', 'yeah', 'yah', 'yep', 'yup', 'uh-huh', 'okay', 'OK', 'okey-dokey', 'okey-doke', 'achcha', 'righto', 'righty-ho', 'surely', 'yea']
negative_words=['no', 'not', 'un']

def proccess_text(text):
    text = nltk.word_tokenize(text)
    proccessed_text = nltk.pos_tag(text)

    names = list()
    nouns = list()
    
    for pair in proccessed_text:
        if pair[1] == 'NNP':
            names.append(pair[0])
        elif pair[1].startswith('N'):
            nouns.append(pair[0])

    result = dict()
    result['names'] = names
    result['nouns'] = nouns
    return result

def find_right_events(text):

    words = proccess_text(text) #names #nouns
    events = list_events('primary')

    #names, maybe take emails from some databaze

    matching_events = list()
    for event in events:
        #names
        #print(re.split(sep, event['summary']))
        #print(re.split(sep, event['description']))
        for word in words['names']:
            if (word in re.split(sep, event['summary'])) or (word in re.split(sep, event['description'])):
                matching_events.append(event)
                break
            if {'name':word} in event['attendees']:
                matching_events.append(event)
                break
        #nouns
        for word in words['nouns']:
            if (word in re.split(sep, event['summary'])) or (word in re.split(sep, event['description'])):
                matching_events.append(event)
                break

    return matching_events

def read_event(event):
    say_event(event)

    said_words = speech_to_text()

    for word in negative_words:
        if word in re.split(sep, said_words):
            return False
           
    for word in affirmative_words:
        if word in said_words:
            return True

    return False

def create_same_event(event):
    tmp_event = dict()
    
    if 'summary' in event.keys(): tmp_event['summary'] = event['summary']
    if 'description' in event.keys(): tmp_event['description'] = event['despription']
    if 'start' in event.keys(): tmp_event['start'] = event['start']
    if 'end' in event.keys(): tmp_event['end'] = event['end']
    if 'location' in event.keys(): tmp_event['location'] = event['location']
    if 'reminders' in event.keys(): tmp_event['reminders'] = event['reminders']
    if 'attendees' in event.keys(): tmp_event['attendees'] = event['attendees']

    return tmp_event

def events_to_speaker_and_google_calendar(events):
    if(len(events) == 0):
        ts.bag2.punch("I am sorry, but I haven't found any matching event")
    else:
        ts.bag2.punch("I found " + str(len(events)) + "matching events")
        
    for event in events:
        if read_event(event):
            event = create_same_event(event)
            add_event(event, 'secondary')
            ts.bag2.punch("I have successfuly added the great event to your calendar.")
            break
        ts.bag2.punch("You don't want to add that great event to your calendar? What a shame!")
    



if __name__ == '__main__':
    print(len(find_right_events(input())))
