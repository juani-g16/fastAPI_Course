from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# with Alembic module this is not longer necesary (althoug it could be kept without problems)
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# set up for testing purposes, not all sites should be allowed to access our API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "this is our api"}
