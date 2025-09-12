import logging
import time
import uuid
from fastapi import Request

logger = logging.getLogger("backend")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

async def log_requests(request: Request, call_next):
    correlation_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start = time.time()
    logger.info(f"Request: {request.method} {request.url}", extra={"correlation_id": correlation_id})
    try:
        response = await call_next(request)
        duration_ms = int((time.time() - start) * 1000)
        response.headers["X-Request-ID"] = correlation_id
        logger.info(
            f"Response {response.status_code} {request.method} {request.url.path} in {duration_ms}ms",
            extra={"correlation_id": correlation_id, "duration_ms": duration_ms},
        )
        return response
    except Exception as exc:
        duration_ms = int((time.time() - start) * 1000)
        logger.exception(
            f"Unhandled error {request.method} {request.url.path} in {duration_ms}ms",
            extra={"correlation_id": correlation_id, "duration_ms": duration_ms},
        )
        raise
