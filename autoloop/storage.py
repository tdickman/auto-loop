import peewee

db = peewee.SqliteDatabase('swaps.db')


def print_all():
    for swap in Swap.select():
        print(swap.__dict__['__data__'])


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Swap(BaseModel):
    id = peewee.CharField(primary_key=True)
    chan_id = peewee.BigIntegerField(null=True)
    amount = peewee.BigIntegerField(null=True)
    state = peewee.IntegerField(null=True)
    start_time = peewee.BigIntegerField(null=True)
    last_update_time = peewee.BigIntegerField(null=True)
    htlc_address = peewee.CharField(null=True)
    cost_server = peewee.BigIntegerField(null=True)
    cost_onchain = peewee.BigIntegerField(null=True)
    cost_offchain = peewee.BigIntegerField(null=True)


SwapState = [
    'Initiated',
    'Preimage Revealed',
    'HTLC Published',
    'Success',
    'Failed',
    'Invoice Settled',
]


db.create_tables([Swap])
