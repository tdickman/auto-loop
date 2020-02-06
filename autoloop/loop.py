import grpc
import client_pb2 as loop
import client_pb2_grpc as looprpc
import time

from . import config


def get_swap_updates():
    channel = grpc.insecure_channel('localhost:11010')
    stub = looprpc.SwapClientStub(channel)
    request = loop.MonitorRequest()
    for response in stub.Monitor(request):
        yield response


def loop_out(chan_id, amount):
    channel = grpc.insecure_channel('localhost:11010')
    stub = looprpc.SwapClientStub(channel)
    request = loop.LoopOutRequest(
        amt=amount,
        max_swap_routing_fee=config.MAX_SWAP_ROUTING_FEE,
        max_prepay_routing_fee=config.MAX_PREPAY_ROUTING_FEE,
        max_swap_fee=config.MAX_SWAP_FEE,
        max_prepay_amt=config.MAX_PREPAY_AMT,
        max_miner_fee=config.MAX_MINER_FEE,
        loop_out_channel=chan_id,
        sweep_conf_target=config.CONF_TARGET,
        swap_publication_deadline=int(time.time() + config.LOOP_OUT_PUBLICATION_DELAY_SECONDS)
    )
    response = stub.LoopOut(request)
    return response


def get_quote(amount, conf_target):
    channel = grpc.insecure_channel('localhost:11010')
    stub = looprpc.SwapClientStub(channel)
    request = loop.QuoteRequest(
        amt=amount,
        conf_target=conf_target,

    )
    response = stub.LoopOutQuote(request)
    return response
