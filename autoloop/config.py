MAX_SWAP_ROUTING_FEE = 3000 * 1000
MAX_PREPAY_ROUTING_FEE = 1000 * 1000
MAX_SWAP_FEE = 5000
MAX_PREPAY_AMT = 5000
MAX_MINER_FEE = 3000
CONF_TARGET = 20

# Percentage at which point a loop out is attempted
LOOP_OUT_PERCENTAGE_TRIGGER = 0.7
# Minimum utilization that can exist after a loop out operation
# completes
LOOP_OUT_MINIMUM = 0.2
LOOP_OUT_AMOUNT = 2000000
# Wait a given number of days after a failed loop out attempt
# before trying again
DAYS_BETWEEN_RETRIES = 0.3
MAX_PENDING_LOOP_OPERATIONS = 2
# Don't loop out any peer we have multiple channels with
DISABLE_LOOP_FOR_DUPLICATE_CHANNELS = True

BLACKLISTED_PUBKEYS = [
    '032c17323caa51269b5124cf07a0c03772587ad8199e692cc3aae8397454367d34',
]

# Loops sometimes get "stuck" - we just ignore these
MAX_AGE_DAYS = 2
