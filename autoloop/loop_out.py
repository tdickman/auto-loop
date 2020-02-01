import sys

from autoloop import loop, storage



@storage.db.atomic('IMMEDIATE')
def loop_out(chan_id, amount):
    response = loop.loop_out(chan_id, amount)
    print(response)
    storage.Swap.create(
        id=response.id,
        chan_id=chan_id,
    )


if __name__ == '__main__':
    loop_out(int(sys.argv[1]), 2000000)
