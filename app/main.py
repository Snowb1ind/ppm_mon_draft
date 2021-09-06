from prometheus_client import start_http_server, Counter
from emoji import demojize
import logging
import asyncio
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s — %(message)s',
                    datefmt='%d.%m.%Y - %H:%M:%S')

TOKEN = os.getenv('TWITCH_TOKEN')
SERVER = 'irc.chat.twitch.tv'
NICKNAME = os.getenv('TWITCH_NICKNAME')
CHANNEL = os.getenv('TWITCH_CHANNEL')
WS_PORT = 6667

FRS = [{"emote": "cogFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "cuteFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "chokeFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "dinkFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "djFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "evilFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "ezFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "fallFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "feelsFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "FRpls", "fr": "true", "fr_replacement": "None"},
       {"emote": "grinFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "Hapje", "fr": "true", "fr_replacement": "None"},
       {"emote": "happyFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "hugFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "jumpFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "ladderFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "loveFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "LFRW", "fr": "true", "fr_replacement": "None"},
       {"emote": "LPPM", "fr": "true", "fr_replacement": "None"},
       {"emote": "MEGALUL", "fr": "true", "fr_replacement": "None"},
       {"emote": "pauseFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "popFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "pteraFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "puzzleFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "ratFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "runFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "Saje", "fr": "true", "fr_replacement": "None"},
       {"emote": "spinFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "stealthFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "suitFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "swimFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "tripFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "trollFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "WAYTOOFR", "fr": "true", "fr_replacement": "None"},
       {"emote": "wiggleFR", "fr": "true", "fr_replacement": "None"}]

OGS = []

# Start prometheus client and metrics
emote_usage = Counter('emote_usage',
                      'Emotes usage counter',
                      ['emote', 'fr', 'fr_replacement'])
start_http_server(8000)


async def check_for_emotes(data, writer):
    """Check for emotes in message text"""
    try:
        if data.startswith('PING'):
            writer.write("PONG\n".encode('utf-8'))
        elif len(data) > 0:
            if NICKNAME in data:
                logging.info(data)
            elif f'{CHANNEL} :' in data:
                message = data.split(f'{CHANNEL} :')[1]
                for emote in FRS:
                    if emote["emote"] in message.split():
                        emote_usage.labels(emote["emote"],
                                           emote["fr"],
                                           emote["fr_replacement"]).inc()
            else:
                logging.error(f"Can't process this message: {data}")
    except Exception as e:
        logging.error(e, exc_info=True)


async def main():
    try:
        # Connect to Twitch
        reader, writer = await asyncio.open_connection(SERVER, WS_PORT)

        # Login to Twitch chat
        lines = [f'PASS {TOKEN}\r\n'.encode('utf-8'),
                 f'NICK {NICKNAME}\r\n'.encode('utf-8'),
                 f'JOIN {CHANNEL}\r\n'.encode('utf-8')]
        writer.writelines(lines)
        await writer.drain()

        while True:
            data = await reader.readuntil('\r\n'.encode('utf-8'))
            asyncio.create_task(check_for_emotes(demojize(data.decode('utf-8')), writer))

    except Exception as e:
        logging.error(e, exc_info=True)
        writer.close()


if __name__ == '__main__':
    asyncio.run(main())
