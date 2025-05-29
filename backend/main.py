from fastapi import FastAPI
from routes import api_router

app = FastAPI(
    title="Sistema de Eventos",
    description="API para gerenciamento de festas, convites e sugestões",
    version="1.0.0"
)

# Include all routes from the modular routers
app.include_router(api_router)

# If you need to add any middleware or event handlers, add them here
@app.on_event("startup")
async def startup_event():
    print("API de Sistema de Eventos iniciada!")

@app.on_event("shutdown")
async def shutdown_event():
    print("API de Sistema de Eventos finalizada!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
