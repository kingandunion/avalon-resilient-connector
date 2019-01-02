from enum import IntEnum

# IBM Resilient Artifact Types 
# see: https://10.1.0.151/docs/rest-api/ui/index.html#!/TypeREST/resource_TypeREST_getType_GET
class ArtifactType(IntEnum):
    """IBM Resilient Artifact Types 
    """
    ip_address = 1
    dns_name = 2

def validate_fields(fieldList, kwargs):
    """
    ensure required fields are present. Throw ValueError if not
    :param fieldList:
    :param kwargs:
    :return: no return
    """
    for field in fieldList:
        if field not in kwargs or kwargs.get(field) == "":
            raise ValueError("Required field is missing or empty: " + field)

# see: https://10.1.0.151/docs/rest-api/json_IncidentArtifactDTO.html
def incident_add_workspace_artifact(rest_client, incident_id, title, description, workspace_id, workspace_url):
    new_artifact = {
        "type": { "name": "String" },
        "value": title,
        "description": {
            "format" : "text", 
            "content" : description
        },
        # user should not be able to update this artifact
        "perms": {
            "read" : True,
            "write" : False,
            "delete" : True
        },                    
        # properties are not visible inthe UI but are available via the Rest API
        "properties": [
            {
                "name": "type",
                "value": "avalon_workspace"
            },
            {
                "name": "id",
                "value": workspace_id
            },
            { 
                "name": "url",
                "value": workspace_url
            }
        ]
    }

    new_artifact_uri = "/incidents/{}/artifacts".format(incident_id)
    rest_client.post(new_artifact_uri, new_artifact)

def incident_set_avalon_workspace_id(rest_client, incident_id, avalon_workspace_id):
    patch_data =  {
        "changes": [
            {
            "field": {
                "name": "avalon_workspace_id"
            },
            "old_value": {},
            "new_value": avalon_workspace_id
            }
        ],
        "version": 0
    }        
 
    incident_patch_uri = "/incidents/{}".format(incident_id)
    resp = rest_client.patch(incident_patch_uri, patch_data)
    return resp


def incident_add_artifact(rest_client, incident_id, art_type, art_value, art_desc):
    new_artifact = {
        "type": art_type,
        "value": art_value,
        "description": {
            "format" : "text", 
            "content" : art_desc
        }
    }

    new_artifact_uri = "/incidents/{}/artifacts".format(incident_id)
    rest_client.post(new_artifact_uri, new_artifact)


def incident_get_artifacts(rest_client, incident_id):
    # get all artifacts for this incident
    artifact_uri = "/incidents/{}/artifacts".format(incident_id)
    artifacts = rest_client.get(artifact_uri)
    return artifacts


def incident_get_workspace_artifact(rest_client, incident_id, artifacts=None):
    # get all artifacts for this incident
    if not artifacts:
        artifacts = incident_get_artifacts(rest_client, incident_id)

    # Tthe workspace artifact should have a property "type" set to "avalon_workspace" 
    for artifact in artifacts:
        artifact_type = get_artifact_property(artifact, "type")
        if not artifact_type is None and artifact_type == "avalon_workspace":
            return artifact

    return None


def get_artifact_property(artifact, name):
    properties = artifact["properties"]
    if properties is None:
        return None

    for prop in properties:
        if prop["name"] == name:
            return prop["value"]

    return None
