import mido
from pythonosc import udp_client

# Configure your OSC client
osc_ip = "192.168.0.201"  # Change this to the IP address of your OSC device
osc_port = 8649  # Change this to the port your OSC device is listening on
osc_client = udp_client.SimpleUDPClient(osc_ip, osc_port)

def send_osc_message(note, value):
    if int(note) < 10:
        path = "/Key10{}".format(note)
    else:
        path = "/Key1{}".format(note)
    print(path)
    osc_client.send_message(path, value)

def select_midi_input():
    print("Available MIDI input devices:")
    devices = mido.get_input_names()
    for i, device in enumerate(devices):
        print(f"{i + 1}. {device}")
    while True:
        choice = input("Enter the number of the MIDI input device you want to use: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(devices):
                return mido.open_input(devices[choice - 1])
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def watch_midi():
    port = select_midi_input()
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

