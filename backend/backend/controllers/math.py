from backend import app
import backend.tasks.add

from celery.result import AsyncResult
from flask import request


@app.post("/add")
def start_add() -> dict[str, object]:
    a = request.json.get("a")
    b = request.json.get("b")
    result = backend.tasks.add.add_together.delay(a, b)
    return {"result_id": result.id}


@app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
