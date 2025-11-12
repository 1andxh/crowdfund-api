from fastapi import FastAPI


version = "v1"

app = FastAPI(
    version=version, title="Crowdfund-API", description="API for crowdfunding"
)
