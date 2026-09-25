import pytest
import anyio


@pytest.mark.asyncio
async def test_create_site(client):
    response = await client.post("/api/sites/", json={
        "url": "https://example.com",
        "description": "Тестовый сайт"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == "https://example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_duplicate_site(client):
    await client.post("/api/sites/", json={"url": "https://example.com"})

    response = await client.post("/api/sites/", json={"url": "https://example.com"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_all_sites(client):
    await client.post("/api/sites/", json={"url": "https://example.com"})
    await client.post("/api/sites/", json={"url": "https://anotherexample.com"})

    response = await client.get("/api/sites/")
    assert response.status_code == 200
    assert len(response.json()) == 2

import asyncio
import time

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_async_vs_sync():
    # Асинхронное приложение
    async_app = FastAPI()

    @async_app.get("/slow")
    async def async_slow():
        await asyncio.sleep(1)  # имитация I/O
        return {"status": "ok"}

    # Синхронное приложение
    sync_app = FastAPI()

    @sync_app.get("/slow")
    def sync_slow():
        time.sleep(1)
        return {"status": "ok"}

    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 2

    async with AsyncClient(transport=ASGITransport(app=async_app), base_url="http://test") as client:
        start = time.perf_counter()
        await asyncio.gather(*[client.get("/slow") for _ in range(20)])
        async_time = time.perf_counter() - start

    async with AsyncClient(transport=ASGITransport(app=sync_app), base_url="http://test") as client:
        start = time.perf_counter()
        await asyncio.gather(*[client.get("/slow") for _ in range(20)])
        sync_time = time.perf_counter() - start

    assert async_time < sync_time

    print(f"Async time: {async_time}")
    print(f"Sync time: {sync_time}")

