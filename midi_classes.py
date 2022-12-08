class Note:
    def __init__(self, note_value, pb_amt = 0):
        self.note_value = note_value
        self.pb_amt = pb_amt
        # Channel ID for a note becomes -1 if it is inactive.
        self.channel_id = -1

    def get_pb(self):
        return self.pb_amt

    def get_note_value(self):
        return self.note_value

    def get_channel_id(self):
        return self.channel_id

    def set_channel_id(self, channel_id):
        self.channel_id = channel_id
        return self.channel_id


class Channels:
    def __init__(self, mw):
        self.mw = mw
        self.available_channels = 16
        # Active channels are 1, inactive are 0
        # If necessary, can store Note objects here (change from 0 to None
        self.channels = [0 for x in range(16)]

    def note_on(self, Note):
        # Don't do anything if there are no free channels
        if self.available_channels == 0:
            return False

        # Find next available channel, 
        # then set the ID value in the Note object
        ch_no = 0
        for i, channel in enumerate(self.channels):
            if channel == None:
                self.available_channels -= 1
                ch_no = i
                channel = 1
                Note.set_channel_id(i)
                break

        # Set the pitch bend value of the available channel
        self.mw.send_pitch_bend(8192 + Note.get_pb(), ch=ch_no)
        # Send the note value
        self.mw.send_note_on(Note.get_note_value())

        return True


    def note_off(self, Note):
        # Send the note off value
        self.mw.send_note_off(Note.get_note_value(), Note.get_channel_id())
        # Deactivate that channel in this Channel object
        self.channels[Note.get_channel_id()] = 0
        self.available_channels += 1
        # Channel ID becomes -1 now inactive.
        Note.set_channel_id(-1)

        return True