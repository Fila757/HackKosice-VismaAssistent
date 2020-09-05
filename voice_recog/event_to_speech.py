from voice_recog.text_to_speech import say

def say_event(event):
    print("printuju eventiky", event)
    say("Summary of the event is " + event['summary'] + " the description of the event is " + event['description'])
    say("Do you want to add this great event to your calender?")
