import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from chatdb import generate_chat_responses, init_database

app = FastAPI()
mysql_db = init_database()

# 创建一个HTTPBearer实例，用于处理Authorization头
security = HTTPBearer()

# 定义一个函数来验证Authorization头
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "Fashion!@#":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials

@app.post("/v1/chatdb")
def chatdb_handler(data: dict, credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data:", data)
    user_input = data.get("user_input")
    if not user_input:
        return {"error": "User input is required"}
    sql_results, sql_commands, err = generate_chat_responses(user_inp=user_input, mysql_db=mysql_db, historical_message=[])
    if err:
        return {"error": err}
    result = ""
    for sql_command, sql_result in zip(sql_commands, sql_results):
        result += f"sql命令：{sql_command[0]}\n"
        result += f"执行结果：{sql_result}\n\n"
    return {"result": result}

def test():
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=41973)
    user_input = """
    To allocate tasks for the order with name"Emily_Dress," which involves producing a Red, M size Dress. 
    30% of the cutting tasks will be assigned to the cutting group "Master Cutters," and the left 70% to the cutting group "Professional Cutters." 
    The task will start from today and must be completed within 30 days. 
    All sewing tasks will be assigned to "Elite Sewers," and are required to be completed within 60 days starting from today.
    """
    sql_results, sql_commands, err = generate_chat_responses(user_inp=user_input, mysql_db=mysql_db, historical_message=[])
    if err:
        return {"error": err}
    result = ""
    for sql_command, sql_result in zip(sql_commands, sql_results):
        result += f"sql命令：{sql_command[0]}\n"
        result += f"执行结果：{sql_result}\n\n"
    return {"result": result}

if __name__ == "__main__":
    print(test())


