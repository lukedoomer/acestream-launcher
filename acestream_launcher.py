#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Acestream Launcher: Open acestream links with any media player"""

import sys
import time
import hashlib
import argparse
import psutil
import pexpect

class AcestreamLauncher(object):
    """Acestream Launcher"""

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog='acestream-launcher',
            description='Open acestream links with any media player'
        )
        parser.add_argument(
            'url',
            metavar='URL',
            help='the acestream url to play'
        )
        parser.add_argument(
            '--engine',
            help='the acestream engine socket to use (default: localhost:62062)',
            default='localhost:62062'
        )
        parser.add_argument(
            '--player',
            help='the media player to use (default: vlc)',
            default='vlc'
        )

        self.appname = 'Acestream Launcher'
        self.args = parser.parse_args()

        self.start_session()
        self.start_player()
        self.close_player()

    def start_session(self):
        """Start acestream telnet session"""

        product_key = 'n51LvQoTlJzNGaFxseRK-uvnvX-sD4Vm5Axwmc4UcoD-jruxmKsuJaH0eVgE'
        self.socketArgs = self.args.engine.split(':')
        session = pexpect.spawn('telnet {0} {1}'.format(self.socketArgs[0], self.socketArgs[1]))

        try:
            session.timeout = 10
            session.sendline('HELLOBG version=3')
            session.expect('key=.*')

            request_key = session.after.decode('utf-8').split()[0].split('=')[1]
            signature = (request_key + product_key).encode('utf-8')
            signature = hashlib.sha1(signature).hexdigest()
            response_key = product_key.split('-')[0] + '-' + signature
            pid = self.args.url.split('://')[1]

            session.sendline('READY key=' + response_key)
            session.expect('AUTH.*')
            session.sendline('USERDATA [{"gender": "1"}, {"age": "3"}]')

        except (pexpect.TIMEOUT, pexpect.EOF):
            self.close_player(1)

        try:
            session.timeout = 30
            session.sendline('START PID ' + pid + ' 0')
            session.expect('http://.*')

            self.session = session
            self.url = session.after.decode('utf-8').split()[0]

        except (pexpect.TIMEOUT, pexpect.EOF):
            self.close_player(1)

    def start_player(self):
        """Start the media player"""

        self.playerArgs = self.args.player.split()
        self.playerArgs.append(self.url)
        self.player = psutil.Popen(self.playerArgs)
        self.player.wait()
        self.session.sendline('STOP')
        self.session.sendline('SHUTDOWN')

    def close_player(self, code=0):
        """Close acestream and media player"""

        try:
            self.player.kill()
        except (AttributeError, psutil.NoSuchProcess):
            print('Media Player not running...')

        try:
            self.acestream.kill()
        except (AttributeError, psutil.NoSuchProcess):
            print('Acestream not running...')

        sys.exit(code)

def main():
    """Start Acestream Launcher"""

    try:
        AcestreamLauncher()
    except (KeyboardInterrupt, EOFError):
        print('Acestream Launcher exiting...')

        sys.exit(0)

main()
