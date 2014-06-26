#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys


from bitcoinrpc.connection import BitcoinConnection



def main():
    user='bitcoinrpc'
    password='HZXhX44pkzV5dyK6CpFuCzASvKEn6Ngg3uNPEuSvtMzq'
    host='127.0.0.1'
    port='18332'
    conn = BitcoinConnection(user, password, host, port)



if __name__ == '__main__':
    sys.exit(main())
