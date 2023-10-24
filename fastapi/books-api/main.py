from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    return "Welcom to the books api"