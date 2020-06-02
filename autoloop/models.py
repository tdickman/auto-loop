import peewee

db = peewee.SqliteDatabase("swaps.db")


def print_all():
    for swap in Swap.select():
        if swap.state == 3:
            print(swap.__dict__["__data__"])


def export_to_csv():
    keys = Swap.select()[0].__dict__["__data__"].keys()
    print(",".join(keys))
    for swap in Swap.select():
        if swap.state == 3:
            data = swap.__dict__["__data__"]
            print(",".join([str(data[k]) for k in keys]))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Swap(BaseModel):
    id = peewee.CharField(primary_key=True)
    chan_id = peewee.BigIntegerField(null=True)
    pub_key = peewee.CharField(null=True)
    amount = peewee.BigIntegerField(null=True)
    state = peewee.IntegerField(null=True)
    start_time = peewee.BigIntegerField(null=True)
    last_update_time = peewee.BigIntegerField(null=True)
    htlc_address = peewee.CharField(null=True)
    cost_server = peewee.BigIntegerField(null=True)
    cost_onchain = peewee.BigIntegerField(null=True)
    cost_offchain = peewee.BigIntegerField(null=True)


SwapState = [
    "Initiated",
    "Preimage Revealed",
    "HTLC Published",
    "Success",
    "Failed",
    "Invoice Settled",
]


db.create_tables([Swap])

# from playhouse.migrate import *
# migrator = SqliteMigrator(db)
# migrate(
#     migrator.add_column('Swap', 'pub_key', peewee.CharField(null=True)),
# )

if __name__ == "__main__":
    export_to_csv()
