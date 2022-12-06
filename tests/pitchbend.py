from midioutwrapper import *

if __name__ == '__main__':
    import time
    
    mout, name = open_midioutput(interactive=True)

    try:
        with mout:
            mw = MidiOutWrapper(mout, ch=3)
            time.sleep(0.1)
            mw.send_pitch_bend()
            mw.send_note_on(60)
            print("firsthello")
            time.sleep(1)
            mw.send_note_off(60)
            time.sleep(1)
            mw.send_pitch_bend()
            mw.send_note_on(60)
            time.sleep(1)
            print("hello")
            mw.send_note_off(60)
            time.sleep(0.1)
            mw.send_pitch_bend(8192-561)
            mw.send_note_on(64)
            time.sleep(1)
            print("hello")
            mw.send_note_off(64)
            time.sleep(0.1)
    except (EOFError, KeyboardInterrupt):
        print('error')

    del mout