import voice_recog.speech_to_text as vr
import words_to_events.word_proccessing as we

def main():
    said = vr.speech_to_text()
    events = we.find_right_events(said)
    we.events_to_speaker_and_google_calendar(events)

main()
