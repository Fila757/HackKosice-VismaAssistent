import json
import nltk
import sys
import os
import re

from google_calendar.list_events import list_events
from google_calendar.add_event import add_event
from voice_recog.event_to_speech import say_event
from voice_recog.text_to_speech import say

sep=';|\.|\?|!| |\n'

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
    events = list_events()

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

    print(matching_events)
    return matching_events

def read_event(event):
    say_event(event)

    said_words = "Aaaa"
    
    if 'yes' in said_words.split():
        return True
    else:
        return False

def events_to_speaker_and_google_calendar(events):
    say("I found " + str(len(events)) + "matching events")
    for event in events:
        if read_event(event):
            add_event(event)
        
    
    #TODO after knowing how piaudio or google assistent works


if __name__ == '__main__':
    print(len(find_right_events(input())))
    
            
