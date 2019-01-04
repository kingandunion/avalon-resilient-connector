from avalon.lib.errors import IntegrationError, WorkspaceLinkError
from avalon.lib.avalon_api import Avalon
from avalon.lib.resilient_api import Resilient, ArtifactType

# maps Avalon Node type to IBM Resilient Artifact type
# only the types that directly correspond to one another are mapped
node_to_artifact_type = dict(
    ip = ArtifactType.ip_address,
    domain = ArtifactType.dns_name,
    url = ArtifactType.url,
)

# maps IBM Resilient Artifact type to Avalon Node type
# the reverse map of node_to_artifact_type above
artifact_to_node_type = dict(reversed(item) for item in node_to_artifact_type.items())

class Actions:
    def __init__(self, avalon_base_url, avalon_api_token, resilient_rest_client, logger):
        self.av = Avalon(avalon_base_url, avalon_api_token, logger)
        self.res = Resilient(resilient_rest_client)
        self.log = logger

    def reload(self, avalon_base_url, avalon_api_token):
        self.av.reload(avalon_base_url, avalon_api_token)

    # Creates an Avalon Workspace and links it with a Resilient Incident 
    def create_avalon_workspace(self, incident, who):
        try:
            # create Avalon workspace
            self._create_avalon_workspace(incident, who)
            return "Avalon workspace created successfully."
        except WorkspaceLinkError:
            return "Avalon workspace already exists for this incident."
        except Exception as err:
            # TODO: Find out how we can return errors from custom action handlers    
            # see: https://10.1.0.151/docs/rest-api/json_AcknowledgementDTO.html
            
            # return json.dumps({ 
            #     "message_type": { "id": 1, "name": "error" },
            #     "message": str(err), 
            #     "complete": True,
            #     "results" : { }
            # })

            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))


    # Pulls all nodes from an Avalon Workspace to Resilient Incident artifacts 
    # The Avalon Workspace must be linked to the Resilient Incident first
    def pull_avalon_nodes(self, incident):
        try:
            incident_id = incident["id"]
            artifacts = self.res.incident_get_artifacts(incident_id)

            # get workspace ID
            workspace_id = incident["properties"].get("avalon_workspace_id", None)
            if not workspace_id:
                raise Exception("Please create Avalon workspace for this incident first.") 

            # Call to get workspace / graph object. We need the graph UUID
            workspace_uuid = self._get_avalon_workspace_uuid(workspace_id)

            # Get all avalon nodes
            nodes = self._get_all_avalon_nodes(workspace_id, workspace_uuid)
            if nodes is None:
                return "Avalon workspace does not contains any nodes."

            # import the nodes into the IBM resilient incident
            self._create_resilient_artifacts(incident_id, artifacts, nodes)

            return "Successfully pulled all nodes from Avalon."
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))

    # Pushes all artifacts from a Resilient Incident to Avalon Workspace nodes 
    # The Avalon Workspace must be linked to the Resilient Incident first
    def push_resilient_artifacts(self, incident):
        try:
            incident_id = incident["id"]
            artifacts = self.res.incident_get_artifacts(incident_id)

            # get workspace ID
            workspace_id = incident["properties"].get("avalon_workspace_id", None)
            if not workspace_id:
                raise Exception("Please create Avalon workspace for this incident first.") 

            # Call to get workspace / graph object. We need the graph UUID
            workspace_uuid = self._get_avalon_workspace_uuid(workspace_id)

            # Get all avalon nodes
            nodes = self._get_all_avalon_nodes(workspace_id, workspace_uuid)

            # Push all artifacts
            total_success = True            
            for artifact in artifacts:
                # ignore the special Avalon Workspace artifact
                artifact_type = Resilient.get_artifact_property(artifact, "type")
                if artifact_type and artifact_type == "avalon_workspace":
                    continue

                # add only if node does not exist 
                if not self._find_node_for_artifact(nodes, artifact):
                   success = self._create_avalon_node(artifact, workspace_id)
                   total_success = total_success and success 

            if not total_success:
                return "Some artifacts could not be pushed to Avalon."
    
            return "Successfully pushed all artifacts to Avalon."
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))


    # Pushes one artifact from a Resilient Incident to an Avalon Workspace node 
    # The Avalon Workspace must be linked to the Resilient Incident first
    def push_one_resilient_artifact(self, incident, artifact):
        try:
            # get workspace ID
            workspace_id = incident["properties"].get("avalon_workspace_id", None)
            if not workspace_id:
                raise Exception("Please create Avalon workspace for this incident first.") 

            # Call to get workspace / graph object. We need the graph UUID
            workspace_uuid = self._get_avalon_workspace_uuid(workspace_id)

            # Get all avalon nodes
            nodes = self._get_all_avalon_nodes(workspace_id, workspace_uuid)
            
            if self._find_node_for_artifact(nodes, artifact):
                raise Exception("Could not add Avalon node. A node with value {} already exists.".format(artifact["value"]))

            if not self._create_avalon_node(artifact, workspace_id):
                raise IntegrationError("Unsupported artifact.")
    
            return "{} added to Avalon.".format(artifact["value"])
        except Exception as err:
            # NOTE: This will still mark the action as complete in IBM Resilient
            return "Error: {}".format(str(err))

    @staticmethod    
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

    # creates an Avalon workspace / graph and links it to a Resilient incident
    def _create_avalon_workspace(self, incident, who):
        # check whether Avalon workspace has been created for this incident already
        if incident["properties"]["avalon_workspace_id"]:
            raise WorkspaceLinkError("Already linked to Avalon Workspace ID: {}.".format(incident["avalon_workspace_id"]))   

        workspace_title = "{} (IBM Resilient)".format(incident["name"])
        workspace_summary = "Created from IBM Resilient by {}. IBM Resilient Incident ID: {}".format(who, incident["id"])
        
        data = {
            "Title": workspace_title, 
            "Summary": workspace_summary, 
            "TLP": "r", 
            "ShareWithMyOrganization": False
        }

        resp = self.av.workspace_create(data)
        (error, msg) = Avalon.check_error(resp)
        if error:
            raise IntegrationError(msg)

        # workspace data looks like: {"data": {"path": "https://example.com...aces/22/ "}}
        result = resp.json()
        workspace_data = result["data"]
        workspace_url = workspace_data["path"].strip() 
        workspace_id = self.av.workspace_id_from_url(workspace_url)

        # Set the workspace id field
        self.res.incident_set_avalon_workspace_id(incident["id"], workspace_id)

        # Add a new artifact to the incident
        artifact_title = "Avalon Workspace"
        artifact_description = "Avalon workspace address: {}".format(workspace_url)
        self.res.incident_add_workspace_artifact(incident["id"], 
                                                artifact_title, artifact_description, 
                                                workspace_id, workspace_url)

    # creates Resilient artifacts from Avalon nodes 
    def _create_resilient_artifacts(self, incident_id, artifacts, nodes):
        # 1) match nodes to artifacts by type and value 
        # 2) add artifacts only for nodes that are new  
        for node in nodes:
            node_value = node[0]
            node_type = node[1]

            # check whether it is a supported artifact            
            artifact_type = node_to_artifact_type.get(node_type)
            if artifact_type is None:
                continue

            # check whether artifact with the same type and value already exists 
            artifact_value = node_value   
            matching_artifacts = [
                a for a in artifacts 
                if a["type"] == artifact_type and a["value"] == artifact_value
            ]

            if len(matching_artifacts) > 0:
                continue

            # add new artifact to incident
            artifact_description = "Created from Avalon workspace node."
            self.res.incident_add_artifact(incident_id, artifact_type, artifact_value, artifact_description)

    # creates an Avalon node from a Resilient artifact 
    def _create_avalon_node(self, artifact, workspace_id):
        if artifact["type"] not in artifact_to_node_type:
            return False    

        data = {
            "nodes": [ 
                { 
                    "term": artifact["value"],
                    "type": artifact_to_node_type.get(artifact["type"]) 
                } 
            ]
        }

        resp = self.av.workspace_add_node(workspace_id, data)
        (error, msg) = Avalon.check_error(resp)
        if error:
            raise IntegrationError(msg)

        return True


    # finds a node that is the same as an artifact
    def _find_node_for_artifact(self, nodes, artifact):
        if not nodes:
            return False

        for node in nodes:
            node_value = node[0]
            node_type = node[1]

            artifact_value = node_value                      

            artifact_type = node_to_artifact_type.get(node_type)
            if not artifact_type:
                continue

            if artifact["type"] == artifact_type and artifact["value"] == artifact_value:
                return True

        return False


    #  gets Avalon Workspace UUID
    def _get_avalon_workspace_uuid(self, workspace_id):
        resp = self.av.workspace_get(workspace_id)
        (error, msg) = Avalon.check_error(resp)
        if error:
            raise IntegrationError(msg)

        result = resp.json()

        # get UUID
        return result["data"]["attributes"]["UUID"]


    # gets all nodes of an Avalon Workspace 
    def _get_all_avalon_nodes(self, workspace_id, workspace_uuid):
        resp = self.av.workspace_export(workspace_id, workspace_uuid, "json")
        (error, msg) = Avalon.check_error(resp)
        if error:
            raise IntegrationError(msg)

        result = resp.json()
        nodes = result["data"]

        return nodes





