from prometheus_client import start_http_server, Counter
from emoji import demojize
import logging
import socket
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s — %(message)s',
                    datefmt='%d.%m.%Y - %H:%M:%S')

TOKEN = os.getenv('TWITCH_TOKEN')
SERVER = 'irc.chat.twitch.tv'
NICCKNAME = os.getenv('TWITCH_NICKNAME')
CHANNEL = os.getenv('TWITCH_CHANNEL')
WS_PORT = 6667

POGS = ['PogChamp',
        'lirikPOG',
        'POGGERS',
        'PogU',
        'Pog',
        'PogYou',
        'PogT',
        'LPPM']

KEKWS = ['KEKW',
         'LULW',
         'KEKLEO',
         'KEKYou',
         'KEKL']


def main():
    # Connect to Twitch WebSocket
    sock = socket.socket()
    sock.connect((SERVER, WS_PORT))
    sock.send(f"PASS {TOKEN}\r\n".encode('utf-8'))
    sock.send(f"NICK {NICCKNAME}\r\n".encode('utf-8'))
    sock.send(f"JOIN {CHANNEL}\r\n".encode('utf-8'))

    # Start prometheus client
    ppm = Counter('ppm', 'PPM Counter')
    kpm = Counter('kpm', 'KPM Counter')
    start_http_server(8000)

    try:
        while True:
            # Receive message
            resp = sock.recv(2048).decode('utf-8')

            # Parse mmessage
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                if NICCKNAME in demojize(resp):
                    logging.info(demojize(resp))
                else:
                    message = demojize(resp).split(f'{CHANNEL} :')[1]
                    # PPM checking
                    if any(emote in message.split() for emote in POGS):
                        ppm.inc()
                    # KPM checking
                    if any(emote in message.split() for emote in KEKWS):
                        kpm.inc()
    except KeyboardInterrupt:
        sock.close()
        exit()
    except Exception as e:
        logging.error(e, exc_info=True)
        sock.close()
        exit()


if __name__ == '__main__':
    main()
