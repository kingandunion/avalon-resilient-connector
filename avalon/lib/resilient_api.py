from enum import IntEnum

# IBM Resilient Artifact Types 
# see: https://10.1.0.151/docs/rest-api/ui/index.html#!/TypeREST/resource_TypeREST_getType_GET
class ArtifactType(IntEnum):
    """IBM Resilient Artifact Types 
    """
    ip_address = 1
    dns_name = 2,
    url = 3,
    rfc_822_email_message_file = 4,
    email_subject = 5,
    email_body = 6,
    email_attachment = 7,
    email_attachment_name = 8,
    email_sender = 9,
    malware_sample = 12,
    malware_md5_hash = 13,
    malware_sha_1_hash = 14,
    log_file = 15,
    other_file = 16,
    email_sender_name = 19,
    email_recipient = 20,
    malware_sample_fuzzy_hash = 22,
    user_account = 23,
    registry_key = 24,
    system_name = 25,
    process_name = 26,
    port = 27,
    service = 28,
    string = 29,
    mutex = 30,
    file_name = 31,
    password = 32,
    http_request_header = 34,
    http_response_header = 35,
    x509_certificate_file = 36,
    file_path = 37,
    malware_sha_256_hash = 38,
    mac_address = 39,
    url_referer = 40,
    user_agent = 41,
    uri_path = 42,
    threat_cve_id = 43,
    network_cidr_range = 44,
    malware_family_variant = 45

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
        if artifact_type and artifact_type == "avalon_workspace":
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
