import mido
from pythonosc import udp_client

# Configure your OSC client
osc_ip = "127.0.0.1"  # Change this to the IP address of your OSC device
osc_port = 8263  # Change this to the port your OSC device is listening on
osc_client = udp_client.SimpleUDPClient(osc_ip, osc_port)

def send_osc_message(note, value):
    if (int(format(note)) < 10):
        path = "Key10{}".format(note)
    else:
        path = "/Key1{}".format(note)
    osc_client.send_message(path, value)

def watch_midi():
    with mido.open_input() as port:
        print(port)
        print("Waiting for MIDI messages...")
        for msg in port:
            if msg.type == 'note_on':
                print("Note", msg.note, "pressed")
                send_osc_message(msg.note, True)
            elif msg.type == 'note_off':
                print("Note", msg.note, "released")
                send_osc_message(msg.note, False)

if __name__ == "__main__":
    watch_midi()
