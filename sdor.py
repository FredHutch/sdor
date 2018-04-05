import logging
import pprint
import argparse
from swiftclient.service import SwiftService, SwiftError
from sys import argv

logging.basicConfig(level=logging.ERROR)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("swiftclient").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("container")
parser.add_argument('-p','--prefix', help='object prefix')
parser.add_argument('-d','--delete', help='delete found objects', action='store_true')
parser.add_argument('-l','--list', help='list found objects', action='store_true')
parser.add_argument('-s','--stat', help='stat found objects', action='store_true')
args = parser.parse_args()

with SwiftService() as swift:

    try:
        list_parts_gen = swift.list(container=args.container, options={'prefix':args.prefix})
        for page in list_parts_gen:
            if page['success']:
                for item in page['listing']:
                   if item["content_type"] == u'application/directory' and item["bytes"] == 0:

                       if args.delete:
                           del_iter = swift.delete(container=args.container, objects=[item["name"]])
                           for del_res in del_iter:
                               con = del_res.get('container', '')
                               obj = del_res.get('objects', '')
                               att = del_res.get('attempts', '')
                               if del_res['success'] and not del_res['action'] == 'bulk_delete':
                                   rd = del_res.get('response_dict')
                                   if rd is not None:
                                       msg = "Successfully deleted {0}/{1} in {2} attempts".format(con,obj,att)
                                       t = dict(rd.get('headers', {}))
                                       if t:
                                           msg = msg + " (transaction id: {0})".format(t)
                                       print(msg)
                       elif args.list:
                           pprint.pprint(item)
                       elif args.stat:
                           metadata = swift.stat(container=args.container, objects=[item["name"]])
                           for md in metadata:
                               if md['success']:
                                   pprint.pprint(md['headers'])
                               else:
                                   logger.error("stat failed on %s" % md['object'])
            else:
                raise page["error"]

    except SwiftError as e:
        logger.error(e.value)
