"""
Project: Xray Fragment Tester - Core Logic
Author: github.com/sasanxxx
"""
import json
import uuid

def generate_config(base_config: dict, params: dict) -> dict:
    config = json.loads(json.dumps(base_config))
    
    config["outbounds"][0]["settings"]["fragment"]["length"] = params["fragment_length"]
    config["outbounds"][0]["settings"]["fragment"]["interval"] = params["fragment_interval"]
    config["dns"]["servers"] = [params["dns_server_url"]]
    
    for outbound in config.get("outbounds", []):
        if outbound.get("protocol") == "vless":
            outbound["settings"]["vnext"][0]["address"] = params["server_name"]
            outbound["streamSettings"]["tlsSettings"]["serverName"] = params["server_name"]
            outbound["settings"]["vnext"][0]["users"][0]["id"] = str(uuid.uuid4())
            break
            
    return config