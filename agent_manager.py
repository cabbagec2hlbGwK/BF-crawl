from sys import set_coroutine_origin_tracking_depth
import uuid
import time
import json
import docker
import os
from flask import Flask
from flask import request
from crawlerScope import scope
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
        self.agentHost = os.getenv("CONTAINER_NAME")
        self.elasticApi = os.getenv("ELASTIC_API")
        self.elasticHost = os.getenv("ELASTIC_HOST")
        self.indexName = os.getenv("ELASTIC_INDEX")
        self.networkName = os.getenv("NETWORK_NAME")
        self.createAgent()

    def createAgent(self):
        client = docker.from_env()
        agentId = str(uuid.uuid4())
        self.agentId = agentId
        try:
            # Create the container
            container = client.containers.run(
                    image="bf-agent", 
                    detach=True,  
                    name=f"app-{agentId}",
                    network=self.networkName, 
                    environment={
                        "APPLICATION_MASTER": f"{self.masterEndpoint}:{self.applicationPort}",
                        "AGENT_MASTER": f"{self.masterEndpoint}:{self.masterAgentPort}",
                        "AGENT_ID": f"{agentId}",
                        "ELASTIC_HOST": str(self.elasticHost),
                        "ELASTIC_API": str(self.elasticApi),
                        "INDEX_NAME": str(self.indexName),
                        "BREACHFORM_USER":str(self.user),
                        "BREACHFORM_PASSWORD": str(self.passowrd)
                        }, 
                    )
            print(f"Container {container.name} created and running.")
            self.container = container
        except docker.errors.APIError as e:
            print(f"Error: {e.explanation}")

    def destroy(self):
        self.container.remove(force=True)
    def restart(self):
        self.container.restart()
    def addTask(self, task):
        self.tasks.append(task)

    def getStatus(self):
        return self.container.status
    def getId(self):
        return self.agentId


class ManageAgent:

    def __init__(self, creds, endpoint, agentMastertPort, applicationPort, taskScope) -> None:
        self.avaliableAgents = {}
        self.healthyAgents = {}
        self.taskQueue = []
        self.tasks = {}
        self.initTask(taskScope)
        for cred in creds:
            user, password = next(iter(cred.items()))
            agent = Agent(endpoint=endpoint, agentMastertPort=agentMastertPort, applicationPort=applicationPort, user=user, password=password)
            self.avaliableAgents[agent.getId()]=agent
            self.healthyAgents[agent.getId()]=None

    def initTask(self, taskScope):
        for taskType, url in taskScope.items():
            self.tasks[uuid.uuid4().__str__()]= {"type": taskType, "url":url, "status":"idle"}
    def taskRemove(self, taskId):
        self.tasks.pop(taskId)
    def taskHandeler(self,session):
        agentId = session.get("agentId")
        prevTask = session.get("previousTask")
        if prevTask.get("taskId","NULL")!="NULL":
            if prevTask.get("state") == "done":
                self.updateTask(prevTask.get("taskId"), "done")
                self.taskRemove(prevTask.get("taskId"))
            if prevTask.get("state") == "critFail":
                self.updateTask(prevTask.get("taskId"), "idle")
                return ""
            else:
                if prevTask.get("taskId") in self.tasks:
                    self.updateTask(prevTask.get("taskId"), "idle")
                else:
                    pass
        newTask = self.getTask()
        if newTask == "NULL":
            return {"taskId":"NULL"}
        self.updateTask(newTask, "waiting")
        return {"taskId":newTask, "type":self.tasks[newTask]["type"], "url":self.tasks[newTask]["url"]}


    def updateTask(self, taskId, status):
        self.tasks[taskId]["status"]=status
        return True
    def getTask(self):
        idleTask = "NULL"
        for taskId, task in self.tasks.items():
            if task.get("status") == "idle":
                idleTask = taskId
                break
        return idleTask
            
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
    creds = [{"spiderman1948":"sdfnjsdkFjn#@s0"},{"falcondick":"FuckTrump@123"},{"rusianlan22":"sdlfsjldflF@121"}]
    agentHost = os.getenv("CONTAINER_NAME")
    endpoint = f"http://{agentHost}"
    agentMasterPort = "5050"
    applicationPort = "8000"
    agentHandeler = ManageAgent(creds=creds, endpoint=endpoint, agentMastertPort=agentMasterPort, applicationPort=applicationPort, taskScope=scope)
    
    @app.route("/task", methods=["GET"])
    def tasks():
        res = request.json
        print(res)
        return agentHandeler.taskHandeler(res)
    @app.route("/health", methods=["POST"])
    def health():
        try:
            res = json.loads(request.data.decode())
            agentId = res.get("agentId")
            state = res.get("state")
            message = res.get("message")
            print(message, state, agentId)
            if state == "FAILED_LOGIN" or state=="RESTART":
                time.sleep(1)
                agentHandeler.setUnhealthy(agentId, restart=True)
                return {"status":"SUCCESSFULL"}
            if state != "HEALTHY":
                agentHandeler.setUnhealthy(agentId)
                return {"status":"SUCCESSFULL"}
            else:
                agentHandeler.setHealthy(agentId)
                return {"status":"SUCCESSFULL"}
        except Exception as e:
            return {"status":"ERROR"}

    app.run(port=5050, host=agentHost)

if __name__=="__main__":
    main()
