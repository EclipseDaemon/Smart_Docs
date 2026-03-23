import pytest
import io
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


def make_pdf_file(content: str = "Test document content for SmartDocs"):
    return ("test.pdf", io.BytesIO(content.encode()), "application/pdf")


def make_docx_file():
    return ("test.docx", io.BytesIO(b"fake docx content"), 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document")


async def test_list_documents_empty(client: AsyncClient, auth_headers):
    response = await client.get("/documents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["documents"] == []


async def test_list_documents_unauthorized(client: AsyncClient):
    response = await client.get("/documents")
    assert response.status_code == 401


async def test_upload_document_success(client: AsyncClient, auth_headers):
    name, content, mime = make_pdf_file()
    response = await client.post(
        "/documents/upload",
        headers=auth_headers,
        files={"file": (name, content, mime)}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "test.pdf"
    assert data["file_type"] == "pdf"
    assert data["is_processed"] == False
    assert "id" in data


async def test_upload_document_unauthorized(client: AsyncClient):
    name, content, mime = make_pdf_file()
    response = await client.post(
        "/documents/upload",
        files={"file": (name, content, mime)}
    )
    assert response.status_code == 401


async def test_upload_unsupported_file_type(client: AsyncClient, auth_headers):
    response = await client.post(
        "/documents/upload",
        headers=auth_headers,
        files={"file": ("test.txt", io.BytesIO(b"text content"), "text/plain")}
    )
    assert response.status_code == 415


async def test_get_document_by_id(client: AsyncClient, auth_headers):
    name, content, mime = make_pdf_file()
    upload = await client.post(
        "/documents/upload",
        headers=auth_headers,
        files={"file": (name, content, mime)}
    )
    doc_id = upload.json()["id"]

    response = await client.get(f"/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == doc_id


async def test_get_document_not_found(client: AsyncClient, auth_headers):
    response = await client.get("/documents/99999", headers=auth_headers)
    assert response.status_code == 404


async def test_delete_document_success(client: AsyncClient, auth_headers):
    name, content, mime = make_pdf_file()
    upload = await client.post(
        "/documents/upload",
        headers=auth_headers,
        files={"file": (name, content, mime)}
    )
    doc_id = upload.json()["id"]

    response = await client.delete(f"/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 204

    get_response = await client.get(f"/documents/{doc_id}", headers=auth_headers)
    assert get_response.status_code == 404


async def test_delete_document_not_found(client: AsyncClient, auth_headers):
    response = await client.delete("/documents/99999", headers=auth_headers)
    assert response.status_code == 404


async def test_user_cannot_access_other_user_document(client: AsyncClient, auth_headers):
    name, content, mime = make_pdf_file()
    upload = await client.post(
        "/documents/upload",
        headers=auth_headers,
        files={"file": (name, content, mime)}
    )
    doc_id = upload.json()["id"]

    await client.post("/auth/register", json={
        "email": "other@test.com",
        "password": "password123"
    })
    login = await client.post(
        "/auth/login",
        data={"username": "other@test.com", "password": "password123"}
    )
    other_token = login.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    response = await client.get(f"/documents/{doc_id}", headers=other_headers)
    assert response.status_code == 404