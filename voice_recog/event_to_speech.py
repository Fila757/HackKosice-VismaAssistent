import voice_recog.text_to_speech as ts

def say_event(event):
<<<<<<< HEAD
    ts.bag2.punch("Summary of the event is " + event['summary'] + " the description of the event is " + event['description'])
    ts.bag2.punch("Do you want to add this great event to your calendar?")
=======
    #print("printuju eventiky", event)
    say("Summary of the event is " + event['summary'] + " the description of the event is " + event['description'])
    say("Do you want to add this great event to your calendar?")
>>>>>>> e7dc311b142a043604f7432c4afdba11c7e3bd10
