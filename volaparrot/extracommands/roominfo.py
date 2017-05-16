"""
The MIT License (MIT)
Copyright © 2017 RealDolos & Szeraton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import logging

from time import time
from time import strftime
from time import localtime
from io import BytesIO

from .command import Command

__all__ = ["RoomInfoCommand"]

LOGGER = logging.getLogger(__name__)

FAC = 1024.0 * 1024.0 * 1024.0

class RoomInfoCommand(Command):

    handlers = "!roominfo", "!rumfo"
    last_check = 0

    def handle_cmd(self, cmd, remainder, msg):
        if RoomInfoCommand.last_check + 120 > time():
            return
        if not self.allowed(msg):
            self.post("{}: No room infos for you!".format(msg.nick))
            return True
        RoomInfoCommand.last_check = time()
        info = []
        info += "{:>20}: {}".format("Owner", self.conf_key("owner")),
        info += "{:>20}: {}".format("MOTD", self.conf_key("motd")),
        info += "{:>21} {}".format("Is room deactivated?", self.conf_key("disabled")),
        info += "{:>20}: {} hours".format("File time to live", int(self.conf_key("ttl")/3600)),
        info += "{:>20}: {:.2f} GiB".format("Max file size", self.conf_key("max_file")/FAC),
        info += "{:>20}: {}".format("Max message length", self.conf_key("max_message")),
        info += "{:>20}: {}".format("Room creation time", \
            strftime("%a, %d %b %Y %H:%M:%S", localtime(self.conf_key("creation_time")))),
        info = "\n".join(info)
        LOGGER.warning("\n%s", info)
        info = bytes(info, "utf-8")
        if self.active:
            fid = self.room.upload_file(
                BytesIO(info), upload_as="infos.txt")
        if fid:
            self.post("{}: @{}", msg.nick, fid)
        return True

    def conf_key(self, key):
        return self.room.config.get(key)
