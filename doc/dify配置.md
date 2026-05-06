



## Dify添加自定义工具

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "ChatDB API",
    "description": "API for interacting with the ChatDB service.",
    "version": "v1.0.0"
  },
  "servers": [
    {
      "url": "http://139.159.190.208:41973"
    }
  ],
  "paths": {
    "/v1/chatdb": {
      "post": {
        "description": "Text to sql. Endpoint to interact with database using natural language.",
        "operationId": "chatDB",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UserInputRequest"
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "components": {
    "schemas": {
      "UserInputRequest": {
        "type": "object",
        "properties": {
          "user_input": {
            "type": "string",
            "description": "The input provided by the user."
          },
          "conversation_id": {
            "type": "string",
            "description": "Unique identifier for the conversation."
          }
        },
        "required": [
          "user_input",
          "conversation_id"
        ]
      }
    }
  }
}
```

> 注意修改```servers.url```


2. 导入application
在dify中创建导入DSL文件 ```chat manufacture.yml```(本文档同级目录下)
