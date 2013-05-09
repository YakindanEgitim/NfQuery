from nfqueryUI.lib.rpc.JsonRpcClient import Client

def get_log_from_query_severity():
    client = Client()
    result = client.call('get_log')
    return result

def get_total_severity_from_query_severity(host):
    client = Client()
    result = client.call('get_total_severity', host)
    return result

