import argparse
import asyncio
import time
from dataclasses import dataclass
from statistics import mean
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass
class RequestResult:
    status: int
    elapsed_ms: float
    ok: bool


def perform_request(base_url: str, query: str, timeout: float) -> RequestResult:
    params = urlencode({"q": query, "page": 1, "page_size": 10})
    url = f"{base_url.rstrip('/')}/api/v1/search?{params}"
    start = time.perf_counter()

    try:
        with urlopen(Request(url), timeout=timeout) as response:
            response.read()
            status = response.status
    except Exception:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return RequestResult(status=0, elapsed_ms=elapsed_ms, ok=False)

    elapsed_ms = (time.perf_counter() - start) * 1000
    return RequestResult(status=status, elapsed_ms=elapsed_ms, ok=200 <= status < 300)


async def run_load_test(base_url: str, query: str, users: int, timeout: float) -> list[RequestResult]:
    tasks = [
        asyncio.to_thread(perform_request, base_url, query, timeout)
        for _ in range(users)
    ]
    return await asyncio.gather(*tasks)


def percentile(values: list[float], percent: float) -> float:
    if not values:
        return 0.0

    sorted_values = sorted(values)
    index = min(len(sorted_values) - 1, round((percent / 100) * (len(sorted_values) - 1)))
    return sorted_values[index]


def main() -> int:
    parser = argparse.ArgumentParser(description="Load test for search endpoint")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--query", default="EPrac")
    parser.add_argument("--users", type=int, default=50)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    started = time.perf_counter()
    results = asyncio.run(run_load_test(args.base_url, args.query, args.users, args.timeout))
    total_elapsed_ms = (time.perf_counter() - started) * 1000

    successful = [result for result in results if result.ok]
    failed = [result for result in results if not result.ok]
    timings = [result.elapsed_ms for result in successful]

    print(f"Base URL: {args.base_url}")
    print(f"Query: {args.query}")
    print(f"Concurrent users: {args.users}")
    print(f"Successful requests: {len(successful)}")
    print(f"Failed requests: {len(failed)}")
    print(f"Total elapsed: {total_elapsed_ms:.2f} ms")

    if timings:
        print(f"Average response: {mean(timings):.2f} ms")
        print(f"Min response: {min(timings):.2f} ms")
        print(f"Max response: {max(timings):.2f} ms")
        print(f"P95 response: {percentile(timings, 95):.2f} ms")

    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
