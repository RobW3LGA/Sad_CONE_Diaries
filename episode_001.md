# Sad CONE Diaries
## Episode One: The YANG Model Menace
"A dog chasing two rabbits will lose both." -a 16th century (paraphrased) proverb

After last week's excellent [introduction][wwt-mdt-link] to YANG, NETConf and RESTConf, it was finally time to get busy.

Very quickly, however, my attempts to correlate YANG models with running-config resulted in considerable frustration.

I discovered that different model styles (Native, IETF and OpenConfig) produce distinct results for a running-config, and differing results often make for broken code -and grandpa's bowling words.

Observe the outputs for the same ethernet interface...

- OpenConfig RESTConf request:
```Python
  moduleUri: str = "openconfig-interfaces:interfaces/interface=GigabitEthernet1" # GET OpenConfig Int
```
```JSON
{
  "openconfig-interfaces:interface":{
    "name":"GigabitEthernet1",
    "config":{
      "name":"GigabitEthernet1",
      "type":"iana-if-type:ethernetCsmacd",
      "description":"This is the OpenConfig model",
      "enabled":true
    },
    "state":{
      "name":"GigabitEthernet1",
      "type":"iana-if-type:ethernetCsmacd",
      "description":"This is the OpenConfig model",
      "enabled":true,
      ...(truncated for brevity)
    }
  }
}
```
- IETF RESTConf request:
```Python
  moduleUri: str = "ietf-interfaces:interfaces/interface=GigabitEthernet1" # GET IETF Int
```
```JSON
{
  "name":"GigabitEthernet1",
  "config":{
    "name":"GigabitEthernet1",
    "type":"iana-if-type:ethernetCsmacd",
    "description":"This is the IETF model",
    "enabled":true
  },
  "state":{
    "name":"GigabitEthernet1",
    "type":"iana-if-type:ethernetCsmacd",
    "description":"This is the IETF model",
    "enabled":true,
    ...(truncated for brevity)
  }
}
```
- Native RESTConf request:
```Python
  moduleUri: str = "native/interface/GigabitEthernet=1" # GET Native Int
```
```JSON
{
  "Cisco-IOS-XE-native:GigabitEthernet":{
    "name":"1",
    "description":"This is the Native model",
    "ip":{
      "address":{
        "primary":{
          "address":"192.168.2.161",
          "mask":"255.255.255.0"
        }
      }
    },
    "mop":{
      "enabled":false,
      "sysid":false
    },
    "Cisco-IOS-XE-ethernet:negotiation":{
      "auto":true
    }
  }
}
```
The IETF and OpenConfig models, while largely similar, are still different enough to throw an error.

My instinct was to burn it all down and start again as simple as possible.

I decided to focus solely on learning to read and output config values; and center around RESTConf, JSON, the Native models and [simple, flexible python code][scd-001-demo]. (Feel free to use this code to follow along and then experiment on your own.)

Turns out, native YANG modeling can be nearly code-transparent. Now...

- Starting with the running-config as a guide and converting to JSON (paste to a .json file in VS Code and `SHIFT+ALT+F`, OR paste to a [JSON formatter][json-formatter-link] and "Process"):
```Python
  moduleUri: str = "native" # GET the running-config
```
- Access the version (because it's right there at the top):
```Python
  moduleUri: str = "native/version" # GET the IOS version
```
```JSON
  {"Cisco-IOS-XE-native:version": "16.12"}
```
- Drill down into the memory:
```Python
  moduleUri: str = "native/memory/free/low-watermark/processor" # GET available memory
```
```JSON
  {"Cisco-IOS-XE-native:processor": 72342}
```
- Time to get into a list (the one with the square [] brackets):
```Python
  moduleUri: str = "native/call-home/profile" # GET a list
```
```JSON
  {"Cisco-IOS-XE-call-home:profile": [{"profile-name": "CiscoTAC-1", "active": true}]}
```
Getting the whole list was easy, but how about the items in the list?
- MOST members of a list can easily be accessed by their first value (referenced as the "key" in YANG parlance):
```Python
  moduleUri: str = "native/call-home/profile=CiscoTAC-1" # GET a list item by name
```
```JSON
  {"Cisco-IOS-XE-call-home:profile": {"profile-name": "CiscoTAC-1", "active": true}}
```
- As network engineers inevitably do, we wander down to the interfaces to experiment with lists again:
```Python
  moduleUri: str = "native/interface/GigabitEthernet=1/negotiation" # GET an item inside a list item
```
```JSON
  {"Cisco-IOS-XE-ethernet:negotiation": {"auto": true}}
```

### Sad CONE's final thought...
Eventually I did spend time exploring the other two model styles and they were much easier to navigate from a "Native" frame of reference.

There are some fun features that will require another model style, but for starting out: the natives will play.

### Join us next time for "How To Change An Interface Setting", or: "Aww crap, I just bricked it."

[wwt-mdt-link]: https://www.wwt.com/lab/programmability-foundations-lab
[scd-001-demo]: https://github.com/RobW3LGA/Sad_CONE_Diaries/blob/master/episode_001.py
[json-formatter-link]: https://jsonformatter.curiousconcept.com