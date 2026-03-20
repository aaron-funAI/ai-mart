from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "AI-Mart 运行中", "message": "你好，SDE-AI！这是我的第一个接口。"}