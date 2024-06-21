import uuid

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .exceptions import APIException
from .helpers import convert_language_to_iso
from .tasks import translate

app = FastAPI()


@app.exception_handler(APIException)
async def handle_api_exception(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


class TranslationRequest(BaseModel):
    text: str
    source_language: str = "english"
    target_language: str = "romanian"


class TaskStatus(BaseModel):
    status: str
    result: list | None = None
    id: str | None = None


@app.post("/translate")
async def api_translate(text: TranslationRequest):
    try:
        source_iso = convert_language_to_iso(text.source_language)
        target_iso = convert_language_to_iso(text.target_language)
    except ValueError as e:
        raise APIException(
            message=str(e), status_code=status.HTTP_400_BAD_REQUEST
        ) from e
    if source_iso == target_iso:
        raise APIException(
            message="Source and target languages are the same",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if source_iso != "en":
        raise APIException(
            message="Only English is supported as source language",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    task = translate.apply_async(
        args=[text.text, source_iso, target_iso],
        task_id="translate-" + str(uuid.uuid4()),
    )
    return TaskStatus(status=task.status, id=task.id, result=task.result)


@app.get("/translate/{task_id}")
async def read_translate(task_id: str):
    if not task_id.startswith("translate-"):
        raise APIException(
            message="Wrong task id", status_code=status.HTTP_400_BAD_REQUEST
        )
    task = translate.AsyncResult(task_id)
    return TaskStatus(status=task.status, id=task.id, result=task.result)
