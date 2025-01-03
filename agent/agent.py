import json
import time
import requests
import os
import stem.process
from utils.browser import Browser
from utils.indexer import ingestData


def print_bootstrap_lines(line):
    print(f"TOR: {line}")

def tor_proxy():
    tor_process = stem.process.launch_tor_with_config(
        config={
            "SocksPort": "9050",
            # "ExitNodes": "{US}",
        },
        init_msg_handler=print_bootstrap_lines,
    )
    return tor_process


def tor_req():
    proxy_ip = "localhost"  # Tor proxy IP address
    proxy_port = 9050

    # Create a session and set the proxy
    session = requests.session()
    session.proxies.update(
        {
            "http": f"socks5h://{proxy_ip}:{proxy_port}",
            "https": f"socks5h://{proxy_ip}:{proxy_port}",
        }
    )
    return session

def getTask(agent, agentId, taskId="NULL", prevTaskState="NULL"):
    res = requests.get(f"{agent}/task", json={"agentId":agentId,"previousTask":{"taskId":taskId,"state":prevTaskState}})
    res = res.json()
    return res

def running(brow, application, agent,agentId):
    run = True
    prevTaskId = "NULL"
    prevTaskState = "NULL"
    try:
        while run:
            time.sleep(5)
            task = getTask(agent, agentId, prevTaskId, prevTaskState)
            if task.get("taskId") == "NULL":
                prevTaskId = "NULL"
                prevTaskState = "NULL"
                continue
            prevTaskId = task.get("taskId")
            prevTaskState="NULL"
            if "Forum" in task.get("type"):
                tot =0
                urls = brow.getForumLinks(forum = task.get("type"), url = task.get("url"), maxPages = 3)
                healthUpdate(agent, agentId, "HEALTHY", f"{len(urls)}")
                for link in urls:
                    tot += 1
                    healthUpdate(agent, agentId, "HEALTHY", f"DONE---------{tot}")
                    data = brow.getPageSource(link)
                    ingestData(str(data), link, task.get("type"))
                prevTaskState="done"
            else:
                data = brow.getPageSource(task.get("url"))
                healthUpdate(agent, agentId, "HEALTHY", f"DONE---------")
                ingestData(str(data), task.get("url"), task.get("type"))
                prevTaskState="done"





    except Exception as e:
        healthUpdate(agent, agentId, "RESTART", f"EXCEPTION:{e}")
        task = getTask(agent, agentId, prevTaskId, "critFail")

def healthUpdate(endpoint, agentId, state, message):
    requests.post(f"{endpoint}/health", json= {"state":state, "agentId":agentId, "message":message})
    print("successfull health update")
def main():
    applicationMaster = os.getenv("APPLICATION_MASTER","NULL")
    agentMaster = os.getenv("AGENT_MASTER","NULL")
    agentId = os.getenv("AGENT_ID","NULL")
    user = os.getenv("BREACHFORM_USER","NULL")
    password = os.getenv("BREACHFORM_PASSWORD","NULL")
    tor = tor_proxy()
    print("STARTING AGENT..")
    brow = Browser()
    try:
        success = brow.breachFormLogin(user,password,f"{applicationMaster}/capta")
        brow.browser.save_screenshot("lang.png")
        if success:
            healthUpdate(agentMaster, agentId, "HEALTHY", "LOGIN_SUCCESS")
        else:
            healthUpdate(agentMaster, agentId, "FAILED_LOGIN", "LOGIN_FAILED")
            exit(1)
        time.sleep(5)
        data = brow.browser.page_source
        running(brow=brow, application=applicationMaster, agent=agentMaster, agentId=agentId)
    except Exception as e:
        print(e)
        healthUpdate(agentMaster, agentId, "OFFLINE", f"EXCEPTION:{e}")
        brow.browser.quit()
        time.sleep(30)
        exit(100)


if __name__=="__main__":
    main()
