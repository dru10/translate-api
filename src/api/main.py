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


@app.post("/translate")
async def api_translate(text: TranslationRequest):
    try:
        source_iso = convert_language_to_iso(text.source_language)
        target_iso = convert_language_to_iso(text.target_language)
    except ValueError as e:
        raise APIException(
            message=str(e), status_code=status.HTTP_400_BAD_REQUEST
        ) from e
    task = translate.apply_async(
        args=[text.text], task_id="translate-" + str(uuid.uuid4())
    )
    return {"status": task.status, "id": task.id}


@app.get("/translate/{task_id}")
async def read_translate(task_id: str):
    if not task_id.startswith("translate-"):
        raise APIException(
            message="Wrong task id", status_code=status.HTTP_400_BAD_REQUEST
        )
    task = translate.AsyncResult(task_id)
    return {"status": task.status, "result": task.result}
