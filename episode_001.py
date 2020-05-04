import json
import requests
from requests.models import Response
requests.packages.urllib3.disable_warnings()

hostname: str = 'HOSTNAME.local'
user: str     = 'USER'
password: str = 'P@ssw0rd'
restconfUri: str = f"https://{hostname}/restconf/data"


# moduleUri: str = "openconfig-interfaces:interfaces/interface=GigabitEthernet1" # GET OpenConfig Int
# moduleUri: str = "ietf-interfaces:interfaces/interface=GigabitEthernet1" # GET IETF Int
# moduleUri: str = "native/interface/GigabitEthernet=1" GET Native Int

moduleUri: str = "native" # GET the running-config
# moduleUri: str = "native/version" # GET the IOS version
# moduleUri: str = "native/memory/free/low-watermark/processor" # GET available memory
# moduleUri: str = "native/call-home/profile" # GET a list
# moduleUri: str = "native/call-home/profile=CiscoTAC-1" # GET a list item by name
# moduleUri: str = "native/interface/GigabitEthernet=1/negotiation" # GET an item inside a list item


requestHeaders: dict = {
  'Content-Type': 'application/yang-data+json',
  'Accept': 'application/yang-data+json'
}

requestUri: str = f"{restconfUri}/{moduleUri}"

def main():

    response: Response = requests.get(requestUri, auth=(user, password), headers=requestHeaders, verify=False)

    if response.ok:

        try:

            print(json.dumps(response.json()))

        except:

            print(f"Code: {response.status_code}")
            print(response.text)

    else:

        print(f'Response was not OK:\n{response}')

    response.close()


if __name__ == '__main__':

    main()
