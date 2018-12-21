def validateFields(fieldList, kwargs):
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
def incident_add_workspace_artifact(rest_client, incident_id, workspace_id, workspace_title, workspace_url):
    new_artifact = {
        "type": { "name": "String" },
        "value": workspace_title,
        "description": {
            "format" : "text", 
            "content" : "Avalon Workspace Address: {}".format(workspace_url)
        },
        "properties": [
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