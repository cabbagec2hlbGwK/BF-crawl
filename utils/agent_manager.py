import uuid
import json
import docker
from flask import Flask
from flask import request
#import requests
#import kubernetes

class Agent:
    def __init__(self, endpoint, agentMastertPort, applicationPort, user, password) -> None:
        self.name = ""
        self.masterEndpoint = endpoint
        self.masterAgentPort = agentMastertPort
        self.applicationPort = applicationPort
        self.user = user
        self.passowrd = password
        self.tasks = []
        self.createAgent()

    def createAgent(self):
        client = docker.from_env()
        agentId = str(uuid.uuid4())
        self.agentId = agentId
        try:
            # Create the container
            container = client.containers.run(
                    image="agent5", 
                    detach=True,  
                    name=f"app-{agentId}",
                    network="myapp", 
                    environment={
                        "APPLICATION_MASTER": f"{self.masterEndpoint}:{self.applicationPort}",
                        "AGENT_MASTER":f"{self.masterEndpoint}:{self.masterAgentPort}",
                        "AGENT_ID":agentId,
                        "ELASTIC_HOST":"",
                        "ELASTIC_API":"",
                        "BREACHFORM_USER":self.user,
                        "BREACHFORM_PASSWORD":self.passowrd
                        }, 
                    )
            print(f"Container {container.name} created and running.")
            self.container = container
        except docker.errors.APIError as e:
            print(f"Error: {e.explanation}")

    def destroy(self):
        self.container.remove(force=True)
    def restart(self):
        self.container.restart(timeout=3)
    def addTask(self, task):
        self.tasks.append(task)

    def getStatus(self):
        return self.container.status
    def getId(self):
        return self.agentId


class ManageAgent:

    def __init__(self, creds, endpoint, agentMastertPort, applicationPort) -> None:
        self.avaliableAgents = {}
        self.healthyAgents = {}
        for cred in creds:
            user, password = next(iter(cred.items()))
            agent = Agent(endpoint=endpoint, agentMastertPort=agentMastertPort, applicationPort=applicationPort, user=user, password=password)
            self.avaliableAgents[agent.getId()]=agent
            self.healthyAgents[agent.getId()]=None

    def getAgent(self, agentId):
        return self.avaliableAgents[agentId]
    def getHealthyAgents(self):
        return self.healthyAgents.keys()
    def setUnhealthy(self, agentId, restart=False):
        try:
            agent = self.avaliableAgents[agentId]
            self.healthyAgents[agentId]=0
            if restart:
                agent.restart()
            else:
                agent.destroy()
            return True
        except Exception as e:
            print(e)
            return False
    def setHealthy(self, agentId):
        try:
            _ = self.avaliableAgents[agentId]
            self.healthyAgents[agentId]=1
            return True
        except Exception as e:
            print(e)
            return False


def main():
    #def __init__(self, creds:dict, endpoint, agentMastertPort, applicationPort) -> None:
    app = Flask("AGENT_MANAGER")
    creds = [{"spiderman1948":"sdfnjsdkFjn#@s0"}]
    endpoint = "http://agent1"
    agentMasterPort = "5050"
    applicationPort = "8000"
    agentHandeler = ManageAgent(creds=creds, endpoint=endpoint, agentMastertPort=agentMasterPort, applicationPort=applicationPort)
    
    @app.route("/health", methods=["POST"])
    def health():
        try:
            res = json.loads(request.data.decode())
            agentId = res.get("agentId")
            state = res.get("state")
            message = res.get("message")
            print(message, state, agentId)
            if state != "HEALTHY":
                agentHandeler.setUnhealthy(agentId)
            if state == "FAILED_LOGIN":
                agentHandeler.setUnhealthy(agentId, restart=True)
            else:
                agentHandeler.setHealthy(agentId)
            return {"status":"SUCCESSFULL"}
        except Exception as e:
            return {"status":"ERROR"}

    app.run(port=5050, host="agent1")

if __name__=="__main__":
    main()
