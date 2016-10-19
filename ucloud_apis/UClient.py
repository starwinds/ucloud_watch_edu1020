#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

from Client import *
from commands import COMMANDS

class UClient(Client):

    """ UCloud Client """

    def run(self, command, args={}, post=None, debug=False, resptype="json"):
        response = self.request(command, args, post=post, debug=debug, resptype=resptype)
        if response is None:
            raise RuntimeError(
                'Response Error : %s' % json.dumps(response, indent=4))

        if __name__ == '__main__':
            dump_result = json.dumps(response, indent=2)
            print dump_result
            f = file('request_result.txt', 'w')
            f.write('%s %s \n %s' % (sys.argv[1],sys.argv[2],dump_result))
            f.close()
        return response

""" Command Line Interface """

def usage_out():
    print "usage: python UClient.py api_type command args"
    print "         api_type : server or lb(loadbalancer) or waf or watch or package"

def parse_param_from_file(dir):
    with open(dir) as param_file:
       temp_dict = json.load(param_file)
    result_dict = dict()
    result_dict['command'] = temp_dict['command']
    result_dict['parameter'] = dict()
    for i_key in temp_dict['parameter']:
       if temp_dict['parameter'][i_key]['required'] == 'yes':
          result_dict['parameter'][i_key] = temp_dict['parameter'][i_key]['param']
    return result_dict

if __name__ == "__main__":
    import sys
    import os

    UCLOUD_RESP_TYPE = "json"
    if "UCLOUD_RESP_TYPE" in os.environ:
        UCLOUD_RESP_TYPE = os.environ["UCLOUD_RESP_TYPE"]

    param_dict = parse_param_from_file(sys.argv[2])

    if len(sys.argv) < 3:
        usage_out()
        exit(-1)

    args = {}

    client  = UClient(api_type=sys.argv[1])

    command = COMMANDS.get(sys.argv[2], None)
      
    client.run(param_dict['command'],param_dict['parameter'],debug=True, resptype=UCLOUD_RESP_TYPE)    
    exit(0)
