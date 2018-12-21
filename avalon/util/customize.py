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
                    "message_destinations": [u'avalon_connector'], 
                    "functions": [], 
                    "phases": [], 
                    "automatic_tasks": [], 
                    "scripts": [], 
                    "workflows": [],
                    "actions": [u'Avalon: Create Workspace']
                    }
    return reload_params


def customization_data(client=None):
    """Produce any customization definitions (types, fields, message destinations, etc)
       that should be installed by `resilient-circuits customize`
    """

    # This import data contains:


    yield ImportDefinition(u"""
eyJpZCI6IDIsICJmaWVsZHMiOiBbeyJjaG9zZW4iOiBmYWxzZSwgImludGVybmFsIjogZmFsc2Us
ICJ1dWlkIjogImMzZjBlM2VkLTIxZTEtNGQ1My1hZmZiLWZlNWNhMzMwOGNjYSIsICJvcGVyYXRp
b25zIjogW10sICJ2YWx1ZXMiOiBbXSwgImNoYW5nZWFibGUiOiB0cnVlLCAiaWQiOiAzOCwgIm5h
bWUiOiAiaW5jX3RyYWluaW5nIiwgInRleHQiOiAiU2ltdWxhdGlvbiIsICJwcmVmaXgiOiBudWxs
LCAidHlwZV9pZCI6IDAsICJ0b29sdGlwIjogIldoZXRoZXIgdGhlIGluY2lkZW50IGlzIGEgc2lt
dWxhdGlvbiBvciBhIHJlZ3VsYXIgaW5jaWRlbnQuICBUaGlzIGZpZWxkIGlzIHJlYWQtb25seS4i
LCAiaW5wdXRfdHlwZSI6ICJib29sZWFuIiwgImhpZGVfbm90aWZpY2F0aW9uIjogZmFsc2UsICJk
ZWZhdWx0X2Nob3Nlbl9ieV9zZXJ2ZXIiOiBmYWxzZSwgImJsYW5rX29wdGlvbiI6IGZhbHNlLCAi
b3BlcmF0aW9uX3Blcm1zIjoge30sICJyZWFkX29ubHkiOiB0cnVlLCAicmljaF90ZXh0IjogZmFs
c2UsICJleHBvcnRfa2V5IjogImluY2lkZW50L2luY190cmFpbmluZyIsICJ0ZW1wbGF0ZXMiOiBb
XX1dLCAicGhhc2VzIjogW10sICJvdmVycmlkZXMiOiBbXSwgImFjdGlvbnMiOiBbXSwgImxheW91
dHMiOiBbXSwgIm5vdGlmaWNhdGlvbnMiOiBudWxsLCAidGltZWZyYW1lcyI6IG51bGwsICJpbmR1
c3RyaWVzIjogbnVsbCwgInJlZ3VsYXRvcnMiOiBudWxsLCAiZ2VvcyI6IG51bGwsICJmdW5jdGlv
bnMiOiBbXSwgInNlcnZlcl92ZXJzaW9uIjogeyJtYWpvciI6IDMwLCAibWlub3IiOiAwLCAiYnVp
bGRfbnVtYmVyIjogMzQ3NiwgInZlcnNpb24iOiAiMzAuMC4zNDc2In0sICJleHBvcnRfZm9ybWF0
X3ZlcnNpb24iOiAyLCAiZXhwb3J0X2RhdGUiOiAxNTQ1MzQzNDQ3NTM4LCAiaW5jaWRlbnRfdHlw
ZXMiOiBbeyJ1cGRhdGVfZGF0ZSI6IDE1NDUzNDM4MTQ1NzMsICJjcmVhdGVfZGF0ZSI6IDE1NDUz
NDM4MTQ1NzMsICJ1dWlkIjogImJmZWVjMmQ0LTM3NzAtMTFlOC1hZDM5LTRhMDAwNDA0NGFhMCIs
ICJkZXNjcmlwdGlvbiI6ICJDdXN0b21pemF0aW9uIFBhY2thZ2VzIChpbnRlcm5hbCkiLCAiZXhw
b3J0X2tleSI6ICJDdXN0b21pemF0aW9uIFBhY2thZ2VzIChpbnRlcm5hbCkiLCAibmFtZSI6ICJD
dXN0b21pemF0aW9uIFBhY2thZ2VzIChpbnRlcm5hbCkiLCAiZW5hYmxlZCI6IGZhbHNlLCAic3lz
dGVtIjogZmFsc2UsICJwYXJlbnRfaWQiOiBudWxsLCAiaGlkZGVuIjogZmFsc2UsICJpZCI6IDB9
XSwgImF1dG9tYXRpY190YXNrcyI6IFtdLCAibWVzc2FnZV9kZXN0aW5hdGlvbnMiOiBbXSwgInRh
c2tfb3JkZXIiOiBbXSwgImFjdGlvbl9vcmRlciI6IFtdLCAidHlwZXMiOiBbXSwgInNjcmlwdHMi
OiBbXSwgImluY2lkZW50X2FydGlmYWN0X3R5cGVzIjogW10sICJ3b3JrZmxvd3MiOiBbXSwgInJv
bGVzIjogW10sICJ3b3Jrc3BhY2VzIjogW119
"""
    )