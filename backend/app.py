from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from chatbot import chatbot_response

app = FastAPI()
origins = ["https://finance-chatbot-sigma.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],  # Specific methods
    allow_headers=["*"]
)

@app.post('/chat')
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get('message')
        
        if not user_input:
            return JSONResponse(status_code=400, content={"error": "Message not provided"})
        
        response_data = {'response': chatbot_response(user_input)}
        
        return JSONResponse(content=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
@app.options("/{path:path}")
async def preflight_handler(path: str, request: Request):
    return JSONResponse(headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type"
    })


handler = Mangum(app)
