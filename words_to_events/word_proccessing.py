import json
import nltk
import sys
import os

sys.path.append('../google_calendar')
from list_events import list_events

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
        for word in words[0]:
            if word in event['summary'] or word in event['description']:
                matching_events.append(event)
                break
            if word in event['attendees']:
                matching_events.append(event)
                break
        #nouns
        for word in words[1]:
            if word in event['summary'] or word in event['description']:
                matching_events.append(event)
                break

    return matching_events
                
    
def events_to_speaker(events):
    pass
    #TODO after knowing how piaudio or google assistent works


if __name__ == '__main__':
    print(find_right_events(input()))
    
            
