from fastapi import FastAPI
from api.routers.spotify import router as spotify_router

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")
# Include the router from spotify_endpoints
app.include_router(spotify_router)

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}
