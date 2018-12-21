# -*- coding: utf-8 -*-

"""Generate the Resilient customizations required for avalon"""

from __future__ import print_function
from resilient_circuits.util import *

def codegen_reload_data():
    """Parameters to codegen used to generate the avalon package"""
    reload_params = {"package": u"avalon",
                    "incident_fields": [], 
                    "action_fields": [], 
                    "functions_params": [], 
                    "datatables": [], 
                    "message_destinations": [u"avalon_connector"], 
                    "functions": [u"avalon_refresh_artifact"], 
                    "phases": [], 
                    "automatic_tasks": [], 
                    "scripts": [], 
                    "workflows": [],
                    "actions": [u"Avalon: Create Workspace"] 
                    }
    return reload_params


def customization_data(client=None):
    """Produce any customization definitions (types, fields, message destinations, etc)
       that should be installed by `resilient-circuits customize`
    """

    # This import data contains:
    #   Message Destinations:
    #     avalon_connector
    #   Functions:
    #     avalon_refresh_artifact
    #   Rules:
    #     Avalon: Create Workspace


    yield ImportDefinition(u"""
eyJpZCI6IDksICJmaWVsZHMiOiBbeyJjaG9zZW4iOiBmYWxzZSwgImludGVybmFsIjogZmFsc2Us
ICJ1dWlkIjogImMzZjBlM2VkLTIxZTEtNGQ1My1hZmZiLWZlNWNhMzMwOGNjYSIsICJvcGVyYXRp
b25zIjogW10sICJ2YWx1ZXMiOiBbXSwgImNoYW5nZWFibGUiOiB0cnVlLCAiaWQiOiAzOCwgIm5h
bWUiOiAiaW5jX3RyYWluaW5nIiwgInRleHQiOiAiU2ltdWxhdGlvbiIsICJwcmVmaXgiOiBudWxs
LCAidHlwZV9pZCI6IDAsICJ0b29sdGlwIjogIldoZXRoZXIgdGhlIGluY2lkZW50IGlzIGEgc2lt
dWxhdGlvbiBvciBhIHJlZ3VsYXIgaW5jaWRlbnQuICBUaGlzIGZpZWxkIGlzIHJlYWQtb25seS4i
LCAiaW5wdXRfdHlwZSI6ICJib29sZWFuIiwgImhpZGVfbm90aWZpY2F0aW9uIjogZmFsc2UsICJk
ZWZhdWx0X2Nob3Nlbl9ieV9zZXJ2ZXIiOiBmYWxzZSwgImJsYW5rX29wdGlvbiI6IGZhbHNlLCAi
b3BlcmF0aW9uX3Blcm1zIjoge30sICJyZWFkX29ubHkiOiB0cnVlLCAicmljaF90ZXh0IjogZmFs
c2UsICJleHBvcnRfa2V5IjogImluY2lkZW50L2luY190cmFpbmluZyIsICJ0ZW1wbGF0ZXMiOiBb
XX1dLCAicGhhc2VzIjogW10sICJvdmVycmlkZXMiOiBbXSwgImFjdGlvbnMiOiBbeyJpZCI6IDE1
LCAibmFtZSI6ICJBdmFsb246IENyZWF0ZSBXb3Jrc3BhY2UiLCAidHlwZSI6IDEsICJvYmplY3Rf
dHlwZSI6ICJpbmNpZGVudCIsICJjb25kaXRpb25zIjogW10sICJhdXRvbWF0aW9ucyI6IFtdLCAi
bWVzc2FnZV9kZXN0aW5hdGlvbnMiOiBbIkF2YWxvbiBDb25uZWN0b3IiXSwgIndvcmtmbG93cyI6
IFtdLCAidmlld19pdGVtcyI6IFtdLCAidGltZW91dF9zZWNvbmRzIjogODY0MDAsICJ1dWlkIjog
IjI2MWY2YWQyLWJhNjgtNGNkMS1hZDIzLTZiNWZiOWNjYzY5YiIsICJleHBvcnRfa2V5IjogIkF2
YWxvbjogQ3JlYXRlIFdvcmtzcGFjZSIsICJsb2dpY190eXBlIjogImFsbCJ9XSwgImxheW91dHMi
OiBbXSwgIm5vdGlmaWNhdGlvbnMiOiBudWxsLCAidGltZWZyYW1lcyI6IG51bGwsICJpbmR1c3Ry
aWVzIjogbnVsbCwgInJlZ3VsYXRvcnMiOiBudWxsLCAiZ2VvcyI6IG51bGwsICJmdW5jdGlvbnMi
OiBbeyJpZCI6IDEsICJuYW1lIjogImF2YWxvbl9yZWZyZXNoX2FydGlmYWN0IiwgImRlc2NyaXB0
aW9uIjogeyJmb3JtYXQiOiAidGV4dCIsICJjb250ZW50IjogIlJlZnJlc2hlcyBhcnRpZmFjdCBk
YXRhIGZyb20gYXJ0aWZhY3QgbGlua2VkIEF2YWxvbiB3b3Jrc3BhY2UifSwgInV1aWQiOiAiZDg0
NzhiY2UtMzBjOC00ZDE0LTg0MmItOGVlMzgzZTM0YWM0IiwgInZlcnNpb24iOiAwLCAiY3JlYXRv
ciI6IHsiaWQiOiAxLCAidHlwZSI6ICJ1c2VyIiwgIm5hbWUiOiAidmFsQGtpbmdhbmR1bmlvbi5j
b20iLCAiZGlzcGxheV9uYW1lIjogIlZhbCBLYW50Y2hldiJ9LCAid29ya2Zsb3dzIjogW10sICJk
aXNwbGF5X25hbWUiOiAiQXZhbG9uOiBSZWZyZXNoIEFydGlmYWN0IiwgImRlc3RpbmF0aW9uX2hh
bmRsZSI6ICJhdmFsb25fY29ubmVjdG9yIiwgImV4cG9ydF9rZXkiOiAiYXZhbG9uX3JlZnJlc2hf
YXJ0aWZhY3QiLCAibGFzdF9tb2RpZmllZF9ieSI6IHsiaWQiOiAxLCAidHlwZSI6ICJ1c2VyIiwg
Im5hbWUiOiAidmFsQGtpbmdhbmR1bmlvbi5jb20iLCAiZGlzcGxheV9uYW1lIjogIlZhbCBLYW50
Y2hldiJ9LCAibGFzdF9tb2RpZmllZF90aW1lIjogMTU0NTM2Njk4ODg4OCwgInZpZXdfaXRlbXMi
OiBbXX1dLCAic2VydmVyX3ZlcnNpb24iOiB7Im1ham9yIjogMzAsICJtaW5vciI6IDAsICJidWls
ZF9udW1iZXIiOiAzNDc2LCAidmVyc2lvbiI6ICIzMC4wLjM0NzYifSwgImV4cG9ydF9mb3JtYXRf
dmVyc2lvbiI6IDIsICJleHBvcnRfZGF0ZSI6IDE1NDUzNjcyMjI5ODQsICJpbmNpZGVudF90eXBl
cyI6IFt7InVwZGF0ZV9kYXRlIjogMTU0NTM2NzQ2NDc3OCwgImNyZWF0ZV9kYXRlIjogMTU0NTM2
NzQ2NDc3OCwgInV1aWQiOiAiYmZlZWMyZDQtMzc3MC0xMWU4LWFkMzktNGEwMDA0MDQ0YWEwIiwg
ImRlc2NyaXB0aW9uIjogIkN1c3RvbWl6YXRpb24gUGFja2FnZXMgKGludGVybmFsKSIsICJleHBv
cnRfa2V5IjogIkN1c3RvbWl6YXRpb24gUGFja2FnZXMgKGludGVybmFsKSIsICJuYW1lIjogIkN1
c3RvbWl6YXRpb24gUGFja2FnZXMgKGludGVybmFsKSIsICJlbmFibGVkIjogZmFsc2UsICJzeXN0
ZW0iOiBmYWxzZSwgInBhcmVudF9pZCI6IG51bGwsICJoaWRkZW4iOiBmYWxzZSwgImlkIjogMH1d
LCAiYXV0b21hdGljX3Rhc2tzIjogW10sICJtZXNzYWdlX2Rlc3RpbmF0aW9ucyI6IFt7Im5hbWUi
OiAiQXZhbG9uIENvbm5lY3RvciIsICJwcm9ncmFtbWF0aWNfbmFtZSI6ICJhdmFsb25fY29ubmVj
dG9yIiwgImRlc3RpbmF0aW9uX3R5cGUiOiAwLCAiZXhwZWN0X2FjayI6IHRydWUsICJ1c2VycyI6
IFsidmFsQGtpbmdhbmR1bmlvbi5jb20iXSwgInV1aWQiOiAiYzMzMjUwZjQtNzgxMS00NWI1LTg1
OGItZDU5N2QyMjY5YzgxIiwgImV4cG9ydF9rZXkiOiAiYXZhbG9uX2Nvbm5lY3RvciJ9XSwgInRh
c2tfb3JkZXIiOiBbXSwgImFjdGlvbl9vcmRlciI6IFtdLCAidHlwZXMiOiBbXSwgInNjcmlwdHMi
OiBbXSwgImluY2lkZW50X2FydGlmYWN0X3R5cGVzIjogW10sICJ3b3JrZmxvd3MiOiBbXSwgInJv
bGVzIjogW10sICJ3b3Jrc3BhY2VzIjogW119
"""
    )