from midioutwrapper import *

if __name__ == '__main__':
    import time
    
    mout, name = open_midioutput(interactive=True)

    try:
        with mout:
            mw = MidiOutWrapper(mout)
            # why is this part not making sound..?
            time.sleep(0.1)
            mw.send_pitch_bend()
            mw.send_note_on(60)
            time.sleep(1)
            mw.send_note_off(60)
            time.sleep(1)

            # the notes begin

            mw.send_pitch_bend()
            mw.send_note_on(60)

            mw.send_pitch_bend(8192-561, ch=2)
            mw.send_note_on(64, ch=2)

            mw.send_pitch_bend(8192+80, ch=3)
            mw.send_note_on(67, ch=3)

            mw.send_pitch_bend(8192-1277, ch=4)
            mw.send_note_on(70, ch=4)

            time.sleep(5)
            
        
            mw.send_note_off(60, ch=1)
            mw.send_note_off(64, ch=2)
            mw.send_note_off(67, ch=3)
            mw.send_note_off(70, ch=4)
            time.sleep(0.1)
    except (EOFError, KeyboardInterrupt):
        print('error')

    del mout