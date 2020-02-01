from autoloop import loop, storage


def print_swap(swap):
    payload = '{htlc_address} - {chan_id} - {amount} sats'.format(
        **swap.__dict__['__data__']
    )
    if swap.cost_server is not None:
        payload += ' - server {cost_server} onchain {cost_onchain} offchain {cost_offchain} - {state}'.format(
            **swap.__dict__['__data__']
        )
    payload += ' - {}'.format(storage.SwapState[swap.state])
    print(payload)


def persist_swap_updates():
    for update in loop.get_swap_updates():
        with storage.db.atomic('IMMEDIATE'):
            swap = storage.Swap.get(id=update.id)
            swap.amount = update.amt
            swap.state = update.state
            swap.start_time = update.initiation_time
            swap.last_update_time = update.last_update_time
            swap.htlc_address = update.htlc_address
            swap.save()
            print_swap(swap)


if __name__ == '__main__':
    persist_swap_updates()
