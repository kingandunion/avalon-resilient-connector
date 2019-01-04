# -*- coding: utf-8 -*-

"""Generate the Resilient customizations required for avalon"""

from __future__ import print_function
from resilient_circuits.util import *

def codegen_reload_data():
    """Parameters to codegen used to generate the avalon package"""
    reload_params = {"package": u"avalon",
                    "incident_fields": [u"avalon_last_pull_time", u"avalon_pull_nodes_automatically", u"avalon_workspace_id"], 
                    "action_fields": [], 
                    "functions_params": [], 
                    "datatables": [], 
                    "message_destinations": [u"avalon_actions"], 
                    "functions": [u"avalon_refresh"], 
                    "phases": [], 
                    "automatic_tasks": [], 
                    "scripts": [], 
                    "workflows": [u"avalon_refresh"], 
                    "actions": [u"Avalon: Create Workspace", u"Avalon: Pull Nodes", u"Avalon: Pull Nodes Every 60 min", u"Avalon: Push Artifact", u"Avalon: Push Artifacts"] 
                    }
    return reload_params


def customization_data(client=None):
    """Produce any customization definitions (types, fields, message destinations, etc)
       that should be installed by `resilient-circuits customize`
    """

    # This import data contains:
    #   Incident fields:
    #     avalon_last_pull_time
    #     avalon_pull_nodes_automatically
    #     avalon_workspace_id
    #   Message Destinations:
    #     avalon_actions
    #   Functions:
    #     avalon_refresh
    #   Workflows:
    #     avalon_refresh
    #   Rules:
    #     Avalon: Create Workspace
    #     Avalon: Pull Nodes
    #     Avalon: Pull Nodes Every 60 min
    #     Avalon: Push Artifact
    #     Avalon: Push Artifacts


    yield ImportDefinition(u"""
eyJ0YXNrX29yZGVyIjogW10sICJ3b3JrZmxvd3MiOiBbeyJwcm9ncmFtbWF0aWNfbmFtZSI6ICJh
dmFsb25fcmVmcmVzaCIsICJvYmplY3RfdHlwZSI6ICJpbmNpZGVudCIsICJleHBvcnRfa2V5Ijog
ImF2YWxvbl9yZWZyZXNoIiwgInV1aWQiOiAiZDM4YzY3MWYtZmMzOS00NzQxLWIwMTctNzM0ZjAx
YmUxNjdjIiwgImxhc3RfbW9kaWZpZWRfYnkiOiAidmFsQGtpbmdhbmR1bmlvbi5jb20iLCAibmFt
ZSI6ICJBdmFsb246IFJlZnJlc2giLCAiY29udGVudCI6IHsieG1sIjogIjw/eG1sIHZlcnNpb249
XCIxLjBcIiBlbmNvZGluZz1cIlVURi04XCI/PjxkZWZpbml0aW9ucyB4bWxucz1cImh0dHA6Ly93
d3cub21nLm9yZy9zcGVjL0JQTU4vMjAxMDA1MjQvTU9ERUxcIiB4bWxuczpicG1uZGk9XCJodHRw
Oi8vd3d3Lm9tZy5vcmcvc3BlYy9CUE1OLzIwMTAwNTI0L0RJXCIgeG1sbnM6b21nZGM9XCJodHRw
Oi8vd3d3Lm9tZy5vcmcvc3BlYy9ERC8yMDEwMDUyNC9EQ1wiIHhtbG5zOm9tZ2RpPVwiaHR0cDov
L3d3dy5vbWcub3JnL3NwZWMvREQvMjAxMDA1MjQvRElcIiB4bWxuczpyZXNpbGllbnQ9XCJodHRw
Oi8vcmVzaWxpZW50LmlibS5jb20vYnBtblwiIHhtbG5zOnhzZD1cImh0dHA6Ly93d3cudzMub3Jn
LzIwMDEvWE1MU2NoZW1hXCIgeG1sbnM6eHNpPVwiaHR0cDovL3d3dy53My5vcmcvMjAwMS9YTUxT
Y2hlbWEtaW5zdGFuY2VcIiB0YXJnZXROYW1lc3BhY2U9XCJodHRwOi8vd3d3LmNhbXVuZGEub3Jn
L3Rlc3RcIj48cHJvY2VzcyBpZD1cImF2YWxvbl9yZWZyZXNoXCIgaXNFeGVjdXRhYmxlPVwidHJ1
ZVwiIG5hbWU9XCJBdmFsb246IFJlZnJlc2hcIj48ZG9jdW1lbnRhdGlvbj48IVtDREFUQVtQdWxs
cyBkYXRhIGZyb20gbGlua2VkIEF2YWxvbiB3b3Jrc3BhY2UuIFJlcXVpcmVzIGFuIEF2YWxvbiBX
b3Jrc3BhY2UgdG8gYmUgbGlua2VkIHRvIGFuIGluY2lkZW50LiBZb3UgY2FuIGNyZWF0ZSBhbmQg
bGluayBhbiBBdmFsb24gd29ya3NwYWNlIGFydGlmYWN0IGJ5IGV4ZWN1dGluZyB0aGUgXCJBdmFs
b246IENyZWF0ZSBXb3Jrc3BhY2VcIiBjdXN0b20gbWVudSBjb21tYW5kLl1dPjwvZG9jdW1lbnRh
dGlvbj48c3RhcnRFdmVudCBpZD1cIlN0YXJ0RXZlbnRfMXl0azg5Z1wiPjxvdXRnb2luZz5TZXF1
ZW5jZUZsb3dfMGljbnZkejwvb3V0Z29pbmc+PC9zdGFydEV2ZW50PjxzZXJ2aWNlVGFzayBpZD1c
IlNlcnZpY2VUYXNrXzEzeXM4YzVcIiBuYW1lPVwiYXZhbG9uX3JlZnJlc2hcIiByZXNpbGllbnQ6
dHlwZT1cImZ1bmN0aW9uXCI+PGV4dGVuc2lvbkVsZW1lbnRzPjxyZXNpbGllbnQ6ZnVuY3Rpb24g
dXVpZD1cIjRiY2MyZGYxLWM2MGMtNGY2Mi04NzlhLTAyNGNiMTUwYTE5ZVwiPntcImlucHV0c1wi
Ont9fTwvcmVzaWxpZW50OmZ1bmN0aW9uPjwvZXh0ZW5zaW9uRWxlbWVudHM+PGluY29taW5nPlNl
cXVlbmNlRmxvd18xa2FqdWx6PC9pbmNvbWluZz48b3V0Z29pbmc+U2VxdWVuY2VGbG93XzBxOWli
eG08L291dGdvaW5nPjwvc2VydmljZVRhc2s+PGluY2x1c2l2ZUdhdGV3YXkgaWQ9XCJJbmNsdXNp
dmVHYXRld2F5XzFyd3I4dWpcIj48aW5jb21pbmc+U2VxdWVuY2VGbG93XzBpY252ZHo8L2luY29t
aW5nPjxpbmNvbWluZz5TZXF1ZW5jZUZsb3dfMHE5aWJ4bTwvaW5jb21pbmc+PG91dGdvaW5nPlNl
cXVlbmNlRmxvd18xa2FqdWx6PC9vdXRnb2luZz48L2luY2x1c2l2ZUdhdGV3YXk+PHNlcXVlbmNl
RmxvdyBpZD1cIlNlcXVlbmNlRmxvd18waWNudmR6XCIgc291cmNlUmVmPVwiU3RhcnRFdmVudF8x
eXRrODlnXCIgdGFyZ2V0UmVmPVwiSW5jbHVzaXZlR2F0ZXdheV8xcndyOHVqXCIvPjxzZXF1ZW5j
ZUZsb3cgaWQ9XCJTZXF1ZW5jZUZsb3dfMHE5aWJ4bVwiIHNvdXJjZVJlZj1cIlNlcnZpY2VUYXNr
XzEzeXM4YzVcIiB0YXJnZXRSZWY9XCJJbmNsdXNpdmVHYXRld2F5XzFyd3I4dWpcIi8+PHNlcXVl
bmNlRmxvdyBpZD1cIlNlcXVlbmNlRmxvd18xa2FqdWx6XCIgc291cmNlUmVmPVwiSW5jbHVzaXZl
R2F0ZXdheV8xcndyOHVqXCIgdGFyZ2V0UmVmPVwiU2VydmljZVRhc2tfMTN5czhjNVwiLz48L3By
b2Nlc3M+PGJwbW5kaTpCUE1ORGlhZ3JhbSBpZD1cIkJQTU5EaWFncmFtXzFcIj48YnBtbmRpOkJQ
TU5QbGFuZSBicG1uRWxlbWVudD1cInVuZGVmaW5lZFwiIGlkPVwiQlBNTlBsYW5lXzFcIj48YnBt
bmRpOkJQTU5TaGFwZSBicG1uRWxlbWVudD1cIlN0YXJ0RXZlbnRfMXl0azg5Z1wiIGlkPVwiU3Rh
cnRFdmVudF8xeXRrODlnX2RpXCI+PG9tZ2RjOkJvdW5kcyBoZWlnaHQ9XCIzNlwiIHdpZHRoPVwi
MzZcIiB4PVwiMTE4XCIgeT1cIjIwM1wiLz48YnBtbmRpOkJQTU5MYWJlbD48b21nZGM6Qm91bmRz
IGhlaWdodD1cIjEzXCIgd2lkdGg9XCI5MFwiIHg9XCI5MVwiIHk9XCIyNDJcIi8+PC9icG1uZGk6
QlBNTkxhYmVsPjwvYnBtbmRpOkJQTU5TaGFwZT48YnBtbmRpOkJQTU5TaGFwZSBicG1uRWxlbWVu
dD1cIlNlcnZpY2VUYXNrXzEzeXM4YzVcIiBpZD1cIlNlcnZpY2VUYXNrXzEzeXM4YzVfZGlcIj48
b21nZGM6Qm91bmRzIGhlaWdodD1cIjgwXCIgd2lkdGg9XCIxMDBcIiB4PVwiMzQwXCIgeT1cIjI1
XCIvPjwvYnBtbmRpOkJQTU5TaGFwZT48YnBtbmRpOkJQTU5TaGFwZSBicG1uRWxlbWVudD1cIklu
Y2x1c2l2ZUdhdGV3YXlfMXJ3cjh1alwiIGlkPVwiSW5jbHVzaXZlR2F0ZXdheV8xcndyOHVqX2Rp
XCI+PG9tZ2RjOkJvdW5kcyBoZWlnaHQ9XCI1MFwiIHdpZHRoPVwiNTBcIiB4PVwiMjE3XCIgeT1c
IjIxNFwiLz48YnBtbmRpOkJQTU5MYWJlbD48b21nZGM6Qm91bmRzIGhlaWdodD1cIjEzXCIgd2lk
dGg9XCIwXCIgeD1cIjI0MlwiIHk9XCIyNjdcIi8+PC9icG1uZGk6QlBNTkxhYmVsPjwvYnBtbmRp
OkJQTU5TaGFwZT48YnBtbmRpOkJQTU5FZGdlIGJwbW5FbGVtZW50PVwiU2VxdWVuY2VGbG93XzBp
Y252ZHpcIiBpZD1cIlNlcXVlbmNlRmxvd18waWNudmR6X2RpXCI+PG9tZ2RpOndheXBvaW50IHg9
XCIxNTRcIiB4c2k6dHlwZT1cIm9tZ2RjOlBvaW50XCIgeT1cIjIyMVwiLz48b21nZGk6d2F5cG9p
bnQgeD1cIjE4NlwiIHhzaTp0eXBlPVwib21nZGM6UG9pbnRcIiB5PVwiMjIxXCIvPjxvbWdkaTp3
YXlwb2ludCB4PVwiMTg2XCIgeHNpOnR5cGU9XCJvbWdkYzpQb2ludFwiIHk9XCIyMzlcIi8+PG9t
Z2RpOndheXBvaW50IHg9XCIyMTdcIiB4c2k6dHlwZT1cIm9tZ2RjOlBvaW50XCIgeT1cIjIzOVwi
Lz48YnBtbmRpOkJQTU5MYWJlbD48b21nZGM6Qm91bmRzIGhlaWdodD1cIjEzXCIgd2lkdGg9XCIw
XCIgeD1cIjIwMVwiIHk9XCIyMjMuNVwiLz48L2JwbW5kaTpCUE1OTGFiZWw+PC9icG1uZGk6QlBN
TkVkZ2U+PGJwbW5kaTpCUE1ORWRnZSBicG1uRWxlbWVudD1cIlNlcXVlbmNlRmxvd18wcTlpYnht
XCIgaWQ9XCJTZXF1ZW5jZUZsb3dfMHE5aWJ4bV9kaVwiPjxvbWdkaTp3YXlwb2ludCB4PVwiMzQw
XCIgeHNpOnR5cGU9XCJvbWdkYzpQb2ludFwiIHk9XCI2NVwiLz48b21nZGk6d2F5cG9pbnQgeD1c
IjI0MlwiIHhzaTp0eXBlPVwib21nZGM6UG9pbnRcIiB5PVwiNjVcIi8+PG9tZ2RpOndheXBvaW50
IHg9XCIyNDJcIiB4c2k6dHlwZT1cIm9tZ2RjOlBvaW50XCIgeT1cIjIxNFwiLz48YnBtbmRpOkJQ
TU5MYWJlbD48b21nZGM6Qm91bmRzIGhlaWdodD1cIjEzXCIgd2lkdGg9XCI5MFwiIHg9XCIyNDZc
IiB5PVwiNDMuNVwiLz48L2JwbW5kaTpCUE1OTGFiZWw+PC9icG1uZGk6QlBNTkVkZ2U+PGJwbW5k
aTpCUE1ORWRnZSBicG1uRWxlbWVudD1cIlNlcXVlbmNlRmxvd18xa2FqdWx6XCIgaWQ9XCJTZXF1
ZW5jZUZsb3dfMWthanVsel9kaVwiPjxvbWdkaTp3YXlwb2ludCB4PVwiMjY3XCIgeHNpOnR5cGU9
XCJvbWdkYzpQb2ludFwiIHk9XCIyMzlcIi8+PG9tZ2RpOndheXBvaW50IHg9XCI0MjNcIiB4c2k6
dHlwZT1cIm9tZ2RjOlBvaW50XCIgeT1cIjIzOVwiLz48b21nZGk6d2F5cG9pbnQgeD1cIjQyM1wi
IHhzaTp0eXBlPVwib21nZGM6UG9pbnRcIiB5PVwiMTU4XCIvPjxvbWdkaTp3YXlwb2ludCB4PVwi
MzkwXCIgeHNpOnR5cGU9XCJvbWdkYzpQb2ludFwiIHk9XCIxNThcIi8+PG9tZ2RpOndheXBvaW50
IHg9XCIzOTBcIiB4c2k6dHlwZT1cIm9tZ2RjOlBvaW50XCIgeT1cIjEwNVwiLz48YnBtbmRpOkJQ
TU5MYWJlbD48b21nZGM6Qm91bmRzIGhlaWdodD1cIjEzXCIgd2lkdGg9XCI5MFwiIHg9XCIzOTNc
IiB5PVwiMTkyXCIvPjwvYnBtbmRpOkJQTU5MYWJlbD48L2JwbW5kaTpCUE1ORWRnZT48L2JwbW5k
aTpCUE1OUGxhbmU+PC9icG1uZGk6QlBNTkRpYWdyYW0+PC9kZWZpbml0aW9ucz4iLCAid29ya2Zs
b3dfaWQiOiAiYXZhbG9uX3JlZnJlc2giLCAidmVyc2lvbiI6IDM2fSwgIndvcmtmbG93X2lkIjog
NCwgImFjdGlvbnMiOiBbXSwgImxhc3RfbW9kaWZpZWRfdGltZSI6IDE1NDY1NzYwMDc0NjcsICJj
cmVhdG9yX2lkIjogInZhbEBraW5nYW5kdW5pb24uY29tIiwgImRlc2NyaXB0aW9uIjogIlB1bGxz
IGRhdGEgZnJvbSBsaW5rZWQgQXZhbG9uIHdvcmtzcGFjZS4gUmVxdWlyZXMgYW4gQXZhbG9uIFdv
cmtzcGFjZSB0byBiZSBsaW5rZWQgdG8gYW4gaW5jaWRlbnQuIFlvdSBjYW4gY3JlYXRlIGFuZCBs
aW5rIGFuIEF2YWxvbiB3b3Jrc3BhY2UgYXJ0aWZhY3QgYnkgZXhlY3V0aW5nIHRoZSBcIkF2YWxv
bjogQ3JlYXRlIFdvcmtzcGFjZVwiIGN1c3RvbSBtZW51IGNvbW1hbmQuIn1dLCAiYWN0aW9ucyI6
IFt7ImxvZ2ljX3R5cGUiOiAiYWxsIiwgIm5hbWUiOiAiQXZhbG9uOiBDcmVhdGUgV29ya3NwYWNl
IiwgInZpZXdfaXRlbXMiOiBbXSwgInR5cGUiOiAxLCAid29ya2Zsb3dzIjogW10sICJvYmplY3Rf
dHlwZSI6ICJpbmNpZGVudCIsICJ0aW1lb3V0X3NlY29uZHMiOiA4NjQwMCwgInV1aWQiOiAiMjYx
ZjZhZDItYmE2OC00Y2QxLWFkMjMtNmI1ZmI5Y2NjNjliIiwgImF1dG9tYXRpb25zIjogW10sICJl
eHBvcnRfa2V5IjogIkF2YWxvbjogQ3JlYXRlIFdvcmtzcGFjZSIsICJjb25kaXRpb25zIjogW3si
dHlwZSI6IG51bGwsICJldmFsdWF0aW9uX2lkIjogbnVsbCwgImZpZWxkX25hbWUiOiAiaW5jaWRl
bnQucHJvcGVydGllcy5hdmFsb25fd29ya3NwYWNlX2lkIiwgIm1ldGhvZCI6ICJub3RfaGFzX2Ff
dmFsdWUiLCAidmFsdWUiOiBudWxsfV0sICJpZCI6IDE4LCAibWVzc2FnZV9kZXN0aW5hdGlvbnMi
OiBbImF2YWxvbl9hY3Rpb25zIl19LCB7ImxvZ2ljX3R5cGUiOiAiYWxsIiwgIm5hbWUiOiAiQXZh
bG9uOiBQdWxsIE5vZGVzIiwgInZpZXdfaXRlbXMiOiBbXSwgInR5cGUiOiAxLCAid29ya2Zsb3dz
IjogW10sICJvYmplY3RfdHlwZSI6ICJpbmNpZGVudCIsICJ0aW1lb3V0X3NlY29uZHMiOiA4NjQw
MCwgInV1aWQiOiAiYWZjZjkxODMtODRhOS00YzhhLThhYWMtODUxMGFkMDI5NzAwIiwgImF1dG9t
YXRpb25zIjogW10sICJleHBvcnRfa2V5IjogIkF2YWxvbjogUHVsbCBOb2RlcyIsICJjb25kaXRp
b25zIjogW3sidHlwZSI6IG51bGwsICJldmFsdWF0aW9uX2lkIjogbnVsbCwgImZpZWxkX25hbWUi
OiAiaW5jaWRlbnQucHJvcGVydGllcy5hdmFsb25fd29ya3NwYWNlX2lkIiwgIm1ldGhvZCI6ICJo
YXNfYV92YWx1ZSIsICJ2YWx1ZSI6IG51bGx9XSwgImlkIjogMTksICJtZXNzYWdlX2Rlc3RpbmF0
aW9ucyI6IFsiYXZhbG9uX2FjdGlvbnMiXX0sIHsibG9naWNfdHlwZSI6ICJhbGwiLCAibmFtZSI6
ICJBdmFsb246IFB1bGwgTm9kZXMgRXZlcnkgNjAgbWluIiwgInZpZXdfaXRlbXMiOiBbXSwgInR5
cGUiOiAxLCAid29ya2Zsb3dzIjogWyJhdmFsb25fcmVmcmVzaCJdLCAib2JqZWN0X3R5cGUiOiAi
aW5jaWRlbnQiLCAidGltZW91dF9zZWNvbmRzIjogODY0MDAsICJ1dWlkIjogIjUyNDIwOWI5LWE2
OTYtNDgxZS1iOWNjLWRkZDAxOGJjNDE5OSIsICJhdXRvbWF0aW9ucyI6IFtdLCAiZXhwb3J0X2tl
eSI6ICJBdmFsb246IFB1bGwgTm9kZXMgRXZlcnkgNjAgbWluIiwgImNvbmRpdGlvbnMiOiBbXSwg
ImlkIjogMjEsICJtZXNzYWdlX2Rlc3RpbmF0aW9ucyI6IFtdfSwgeyJsb2dpY190eXBlIjogImFk
dmFuY2VkIiwgIm5hbWUiOiAiQXZhbG9uOiBQdXNoIEFydGlmYWN0IiwgInZpZXdfaXRlbXMiOiBb
XSwgInR5cGUiOiAxLCAid29ya2Zsb3dzIjogW10sICJvYmplY3RfdHlwZSI6ICJhcnRpZmFjdCIs
ICJ0aW1lb3V0X3NlY29uZHMiOiA4NjQwMCwgInV1aWQiOiAiZTkwODc4ZDgtYmM1ZC00OGI2LTgx
Y2QtNDE0ODQxNWU4YjUzIiwgImN1c3RvbV9jb25kaXRpb24iOiAiNCBBTkQgKDEgT1IgMikgQU5E
IDMiLCAiYXV0b21hdGlvbnMiOiBbXSwgImV4cG9ydF9rZXkiOiAiQXZhbG9uOiBQdXNoIEFydGlm
YWN0IiwgImNvbmRpdGlvbnMiOiBbeyJ0eXBlIjogbnVsbCwgImV2YWx1YXRpb25faWQiOiAyLCAi
ZmllbGRfbmFtZSI6ICJhcnRpZmFjdC50eXBlIiwgIm1ldGhvZCI6ICJlcXVhbHMiLCAidmFsdWUi
OiAiSVAgQWRkcmVzcyJ9LCB7InR5cGUiOiBudWxsLCAiZXZhbHVhdGlvbl9pZCI6IDEsICJmaWVs
ZF9uYW1lIjogImFydGlmYWN0LnR5cGUiLCAibWV0aG9kIjogImVxdWFscyIsICJ2YWx1ZSI6ICJE
TlMgTmFtZSJ9LCB7InR5cGUiOiBudWxsLCAiZXZhbHVhdGlvbl9pZCI6IDMsICJmaWVsZF9uYW1l
IjogImFydGlmYWN0LmRlc2NyaXB0aW9uIiwgIm1ldGhvZCI6ICJub3RfY29udGFpbnMiLCAidmFs
dWUiOiAiQXZhbG9uIn0sIHsidHlwZSI6IG51bGwsICJldmFsdWF0aW9uX2lkIjogNCwgImZpZWxk
X25hbWUiOiAiaW5jaWRlbnQucHJvcGVydGllcy5hdmFsb25fd29ya3NwYWNlX2lkIiwgIm1ldGhv
ZCI6ICJoYXNfYV92YWx1ZSIsICJ2YWx1ZSI6IG51bGx9XSwgImlkIjogMTcsICJtZXNzYWdlX2Rl
c3RpbmF0aW9ucyI6IFsiYXZhbG9uX2FjdGlvbnMiXX0sIHsibG9naWNfdHlwZSI6ICJhbGwiLCAi
bmFtZSI6ICJBdmFsb246IFB1c2ggQXJ0aWZhY3RzIiwgInZpZXdfaXRlbXMiOiBbXSwgInR5cGUi
OiAxLCAid29ya2Zsb3dzIjogW10sICJvYmplY3RfdHlwZSI6ICJpbmNpZGVudCIsICJ0aW1lb3V0
X3NlY29uZHMiOiA4NjQwMCwgInV1aWQiOiAiNGI1MWIwYzgtM2QyOS00YzFjLTk0MTMtNzEwOWM4
ZGQ1YzUyIiwgImF1dG9tYXRpb25zIjogW10sICJleHBvcnRfa2V5IjogIkF2YWxvbjogUHVzaCBB
cnRpZmFjdHMiLCAiY29uZGl0aW9ucyI6IFt7InR5cGUiOiBudWxsLCAiZXZhbHVhdGlvbl9pZCI6
IG51bGwsICJmaWVsZF9uYW1lIjogImluY2lkZW50LnByb3BlcnRpZXMuYXZhbG9uX3dvcmtzcGFj
ZV9pZCIsICJtZXRob2QiOiAiaGFzX2FfdmFsdWUiLCAidmFsdWUiOiBudWxsfV0sICJpZCI6IDIw
LCAibWVzc2FnZV9kZXN0aW5hdGlvbnMiOiBbImF2YWxvbl9hY3Rpb25zIl19XSwgImxheW91dHMi
OiBbXSwgImV4cG9ydF9mb3JtYXRfdmVyc2lvbiI6IDIsICJpZCI6IDI2LCAiaW5kdXN0cmllcyI6
IG51bGwsICJwaGFzZXMiOiBbXSwgImFjdGlvbl9vcmRlciI6IFtdLCAiZ2VvcyI6IG51bGwsICJz
ZXJ2ZXJfdmVyc2lvbiI6IHsibWFqb3IiOiAzMCwgInZlcnNpb24iOiAiMzAuMC4zNDc2IiwgImJ1
aWxkX251bWJlciI6IDM0NzYsICJtaW5vciI6IDB9LCAidGltZWZyYW1lcyI6IG51bGwsICJ3b3Jr
c3BhY2VzIjogW10sICJhdXRvbWF0aWNfdGFza3MiOiBbXSwgImZ1bmN0aW9ucyI6IFt7ImRpc3Bs
YXlfbmFtZSI6ICJhdmFsb25fcmVmcmVzaCIsICJ1dWlkIjogIjRiY2MyZGYxLWM2MGMtNGY2Mi04
NzlhLTAyNGNiMTUwYTE5ZSIsICJjcmVhdG9yIjogeyJkaXNwbGF5X25hbWUiOiAiVmFsIEthbnRj
aGV2IiwgInR5cGUiOiAidXNlciIsICJpZCI6IDEsICJuYW1lIjogInZhbEBraW5nYW5kdW5pb24u
Y29tIn0sICJ2aWV3X2l0ZW1zIjogW10sICJleHBvcnRfa2V5IjogImF2YWxvbl9yZWZyZXNoIiwg
Imxhc3RfbW9kaWZpZWRfYnkiOiB7ImRpc3BsYXlfbmFtZSI6ICJWYWwgS2FudGNoZXYiLCAidHlw
ZSI6ICJ1c2VyIiwgImlkIjogMSwgIm5hbWUiOiAidmFsQGtpbmdhbmR1bmlvbi5jb20ifSwgIm5h
bWUiOiAiYXZhbG9uX3JlZnJlc2giLCAidmVyc2lvbiI6IDMsICJ3b3JrZmxvd3MiOiBbeyJwcm9n
cmFtbWF0aWNfbmFtZSI6ICJhdmFsb25fcmVmcmVzaCIsICJvYmplY3RfdHlwZSI6ICJpbmNpZGVu
dCIsICJ1dWlkIjogbnVsbCwgImFjdGlvbnMiOiBbXSwgIm5hbWUiOiAiQXZhbG9uOiBSZWZyZXNo
IiwgIndvcmtmbG93X2lkIjogNCwgImRlc2NyaXB0aW9uIjogbnVsbH1dLCAibGFzdF9tb2RpZmll
ZF90aW1lIjogMTU0NjU2ODc1OTIwNywgImRlc3RpbmF0aW9uX2hhbmRsZSI6ICJhdmFsb25fYWN0
aW9ucyIsICJpZCI6IDIsICJkZXNjcmlwdGlvbiI6IHsiY29udGVudCI6ICJQdWxscyBkYXRhIGZy
b20gYSBsaW5rZWQgQXZhbG9uIHdvcmtzcGFjZS4gUmVxdWlyZXMgYW4gQXZhbG9uIFdvcmtzcGFj
ZSBhcnRpZmFjdCB0byBiZSBwcmVzZW50IGluIHRoZSBpbmNpZGVudC4gQXZhbG9uIFdvcmtzcGFj
ZSBhcnRpZmFjdCBjYW4gYmUgY3JlYXRlZCB3aXRoIHRoZSBcIkF2YWxvbjogQ3JlYXRlIFdvcmtz
cGFjZVwiIGN1c3RvbSBtZW51IGNvbW1hbmQuIiwgImZvcm1hdCI6ICJ0ZXh0In19XSwgIm5vdGlm
aWNhdGlvbnMiOiBudWxsLCAicmVndWxhdG9ycyI6IG51bGwsICJpbmNpZGVudF90eXBlcyI6IFt7
ImNyZWF0ZV9kYXRlIjogMTU0NjU3NjA0MjMyOSwgImRlc2NyaXB0aW9uIjogIkN1c3RvbWl6YXRp
b24gUGFja2FnZXMgKGludGVybmFsKSIsICJleHBvcnRfa2V5IjogIkN1c3RvbWl6YXRpb24gUGFj
a2FnZXMgKGludGVybmFsKSIsICJpZCI6IDAsICJuYW1lIjogIkN1c3RvbWl6YXRpb24gUGFja2Fn
ZXMgKGludGVybmFsKSIsICJ1cGRhdGVfZGF0ZSI6IDE1NDY1NzYwNDIzMjksICJ1dWlkIjogImJm
ZWVjMmQ0LTM3NzAtMTFlOC1hZDM5LTRhMDAwNDA0NGFhMCIsICJlbmFibGVkIjogZmFsc2UsICJz
eXN0ZW0iOiBmYWxzZSwgInBhcmVudF9pZCI6IG51bGwsICJoaWRkZW4iOiBmYWxzZX1dLCAic2Ny
aXB0cyI6IFtdLCAidHlwZXMiOiBbXSwgIm1lc3NhZ2VfZGVzdGluYXRpb25zIjogW3sidXVpZCI6
ICJjMzMyNTBmNC03ODExLTQ1YjUtODU4Yi1kNTk3ZDIyNjljODEiLCAiZXhwb3J0X2tleSI6ICJh
dmFsb25fYWN0aW9ucyIsICJuYW1lIjogImF2YWxvbl9hY3Rpb25zIiwgImRlc3RpbmF0aW9uX3R5
cGUiOiAwLCAicHJvZ3JhbW1hdGljX25hbWUiOiAiYXZhbG9uX2FjdGlvbnMiLCAiZXhwZWN0X2Fj
ayI6IHRydWUsICJ1c2VycyI6IFsidmFsQGtpbmdhbmR1bmlvbi5jb20iXX1dLCAiaW5jaWRlbnRf
YXJ0aWZhY3RfdHlwZXMiOiBbXSwgInJvbGVzIjogW10sICJmaWVsZHMiOiBbeyJvcGVyYXRpb25z
IjogW10sICJ0eXBlX2lkIjogMCwgIm9wZXJhdGlvbl9wZXJtcyI6IHt9LCAidGV4dCI6ICJBdmFs
b246IExhc3QgUHVsbCBUaW1lIiwgImJsYW5rX29wdGlvbiI6IGZhbHNlLCAicHJlZml4IjogInBy
b3BlcnRpZXMiLCAiY2hhbmdlYWJsZSI6IHRydWUsICJpZCI6IDgyLCAicmVhZF9vbmx5IjogZmFs
c2UsICJ1dWlkIjogIjU3Y2QyNzJiLWMwMTEtNDg3YS04YjAxLThhNzNiZjIzMGEzMCIsICJjaG9z
ZW4iOiBmYWxzZSwgImlucHV0X3R5cGUiOiAiZGF0ZXRpbWVwaWNrZXIiLCAidG9vbHRpcCI6ICJU
aW1lIG9mIHRoZSBsYXN0IHB1bGwgZnJvbSBBdmFsb24iLCAiaW50ZXJuYWwiOiBmYWxzZSwgInJp
Y2hfdGV4dCI6IGZhbHNlLCAidGVtcGxhdGVzIjogW10sICJleHBvcnRfa2V5IjogImluY2lkZW50
L2F2YWxvbl9sYXN0X3B1bGxfdGltZSIsICJoaWRlX25vdGlmaWNhdGlvbiI6IGZhbHNlLCAicGxh
Y2Vob2xkZXIiOiAiIiwgIm5hbWUiOiAiYXZhbG9uX2xhc3RfcHVsbF90aW1lIiwgImRlZmF1bHRf
Y2hvc2VuX2J5X3NlcnZlciI6IGZhbHNlLCAidmFsdWVzIjogW119LCB7Im9wZXJhdGlvbnMiOiBb
XSwgInR5cGVfaWQiOiAwLCAib3BlcmF0aW9uX3Blcm1zIjoge30sICJ0ZXh0IjogIkF2YWxvbjog
V29ya3NwYWNlIElEIiwgImJsYW5rX29wdGlvbiI6IGZhbHNlLCAicHJlZml4IjogInByb3BlcnRp
ZXMiLCAiY2hhbmdlYWJsZSI6IHRydWUsICJpZCI6IDgwLCAicmVhZF9vbmx5IjogZmFsc2UsICJ1
dWlkIjogIjMyZTU4MWZhLTJlNmQtNDk1NC04YjBlLWY1NjYzYzFmNTlmNCIsICJjaG9zZW4iOiBm
YWxzZSwgImlucHV0X3R5cGUiOiAibnVtYmVyIiwgInRvb2x0aXAiOiAiRW50ZXIgQXZhbG9uIFdv
cmtzcGFjZSBJRCB0byBsaW5rIGl0IHRvIHRoaXMgSW5jaWRlbnQgICIsICJpbnRlcm5hbCI6IGZh
bHNlLCAicmljaF90ZXh0IjogZmFsc2UsICJ0ZW1wbGF0ZXMiOiBbXSwgImV4cG9ydF9rZXkiOiAi
aW5jaWRlbnQvYXZhbG9uX3dvcmtzcGFjZV9pZCIsICJoaWRlX25vdGlmaWNhdGlvbiI6IGZhbHNl
LCAicGxhY2Vob2xkZXIiOiAiIiwgIm5hbWUiOiAiYXZhbG9uX3dvcmtzcGFjZV9pZCIsICJkZWZh
dWx0X2Nob3Nlbl9ieV9zZXJ2ZXIiOiBmYWxzZSwgInZhbHVlcyI6IFtdfSwgeyJvcGVyYXRpb25z
IjogW10sICJ0eXBlX2lkIjogMCwgIm9wZXJhdGlvbl9wZXJtcyI6IHt9LCAidGV4dCI6ICJBdmFs
b246IFB1bGwgTm9kZXMgQXV0b21hdGljYWxseSIsICJibGFua19vcHRpb24iOiBmYWxzZSwgInBy
ZWZpeCI6ICJwcm9wZXJ0aWVzIiwgImNoYW5nZWFibGUiOiB0cnVlLCAiaWQiOiA4MSwgInJlYWRf
b25seSI6IGZhbHNlLCAidXVpZCI6ICIwNmEyYWI4Zi03ZDY5LTQ5NmItYjFmYS0wZjY3OWE1NjMz
YTYiLCAiY2hvc2VuIjogZmFsc2UsICJpbnB1dF90eXBlIjogImJvb2xlYW4iLCAidG9vbHRpcCI6
ICJTZXQgdG8gWWVzIHRvIGF1dG9tYXRpY2FsbHkgcHVsbCBub2RlcyBmcm9tIEF2YWxvbiBldmVy
eSA2MCBtaW51dGVzIiwgImludGVybmFsIjogZmFsc2UsICJyaWNoX3RleHQiOiBmYWxzZSwgInRl
bXBsYXRlcyI6IFtdLCAiZXhwb3J0X2tleSI6ICJpbmNpZGVudC9hdmFsb25fcHVsbF9ub2Rlc19h
dXRvbWF0aWNhbGx5IiwgImhpZGVfbm90aWZpY2F0aW9uIjogZmFsc2UsICJwbGFjZWhvbGRlciI6
ICIiLCAibmFtZSI6ICJhdmFsb25fcHVsbF9ub2Rlc19hdXRvbWF0aWNhbGx5IiwgImRlZmF1bHRf
Y2hvc2VuX2J5X3NlcnZlciI6IGZhbHNlLCAidmFsdWVzIjogW119XSwgIm92ZXJyaWRlcyI6IFtd
LCAiZXhwb3J0X2RhdGUiOiAxNTQ2NTc2MDU0NzU3fQ==
"""
    )