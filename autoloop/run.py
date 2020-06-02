import sys
import time

from autoloop import config, lnd, handler
from autoloop.models import Swap


NANO_SECONDS_DAY = 24 * 60 * 60 * (10 ** 9)


def get_eligible_channels():
    """
    Return a list of channels that meet
    the following criteria:

    * utilization > config.LOOP_OUT_PERCENTAGE
    * utilization - LOOP_OUT_AMOUNT > LOOP_OUT_MINIMUM
    * ...
    """

    channels = lnd.get_channels()
    channel_count = {}
    for channel in channels:
        if channel.remote_pubkey not in channel_count:
            channel_count[channel.remote_pubkey] = 0

        channel_count[channel.remote_pubkey] += 1

    for channel in channels:
        if channel.remote_pubkey in config.BLACKLISTED_PUBKEYS:
            continue

        if (
            channel.local_balance / channel.capacity
            < config.LOOP_OUT_PERCENTAGE_TRIGGER
        ):
            continue

        if (
            channel.local_balance - config.LOOP_OUT_AMOUNT
        ) / channel.capacity < config.LOOP_OUT_MINIMUM:
            continue

        most_recent_swap = (
            Swap.select()
            .where(Swap.pub_key == channel.remote_pubkey)
            .order_by(Swap.start_time.desc())
            .first()
        )

        if (
            config.DISABLE_LOOP_FOR_DUPLICATE_CHANNELS
            and channel_count[channel.remote_pubkey] > 1
        ):
            continue

        if most_recent_swap:
            # Pending swap, skip
            if most_recent_swap.state is not None and most_recent_swap.state < 3:
                continue

            # Most recent swap failed, make sure enough time has elapsed
            if most_recent_swap.state == 4:
                if (
                    most_recent_swap.start_time
                    > get_epoch_nano() - config.DAYS_BETWEEN_RETRIES * NANO_SECONDS_DAY
                ):
                    continue

        yield channel


def get_epoch_nano():
    return time.time() * (10 ** 9)


def get_pending_loops():
    return Swap.select().where(
        Swap.state < 3,
        Swap.start_time > get_epoch_nano() - config.MAX_AGE_DAYS * NANO_SECONDS_DAY,
    )


def perform_loop_outs():
    pending_loops = get_pending_loops()
    remaining_loop_outs = config.MAX_PENDING_LOOP_OPERATIONS - pending_loops.count()

    for channel in get_eligible_channels():
        if remaining_loop_outs > 0:
            print(
                "Looping out pubkey {}, channel {}".format(
                    channel.remote_pubkey, channel.chan_id
                )
            )
            handler.loop_out(channel.chan_id, config.LOOP_OUT_AMOUNT)
            remaining_loop_outs -= 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python autoloop/run.py auto | loop_out | monitor | status")
        exit()
    action = sys.argv[1]
    if action == "auto":
        perform_loop_outs()
    elif action == "loop_out":
        chan_id = int(sys.argv[2])
        handler.loop_out(chan_id, config.LOOP_OUT_AMOUNT)
    elif action == "monitor":
        handler.persist_swap_updates()
    elif action == "status":
        for swap in Swap.select().order_by(Swap.start_time):
            handler.print_swap(swap)
