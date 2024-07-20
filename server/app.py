from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from chatbot import chatbot_response
app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
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


handler = Mangum(app)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
