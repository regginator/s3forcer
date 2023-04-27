# s3forcer | https://github.com/regginator/s3forcer
# MIT License - Copyright (c) 2023 Reggie <reggie@latte.to>

# enjoy the shit code.. I wrote this in like a day with little to no knowledge
# about the libraries i'm using here lol. feel free to submit PRs with some
# micro optimizations:tm:

import os
import asyncio
import aiohttp
import json
from sys import exit as sys_exit
from time import monotonic as time_monotonic
from itertools import product as itertools_product
from argparse import ArgumentParser

# parse flags
parser = ArgumentParser(description="s3 funny hacking")
parser.add_argument("--min-length", type=int, default=1, help="Minimum character length of channel name combonations to bruteforce")
parser.add_argument("--chars", type=str, default="abcdefghijklmnopqrstuvwxyz1", help="Characters (in a single string) to use for channel name combonations")
parser.add_argument("--prefix", type=str, default="z", help="Prefix for channel names (e.g. \"zfeature\")")
parser.add_argument("--attempt-milestone", default=5000, type=int, help="Number of attempts between cache writes and milestone prints")
parser.add_argument("--workers", type=int, default=250, help="Number of max thread workers to use")
parser.add_argument("--webhook-url", type=str, default=None, help="Discord webhook URL for found channel notifications")
parser.add_argument("--reset-cache", action="store_true", help="Reset bin/cache_list.json")
args = parser.parse_args()

# read parsed flag args into dedicated variables
min_length = args.min_length
chars = args.chars
prefix = args.prefix
attempt_milestone = args.attempt_milestone
workers = args.workers
webhook_url = args.webhook_url
reset_cache = args.reset_cache

# -------------------------------------------------------- #

def write_file(path, contents):
    with open(path, "w") as file:
        file.write(contents)
        file.close()

def read_file(path):
    with open(path, "r") as file:
        contents = file.read()
        file.close()
        return contents

# create bin for stored db
if not os.path.isdir("bin"):
    os.mkdir("bin")

# we'll check the --reset-cache flag before cont., which exits the prgm as-is
if reset_cache:
    write_file("bin/cache_list.json", "[]")
    print("Reset bin/cache_list.json")
    sys_exit()

if not os.path.isfile("bin/channels.json"):
    write_file("bin/channels.json", "[]")
if not os.path.isfile("bin/cache_list.json"):
    write_file("bin/cache_list.json", "[]")

existing_cache_list = None
def get_cache(): # returns cache_list, cache_positions
    try:
        cache_list = json.loads(read_file("bin/cache_list.json"))
        existing_cache_list = cache_list
    except:
        cache_list = existing_cache_list

    # get position cache for current cfg, if it exists
    cache_table = None
    for cache in cache_list:
        if cache["chars"] == chars and cache["prefix"] == prefix:
            cache_table = cache
    if cache_table is None:
        cache_table = {
            "chars": chars,
            "prefix": prefix,
            "positions": {}
        }

        cache_list.append(cache_table)

    cache_positions = cache_table["positions"]

    return cache_list, cache_positions

async def send_channel_req(session, combonation):
    try:
        channel_name = prefix + combonation
        url = f"https://setup.rbxcdn.com/channel/{channel_name}/DeployHistory.txt"
        async with session.head(url, timeout=15) as response:
            if response.status == 200:
                print(f"[+] Found Channel: {channel_name}")
                channels = json.loads(read_file("bin/channels.json"))

                if not channel_name in channels:
                    channels.append(channel_name)
                    try:
                        write_file("bin/channels.json", json.dumps(channels, indent=4))
                    except:
                        pass

                    # optional*
                    if webhook_url:
                        discord_response = await session.post(webhook_url, json={
                            "embeds": [
                                {
                                    "title": f"Channel Found: **{channel_name}**",
                                    "description": f"DeployHistory: <{url}>",
                                    "color": 0x3498db,
                                    "footer": {
                                        "text": "s3forcer vee2 | reggie#1000 <3"
                                    }
                                }
                            ]
                        })

                        if discord_response.status != 204:
                            error_msg = await discord_response.content.read()
                            print(f"Discord Webhook error ({discord_response.status}): {error_msg}")
    except asyncio.TimeoutError:
        pass # ignore timeouts
    except aiohttp.client_exceptions.ClientConnectionError:
        pass
    except aiohttp.client_exceptions.ServerDisconnectedError:
        pass
    except Exception as err:
        # :middle_finger:
        print(f"[!] Unhandled error exception on aiohttp (send_channel_req): {err}")

async def main():
    # no tcp connection limit
    connector = aiohttp.TCPConnector(limit=None)
    async with aiohttp.ClientSession(connector=connector) as session:
        # we need to limit task queing at a time
        semaphore = asyncio.Semaphore(workers)

        char_len = len(chars)

        # go thru each length combination progressively
        length = min_length
        while True:
            print(f"---- STARTING ATTEMPTS @ {length} CHARS (MAX ATTS: {pow(char_len, length)}) ----")
            start_time = time_monotonic()

            # we WON'T list everything into an iter directly, we'll go through it properly..
            channel_names = map("".join, itertools_product(chars, repeat=length))

            # we'll manage ongoing tasks ourselves
            current_attempt = 1

            cache_list, cache_positions = get_cache()

            length_str = str(length)
            if length_str in cache_positions:
                cache_position = cache_positions[length_str]
                print(f"^^ STARTING AT CACHED POSITION OF {cache_position}.. ^^")
                for _ in channel_names:
                    if current_attempt > cache_position:
                        break
                    current_attempt += 1

            for channel_name in channel_names:
                if current_attempt % attempt_milestone == 0:
                    print(f"Milestone of {current_attempt} attempts reached..")
                    
                    cache_list, cache_positions = get_cache()
                    cache_positions[length_str] = current_attempt
                    try:
                        write_file("bin/cache_list.json", json.dumps(cache_list, indent=4))
                    except:
                        pass

                await semaphore.acquire()
                task = asyncio.ensure_future(send_channel_req(session, channel_name))
                task.add_done_callback(lambda _: semaphore.release())

                current_attempt += 1

            # we're not using asyncio.gather with a task tracker at the end of a length cycle, as
            # it absolutely KILLS memory usage in the process lol

            end_time = time_monotonic()
            print(f"^^ Cycle for @{length} chars took: {end_time - start_time:.3f} seconds ^^")

            # increase the len for the next cycle!
            length += 1

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nKeyboardInterrupt received, exiting..")
    sys_exit()
except Exception as err:
    print(f"[CRITICAL EXIT] Unhandled exception: {err}")
    sys_exit()
