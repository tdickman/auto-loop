import codecs, grpc, os
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc

LND_DIR = os.path.expanduser('~/.lnd')
macaroon = codecs.encode(open(os.path.join(LND_DIR, 'data/chain/bitcoin/mainnet/readonly.macaroon'), 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open(os.path.join(LND_DIR, 'tls.cert'), 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', ssl_creds)
stub = lnrpc.LightningStub(channel)


def get_channels():
    request = ln.ListChannelsRequest(public_only=True)
    return stub.ListChannels(request, metadata=[('macaroon', macaroon)]).channels


def get_channel(chan_id):
    request = ln.ChanInfoRequest(chan_id=chan_id)
    return stub.GetChanInfo(request, metadata=[('macaroon', macaroon)])


def get_info():
    request = ln.GetInfoRequest()
    return stub.GetInfo(request, metadata=[('macaroon', macaroon)])
