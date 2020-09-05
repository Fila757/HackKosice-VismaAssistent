import voice_recog.text_to_speech as ts

def say_event(event):
    ts.bag2.punch("Summary of the event is " + event['summary'] + " the description of the event is " + event['description'])
    ts.bag2.punch("Do you want to add this great event to your calendar?")
