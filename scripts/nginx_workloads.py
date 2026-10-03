import subprocess
import logging 
import sys 

from datetime import datetime, timezone

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


nginx_workload = {
        "deployment": "nginx-deploy",
        "replicas": 6,
        "image": "nginx:1.29.0",
        "port": 80,
        "namespace": "nginx",
        "region": "us-east-1",
        "availability_zones": [
            "us-east-1a",
            "us-east-1b",
            "us-east-1c",
        ]
    }

curl_pod = {
        "pod": "curl",
        "image": "curlimages/curl:7.83.0",
        "region": "us-east-1",
        "namespace": "nginx",
    }

def nginx_deployment(workload, curl):

    describe_deployment = subprocess.run(
        ["kubectl", "describe", "deployment", workload["deployment"], "-n", workload["namespace"]],
        capture_output=True,
        text=True,
        check=True
    )
    
    nginx_pods = subprocess.run(
        ["kubectl", "get", "pods", "-n", workload["namespace"]],
        capture_output=True,
        text=True,
        check=True
    )

    describe_curl = subprocess.run(
        ["kubectl", "describe", "pod", curl["pod"], "-n", curl["namespace"]],
        capture_output=True,
        text=True,
        check=True
    )
    
    logger.info("Nginx Deployment Description: \n%s", describe_deployment.stdout)
    logger.info("Curl Pod Description: \n%s", describe_curl.stdout)
    logger.info("Nginx Pods: \n%s", nginx_pods.stdout)
    
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "nginx_deployment": describe_deployment.stdout,
        "curl_pod": describe_curl.stdout,
        "nginx_pods": nginx_pods.stdout
    }

try: 
    
    nginx_deployment(nginx_workload, curl_pod)

except subprocess.CalledProcessError as e:
    logger.exception("Error retrieving Nginx deployment details: %s", e.stderr)
    sys.exit(1)
    
except FileNotFoundError as e:
    logger.error("kubectl was not found. Check your installation and PATH. %s", str(e))
    sys.exit(1)
    
except Exception as e:
    logger.exception("An unexpected error occurred: %s", str(e))
    sys.exit(1)    
