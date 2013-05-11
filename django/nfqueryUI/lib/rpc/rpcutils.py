from nfqueryUI.lib.rpc.JsonRpcClient import Client

def get_log_from_query_severity():
    client = Client()
    result = client.call('get_log')
    return result

def get_total_severity_from_queryserver(latest_timestamp, host):
    client = Client()
    result = client.call('get_total_severity', latest_timestamp, host)
    return result

