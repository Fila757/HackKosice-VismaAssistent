import json
import nltk
import sys
import os
import re
import traceback

from google_calendar.list_events import list_events
from google_calendar.add_event import add_event
from voice_recog.event_to_speech import say_event
import voice_recog.text_to_speech as ts
from voice_recog.speech_to_text import speech_to_text

import pyjokes
from playsound import playsound

sep=';|\.|\?|!| |\n'
affirmative_words=['yes', 'all right', 'alright', 'very well', 'of course', 'by all means', 'sure', 'certainly', 'absolutely', 'indeed', 'affirmative', 'in the affirmative', 'agreed', 'roger', 'aye', 'yeah', 'yah', 'yep', 'yup', 'uh-huh', 'ok', 'okay', 'OK', 'okey-dokey', 'okey-doke', 'achcha', 'righto', 'righty-ho', 'surely', 'yea']
negative_words=['no', 'not', 'un']
continuations=["continue","more","next"]
searchs=["find", "search"]

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

def get_yesno():
    said_words = speech_to_text()

    for word in negative_words:
        if word in re.split(sep, said_words):
            return False

    for word in affirmative_words:
        if word in said_words:
            return True

    return False

def read_event(event):
    say_event(event)

    return get_yesno()

def create_same_event(event):
    tmp_event = dict()
    
    if 'summary' in event.keys(): tmp_event['summary'] = event['summary']
    if 'description' in event.keys(): tmp_event['description'] = event['description']
    if 'start' in event.keys(): tmp_event['start'] = event['start']
    if 'end' in event.keys(): tmp_event['end'] = event['end']
    if 'location' in event.keys(): tmp_event['location'] = event['location']
    if 'reminders' in event.keys(): tmp_event['reminders'] = event['reminders']
    if 'attendees' in event.keys(): tmp_event['attendees'] = event['attendees']

    return tmp_event

def events_to_speaker_and_google_calendar(event):
    if read_event(event):
        event = create_same_event(event)
        add_event(event, 'secondary')
        ts.bag2.punch("I have successfuly added the great event to your calendar.")
    else:
        ts.bag2.punch("You don't want to add that great event to your calendar? What a shame!")
    
queue = []
queueType = 0
questions = []
questionIndex = 0

def read_question(question, answer = None):
    
    if answer == None: ts.bag3.punch("QUESTION: "+question)
    else: ts.bag3.punch("QUESTION: "+question+"\n ANSWER: "+answer)
    
    ts.bag2.punch(question)
    if answer == None:
        ts.bag2.punch("This question does not have any answer yet, would you like to add one?")
        yesno = get_yesno()
        if yesno:
            ts.bag2.punch("Alright, say the new answer now.")
            said_answer = speech_to_text()
            return (question,said_answer)
        else:
            ts.bag2.punch("Alright, I won't add any.")
    else:
        ts.bag2.punch("This question has answer "+str(answer)+" Do you want to change it?")
        yesno = get_yesno()
        if yesno:
            ts.bag2.punch("Alright, say the new answer now.")
            said_answer = speech_to_text()
            return (question, said_answer)
        else:
            ts.bag2.punch("Alright, I won't edit it.")
    return (question,answer)

    

def react_to_said(said):
    global queue, queueType, questions, questionIndex
    
    if "add question" == said[:12]:
        print("Question "+said[13:]+" added")
        questions.append((said[13:],None))
        ts.bag2.punch("Question "+said[13:]+" added")
        return
       
    if "read question" == said[:13]:
        try:
            queueType=2
            questionIndex = int(said.split()[2])-1
            if questionIndex >= len(questions):
                ts.bag2.punch("There is no question with such number.")
            else:
                ts.bag2.punch("Reading question number "+str(questionIndex+1))
                questions[questionIndex] = read_question(questions[questionIndex][0],questions[questionIndex][1])
        except ValueError:
            ts.bag2.punch("Could not deduce the question number.")
        return


    for search in searchs:
        if search in said:
            print("searchnig")
            queue = find_right_events(said)
            queue = queue[::-1]
            queueType = 1
            ts.bag2.punch("I found " + str(len(queue)) + " matching events.")
            return

    for continuation in continuations:
        if continuation in said:
            if queueType == 1:
                if len(queue) == 0:
                    ts.bag2.punch("I am sorry, but I don't have any reamining matching events.")
                else:
                    current_event = queue.pop()
                    events_to_speaker_and_google_calendar(current_event)
            elif queueType == 2:
                if len(questions) == 0:
                    ts.bag2.punch("I am sorry, but there seem to be no questions.")
                else:
                    questionIndex += 1
                    if questionIndex >= len(questions):
                        questionIndex = 0
                    ts.bag2.punch("Reading question number "+str(questionIndex+1))
                questions[questionIndex] = read_question(questions[questionIndex][0],questions[questionIndex][1])
            return



    if "play" in said and "song" in said:
        print("playing")
        playsound("wake.mp3")
        return
    if "joke" in said:
        print("joking")
        print(pyjokes.get_joke())
        ts.bag2.punch(pyjokes.get_joke())
        return

if __name__ == '__main__':
    print(len(find_right_events(input())))
