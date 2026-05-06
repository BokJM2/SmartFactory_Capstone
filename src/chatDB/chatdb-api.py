import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from chatdb import generate_chat_responses, init_database

app = FastAPI()
mysql_db = init_database()
from expired_dict import ExpiredDict

history = ExpiredDict(3600)

# 创建一个HTTPBearer实例，用于处理Authorization头
security = HTTPBearer()

# 定义一个函数来验证Authorization头
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print(credentials)
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
    conversation_id = data.get("conversation_id")
    historical_message, dialogue_context, context_abstract = history.get(conversation_id, ([], [], ""))
    if not user_input:
        return {"error": "User input is required"}
    sql_results, sql_commands, err, response, context_abstract = generate_chat_responses(
        user_inp=user_input, mysql_db=mysql_db, historical_message=historical_message, context_abstract=context_abstract
    )
    dialogue_context.extend([f'User: {user_input}', f'System: {response}'])
    history[conversation_id] = historical_message, dialogue_context,  context_abstract
    if err:
        return {"error": err}
    result = f"Final response\n{response}\n\n"
    # for sql_command, sql_result in zip(sql_commands, sql_results):
    #     result += f"sql command：{sql_command[0]}\n"
    #     result += f"execution result：{sql_result}\n\n"
    # return {"result": result}
    return sql_results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=41973, workers=1)
