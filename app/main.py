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

# Start prometheus client and metrics
emote_usage = Counter('emote_usage', 'Emotes usage counter', ['emote', 'fr'])
start_http_server(8000)


def test(message, emote):
    if emote in message.split():
        return emote


async def check_for_emotes(data, writer):
    try:
        if data.startswith('PING'):
            writer.write("PONG\n".encode('utf-8'))
        elif len(data) > 0:
            if NICKNAME in demojize(data):
                logging.info(demojize(data))
            elif f'{CHANNEL} :' in demojize(data):
                message = demojize(data).split(f'{CHANNEL} :')[1]
                for emote in asyncio.as_completed(map(test, message, FRS)):
                    earliest_result = await emote
                    # if emote in message.split():
                    emote_usage.labels(earliest_result, 'true').inc()
            else:
                logging.error(f"Can't process these message: {demojize(data)}")
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
            asyncio.create_task(check_for_emotes(data.decode('utf-8'), writer))

    except Exception as e:
        logging.error(e, exc_info=True)
        writer.close()


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
