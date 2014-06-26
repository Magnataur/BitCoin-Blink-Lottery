from django.db import models


class Blink(models.Model):
    size = models.PositiveSmallIntegerField(default=6)
    active = models.BooleanField(default=True)
    bet = models.FloatField(default=0.01)

    def cash(self):
        return self.bet * (self.size - 1)

    def range(self):
        return xrange(self.size)

    def vacancies(self):
        """return free places into the blink"""
        all = list(range(self.size))
        occupied = [n.place for n in self.query_set.all()]
        for n in occupied:
            all.remove(n)
        return all


class ServerBitcoinAddress(models.Model):
    account = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.address

class BitcoinPlayer(models.Model):
    address = models.CharField(max_length=64)
    wallet = models.ForeignKey(ServerBitcoinAddress)
    cash = models.FloatField(default=10)


class Query(models.Model):
    blink = models.ForeignKey(Blink)
    player = models.ForeignKey(BitcoinPlayer)
    place = models.PositiveSmallIntegerField()

