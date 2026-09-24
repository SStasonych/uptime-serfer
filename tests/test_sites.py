import pytest


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
    # Сначала добавляем сайт
    await client.post("/api/sites/", json={"url": "https://example.com"})

    # Пытаемся добавить повторно
    response = await client.post("/api/sites/", json={"url": "https://example.com"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_all_sites(client):
    await client.post("/api/sites/", json={"url": "https://example.com"})
    await client.post("/api/sites/", json={"url": "https://anotherexample.com"})

    response = await client.get("/api/sites/")
    assert response.status_code == 200
    assert len(response.json()) == 2
