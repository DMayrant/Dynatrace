import subprocess 
import logging 
import sys 

from datetime import datetime, timezone

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

dynatrace_config = {
        "kind": "Dynakube",
        "version": "v1beta6",
        "region": "us-east-1",
        "namespace": "dynatrace",
        
    }

def dynatrace_logs(config): 
    
    get_dynatrace = subprocess.run(
        ["kubectl", "get", "dynakubes", "-n", config["namespace"]],
        capture_output=True,
        text=True,
        check=True
    )
    logger.info("Dynakube Details \n%s", get_dynatrace.stdout)
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dynatrace": get_dynatrace.stdout
    }

try: 
    
    results = dynatrace_logs(dynatrace_config)
    sys.exit(0)

except subprocess.CalledProcessError as e:
    logger.exception("Error retrieving dynatrace details: %s", e.stderr)
    sys.exit(1)
    
except FileNotFoundError as e:
    logger.exception("kubectl was not found. Check your installation and PATH", str(e))

except Exception as e:
    logger.exception("An unexpected error occurred: %s", str(e))
    sys.exit(1)    
    
