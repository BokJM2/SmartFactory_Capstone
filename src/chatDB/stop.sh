ps -ef | grep chatdb-api.py | grep -v grep | awk '{print $2}' | xargs kill

