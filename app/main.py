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
NICKNAME = os.getenv('TWITCH_NICKNAME')
CHANNEL = os.getenv('TWITCH_CHANNEL')
WS_PORT = 6667

FRS = ['cogFR',
        'cozy3',
        'cuteFR',
        'dinkFR',
        'djFR',
        'evilFR',
        'ezFR',
        'fallFR',
        'feelsFR',
        'FRpls',
        'grinFR',
        'Hapje',
        'hugFR',
        'jumpFR',
        'ladderFR',
        'LPPM',
        'MEGALUL',
        'pauseFR',
        'popFR',
        'pteraFR',
        'puzzleFR',
        'ratFR',
        'runFR',
        'Saje',
        'spinFR',
        'stealthFR',
        'suitFR',
        'swimFR',
        'tripFR',
        'trollFR',
        'WAYTOOFR',
        'LFRW',
        'loveFR',
        'happyFR']

# KEKWS = ['KEKW',
#          'LULW',
#          'KEKLEO',
#          'KEKYou',
#          'KEKL']


def main():
    # Connect to Twitch WebSocket
    sock = socket.socket()
    sock.connect((SERVER, WS_PORT))
    sock.send(f"PASS {TOKEN}\r\n".encode('utf-8'))
    sock.send(f"NICK {NICKNAME}\r\n".encode('utf-8'))
    sock.send(f"JOIN {CHANNEL}\r\n".encode('utf-8'))

    # Start prometheus client and metrics
    emote_usage = Counter('emote_usage', 'Emotes usage counter', ['emote', 'fr'])
    start_http_server(8000)

    try:
        while True:
            # Receive message
            resp = sock.recv(2048).decode('utf-8')

            # Parse mmessage
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                if NICKNAME in demojize(resp):
                    logging.info(demojize(resp))
                elif f'{CHANNEL} :' in demojize(resp):
                    message = demojize(resp).split(f'{CHANNEL} :')[1]
                    # # PPM checking
                    # if any(emote in message.split() for emote in POGS):
                    #     ppm.inc()
                    # # KPM checking
                    # if any(emote in message.split() for emote in KEKWS):
                    #     kpm.inc()
                    for emote in FRS:
                        if emote in message.split():
                            emote_usage.labels(emote, 'true').inc()
                else:
                    logging.error(f"Can't process these message: {demojize(resp)}")
    except KeyboardInterrupt:
        sock.close()
        exit()
    except Exception as e:
        logging.error(e, exc_info=True)
        sock.close()
        exit()


if __name__ == '__main__':
    main()
