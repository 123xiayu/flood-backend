from src.api.v1.routes import api_router
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="flood-backend")
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
