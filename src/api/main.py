from fastapi import FastAPI
from pydantic import BaseModel

from .tasks import hello, translate

app = FastAPI()


class TranslationRequest(BaseModel):
    text: str


@app.get("/")
async def read_root():
    task = hello.delay()
    return {"status": task.status, "id": task.id}


@app.get("/task/{task_id}")
async def read_task(task_id: str):
    task = hello.AsyncResult(task_id)
    return {"status": task.status, "result": task.result}


@app.post("/translate")
async def api_translate(text: TranslationRequest):
    task = translate.delay(text.text)
    return {"status": task.status, "id": task.id}
