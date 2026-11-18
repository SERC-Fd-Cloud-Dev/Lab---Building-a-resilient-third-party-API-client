from http import HTTPStatus
from fastapi.responses import JSONResponse

class UpstreamFailure(Exception):
    def __init__(self, kind, status=502, retryable=False, fallback=False):
        self.kind, self.status = kind, status
        self.retryable, self.fallback = retryable, fallback
        super().__init__(kind)  # Safe fixed category, never a URL or response body.

def classify_status(status):
    if status in {500, 502, 503, 504}:
        return UpstreamFailure('upstream_unavailable', 503, True, True)
    if status == 404:
        return UpstreamFailure('not_found', 404)
    # Exercise 6: investigate a rate-limited supplier and refine this mapping.
    return UpstreamFailure('upstream_rejected', 502)

def problem(error, request_id):
    details = {
        'timeout': 'The upstream service did not respond in time.',
        'connection': 'The upstream service could not be reached.',
        'upstream_unavailable': 'The upstream service is temporarily unavailable.',
        'circuit_open': 'The upstream service is temporarily unavailable.',
        'not_found': 'The requested resource was not found.',
        'rate_limited': 'The upstream service is rate limiting requests. Try later.',
    }
    return JSONResponse(status_code=error.status, media_type='application/problem+json',
        content={'type': 'about:blank', 'title': HTTPStatus(error.status).phrase,
                 'status': error.status,
                 'detail': details.get(error.kind, 'The upstream service could not provide usable data.'),
                 'instance': f'urn:uuid:{request_id}'})
