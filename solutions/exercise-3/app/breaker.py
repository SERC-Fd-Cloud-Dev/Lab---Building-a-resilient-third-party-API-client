from circuitbreaker import CircuitBreaker
from .errors import UpstreamFailure

def make_breaker():
    return CircuitBreaker(failure_threshold=2, recovery_timeout=5,
        expected_exception=lambda exc_type, exc: isinstance(exc, UpstreamFailure) and exc.retryable,
        name='supplier')
