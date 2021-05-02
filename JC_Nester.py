from __future__ import print_function
import time
import jcapiv1
from jcapiv1.rest import ApiException
from pprint import pprint


import argparse
import os 
import jcapiv2
from jcapiv2.rest import ApiException

# Jumpcloud Group management Script
# Best Practice (IMHO), is to create source groups that contain business unit members. 
# These groups will be where membership changes happen. 
#   -- SOURCE_Development
#   -- SOURCE_Infrastructure
#   -- SOURCE_Finance

# Then create placeholder application access groups which the SOURCE groups will be copied into
#   -- SAML_AWS
#   -- SAML_Google
#   -- SAML_StackOverflow
#   -- RAD_VPN
#   -- RAD_8021x

# Then use this script to populate the "nested" groups
#     # JC_Nester.py -a combine SOURCE_Development SAML_AWS
#     # JC_Nester.py -a combine SOURCE_Infrastructure SAML_AWS
#     # 
#     # JC_Nester.py -a combine SOURCE_Finance SAML_Google
#     # JC_Nester.py -a combine SOURCE_Development SAML_Google
#     # JC_Nester.py -a combine SOURCE_Infrastructure SAML_Google


# Parse Arguments
parser = argparse.ArgumentParser(description='Fake nested groups in Jumpcloud.')
parser.add_argument('sourcegroup', type=str, nargs='?', help='The source group for the action')
parser.add_argument('destgroup', type=str, nargs='?', help='The destination group for the action')
parser.add_argument('-d', '--dry-run', action="store_true", help="Don't actually write changes")
parser.add_argument('-a', '--action', choices=['overwrite', 'combine'], help="Action to perform")

parser.add_argument('-l', '--list', action="store_true", help="List Jumpcloud groups")
args = parser.parse_args()


# Api Auth
secrets="../.secrets"

def get_file_contents(secrets):
    try:
        with open(secrets, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

api_key = get_file_contents(secrets)


CONTENT_TYPE = "application/json"
ACCEPT = "application/json"

# APIv1 configuration
configuration = jcapiv1.Configuration()
configuration.api_key['x-api-key'] = api_key

# APIv2 CONFIGURATION
CONFIGURATION = jcapiv2.Configuration()
CONFIGURATION.api_key['x-api-key'] = api_key 
API_INSTANCE = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(CONFIGURATION))



def get_groups_list():
    """Retrieve all user groups."""
    try:
        i=0
        groups_list = API_INSTANCE.groups_user_list(CONTENT_TYPE, ACCEPT)
        group_names = [g.name for g in groups_list]   
        group_ids   = [g.id for g in groups_list]
        group_dict = dict(zip(group_ids, group_names))

        for id in group_dict.keys():
            print(id, '->', group_dict[id])
        return

    except ApiException as err:
        print("Exception when calling UserGroupsApi->groups_user_list: %s\n" % err)




def get_users_list():
    api_instance = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configuration))
    content_type = 'application/json' # str |  (default to application/json)
    accept = 'application/json' # str |  (default to application/json)
    limit = 50 # int | The number of records to return at once. (optional) (default to 10)
    skip = 0 # int | The offset into the records to return. (optional) (default to 0)
    sort = '' # str | The comma separated fields used to sort the collection. Default sort is ascending, prefix with `-` to sort descending.  (optional) (default to )
    fields = '' # str | The comma separated fields included in the returned records. If omitted the default list of fields will be returned.  (optional) (default to )
    x_org_id = '' # str |  (optional) (default to )
    search = '' # str | A nested object containing a string `searchTerm` and a list of `fields` to search on. (optional)
    filter = '' # str | A filter to apply to the query. (optional)
        
    try:
        api_response = api_instance.systemusers_list(content_type, accept, limit=limit, skip=skip, sort=sort, fields=fields, x_org_id=x_org_id)#, search=search, filter=filter)
    except ApiException as e:
        print("Exception when calling SystemusersApi->systemusers_list: %s\n" % e)



print(args)
if args.list: 
    get_groups_list()
    get_users_list()
    os._exit(0)
elif args.action in ['overwrite']:
    print("OVERWRITE?!?!")
    get_group_members(args.sourcegroup) 
    os._exit(0)
elif args.action in ["combine"]:
    print("COMBINE!?!?!?")
    os._exit(0)
else:
    os._exit(0)
