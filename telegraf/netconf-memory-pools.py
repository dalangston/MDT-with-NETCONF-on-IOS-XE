from typing import Dict
from ncclient import manager
import xmltodict
import json
from dotenv import load_dotenv
import os
import yaml

def dict_to_telegraf_json(rpc_reply_dict: Dict) -> str:
    """
    """

    memory_stats_array = []

    for memory_entry in rpc_reply_dict["rpc-reply"]["data"]["memory-statistics"]["memory-statistic"]:
        memory_dict = {
            "name": memory_entry["name"],
            "percent_used": ( int(memory_entry["used-memory"])/int(memory_entry["total-memory"]) ) * 100,
            "field": "memory_pool"
        }  # need to use the sum by clause on PromQL to find freed bytes in CPU
        memory_stats_array.append(memory_dict)

    return json.dumps(memory_stats_array)  # return JSON formatted data

def main():
    load_dotenv()

    with open('networkdevices.yml', 'r') as file:
        config = yaml.safe_load(file)

    # https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/16111/Cisco-IOS-XE-memory-oper.yang
    netconf_filter = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <memory-statistics xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper">
                <memory-statistic>
                    <name/>
                    <used-memory/>
                    <total-memory/>
                </memory-statistic>
            </memory-statistics>
        </filter>
        """        

    for deviceIndex in range(0, len(config['devices'])):
        for credential in config['devices'][deviceIndex]['credentials']:
            try:
                with manager.connect(
                    host = config['devices'][deviceIndex]['host'],  # Locally connected device. Will eventually make this a configurable item
                    port = config['devices'][deviceIndex]['port'],
                    username = credential['username'],
                    password = os.getenv(credential['password_env']),  # <--------- enter device password
                    hostkey_verify = bool(config['devices'][deviceIndex]['hostkey_verify']),
                    device_params = config['devices'][deviceIndex]['device_params']
                ) as m:
                    netconf_rpc_reply = m.get(
                        filter = netconf_filter
                    ).xml
                break
            except:
                if deviceIndex == len(config['devices']):
                    exit(1)
                else:
                    continue

        netconf_reply_dict = xmltodict.parse(netconf_rpc_reply)
        telegraf_json_input = dict_to_telegraf_json(netconf_reply_dict)

        # telegraf needs data in a certain data format.
        # I have chosen JSON data that will be picked up by the exec plugin
        print(telegraf_json_input)

if __name__ == "__main__":
    main()