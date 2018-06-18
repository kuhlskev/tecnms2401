from argparse import ArgumentParser
import ncclient.manager
import xml.dom.minidom
from ncclient.operations import TimeoutExpiredError
import pprint

#xml_file = 'bgp_conf.xml'
xml_file = 'eigrp_conf.xml'
#xml_file = 'hostname.xml'

def main():
  parser = ArgumentParser(description='Select options.')
  # Input parameters
  parser.add_argument('--host', type=str, default='172.20.20.10',
  help="The device IP or DN")
  parser.add_argument('-u', '--username', type=str, default='vagrant')
  parser.add_argument('-p', '--password', type=str, default='vagrant')
  parser.add_argument('--port', type=int, default=830,
  help="Specify this if you want a non-default port")
  args = parser.parse_args()
  nckwargs = dict(
    host=args.host,
    port=args.port,
    hostkey_verify=False,
    username=args.username,
    password=args.password,
    device_params={'name':"csr"}
  )
  m = ncclient.manager.connect(**nckwargs)
  try:
    with open(xml_file) as f:
      xml_edit = f.read()
      m.edit_config(xml_edit, target='running')
    #xmlDom = xml.dom.minidom.parseString(str(c))
    #print (xmlDom.toprettyxml( indent = " " ))
  except TimeoutExpiredError as e:
    print("Operation timeout!")
  #except Exception as e:
  #  print("ERORR severity={}, tag={}".format(e.severity, e.tag))
  m.close_session()
if __name__ == '__main__':
  main()