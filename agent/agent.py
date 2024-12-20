import time
import requests
import os
import stem.process
from utils.browser import Browser


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

def healthUpdate(endpoint, agentId, state, message):
    requests.post(f"{endpoint}/health", json= {"state":state, "agentId":agentId, "message":message})
    print("successfull health update")
def main():
    applicationMaster = os.getenv("APPLICATION_MASTER","NULL")
    agentMaster = os.getenv("AGENT_MASTER","NULL")
    agentId = os.getenv("AGENT_ID","NULL")
    elasticHost = os.getenv("ELASTIC_HOST","NULL")
    elasticApi = os.getenv("ELASTIC_API","NULL")
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
        print(brow.browser.page_source)
    except Exception as e:
        print(e)
        brow.browser.quit()
        healthUpdate(agentMaster, agentId, "OFFLINE", f"EXCEPTION:{e}")
        exit(100)


if __name__=="__main__":
    main()
