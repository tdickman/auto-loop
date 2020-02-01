import sys

from autoloop import lnd, loop, models


@models.db.atomic('IMMEDIATE')
def loop_out(chan_id, amount):
    response = loop.loop_out(chan_id, amount)
    pub_key = lnd.get_channel(chan_id).node2_pub
    models.Swap.create(
        id=response.id,
        chan_id=chan_id,
        pub_key=pub_key,
    )


def print_swap(swap):
    payload = '{htlc_address} - {chan_id} - {amount} sats'.format(
        htlc_address=swap.htlc_address,
        chan_id=swap.chan_id,
        amount=swap.amount,
    )
    if swap.cost_server is not None:
        payload += ' - server {cost_server} onchain {cost_onchain} offchain {cost_offchain} - {state}'.format(
            **swap.__dict__['__data__']
        )
    payload += ' - {}'.format(models.SwapState[swap.state])
    print(payload)


def persist_swap_updates():
    for update in loop.get_swap_updates():
        with models.db.atomic('IMMEDIATE'):
            swap = models.Swap.select().where(models.Swap.id==update.id).first()
            if not swap:
                swap = models.Swap.create(id=update.id)
            swap.amount = update.amt
            swap.state = update.state
            swap.start_time = update.initiation_time
            swap.last_update_time = update.last_update_time
            swap.htlc_address = update.htlc_address
            swap.cost_server = update.cost_server
            swap.cost_onchain = update.cost_onchain
            swap.cost_offchain = update.cost_offchain
            swap.save()
            print_swap(swap)


if __name__ == '__main__':
    loop_out(int(sys.argv[1]), 2000000)
