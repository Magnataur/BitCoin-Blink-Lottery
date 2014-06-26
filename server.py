#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import string
import random

from blink_web.models import Blink, Query, ServerBitcoinAddress
from time import sleep
from random import choice
from bitcoinrpc.connection import BitcoinConnection


BITCOIN_BLINKS_ACTIVE = 3
BITCOIN_NEW_ADDRESSES = 50


def get_unique_account_name():
    chars = string.ascii_uppercase + string.digits
    size = 64
    return ''.join(random.choice(chars) for x in range(size))


def main():
    user='bitcoinrpc'
    password='HZXhX44pkzV5dyK6CpFuCzASvKEn6Ngg3uNPEuSvtMzq'
    host='127.0.0.1'
    port='18332'
    conn = BitcoinConnection(user, password, host, port)

    while True:
        # Step 1: create new blinks
        bs = Blink.objects.filter(active=True)
        if len(bs) < BITCOIN_BLINKS_ACTIVE:
            new_blink = Blink()
            new_blink.save()
            print 'Blink created, id = %s' % (new_blink.pk, )

        bs = Blink.objects.filter(active=False)

        for b in bs:
            qs = Query.objects.filter(blink=b)
            winner = choice(qs)
            winner.player.cash += winner.blink.cash()
            winner.player.save()
            for q in qs:
                q.delete()
                print 'Queue deleted'
            print 'Blink deleted, id = %s'  % (b.pk, )
            b.delete()

        # Step 2: create new bitcoin addresses
        ads = ServerBitcoinAddress.objects.filter(active=False)
        if len(ads) < BITCOIN_NEW_ADDRESSES:
            new_address = ServerBitcoinAddress()
            new_address.account = get_unique_account_name()
            new_address.address = conn.getaccountaddress(new_address.account)
            new_address.save()
            print 'Bitcoin address created, id = %s, accout = %s' % (new_address.pk, new_address.account, )

        sleep(1)


if __name__ == '__main__':
    sys.exit(main())