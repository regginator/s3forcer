# s3forcer

the funny setup.rbxcdn.com raw bruteforce grid thing:tm:

## Install

1. Clone the repository via `git`:

    ```txt
    git clone https://github.com/regginator/s3forcer.git
    cd s3forcer
    ```

2. Install requirements ([`aiohttp`](https://pypi.org/project/aiohttp/)) via pip:

    ```txt
    pip install -r requirements.txt
    ```

## Usage

`python3 main.py --help` (`py` instead of `python3` on Windows)

```txt
usage: main.py [-h] [--min-length MIN_LENGTH] [--chars CHARS] [--prefix PREFIX]
               [--attempt-milestone ATTEMPT_MILESTONE] [--workers WORKERS]
               [--webhook-url WEBHOOK_URL] [--reset-cache]

s3 funny hacking

options:
  -h, --help            show this help message and exit
  --min-length MIN_LENGTH
                        Minimum character length of channel name combonations to bruteforce
  --chars CHARS         Characters (in a single string) to use for channel name combonations
  --prefix PREFIX       Prefix for channel names (e.g. "zfeature")
  --attempt-milestone ATTEMPT_MILESTONE
                        Number of attempts between cache writes and milestone prints
  --workers WORKERS     Number of max thread workers to use
  --webhook-url WEBHOOK_URL
                        Discord webhook URL for found channel notifications
  --reset-cache         Reset bin/cache_list.json
```

### Extra Notes

* To quit the process and stop the request session, you need to use a keyboard interrupt (`Ctrl+C`) in your terminal, or just cancel the process directly through whatever you're using.

* If you get immediate request errors, try toggling `--workers` to a number lower than the default of `250`! You may need to mess with this flag a bit to get the most desirable result for your own personal machine/network.

* If you're annoyed at how often the "Milestone of (n) reached.." message is, you can toggle `--attempt-milestone` (which is the multiplier this uses) to a higher number! *This flag is also used for how often the session should write to the cache, which is what s3forcer uses to pick up (roughly) where you left off on a certain length cycle of your current prefix+char configuration, incase you exit the program or there's an uncaught error for whatever reason.*

* Lastly, `--webhook-url` is optional, and accepts a string of a [Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) URL. When the session finds a channel not already in `bin/channels.json`, it'll send a `POST` request to the Webhook in question with the channel name, and DeployHistory link.

<sub>

*P.S., just try to figure everything else out yourself from the `--help` prompt; this is provided with zero extra support or warranty <3*

</sub>

## License

```txt
MIT License

Copyright (c) 2023 Reggie <reggie@latte.to>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
