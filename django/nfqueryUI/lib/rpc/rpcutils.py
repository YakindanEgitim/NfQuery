from nfqueryUI.lib.rpc.JsonRpcClient import Client

def get_log():
    client = Client()
    result = client.call('get_log')
    return result

