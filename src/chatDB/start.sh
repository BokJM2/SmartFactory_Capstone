ps -ef | grep chatdb-api.py | grep -v grep | awk '{print $2}' | xargs kill
python_path='/data/yuanzhaolin/LLM_garment_MES/env/bin/python'
nohup $python_path -u chatdb-api.py >> chatdb-api.log 2>&1 &

