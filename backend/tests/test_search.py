import pytest
from pathlib import Path
import tempfile
import json

from ai_document_assistant.core.search import DocumentSearch

@pytest.fixture
def temp_storage():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

def test_document_search_initialization(temp_storage):
    search = DocumentSearch(temp_storage)
    assert search.storage_dir == temp_storage
    assert search.index_file == temp_storage / "search_index.json"

def test_document_indexing(temp_storage):
    search = DocumentSearch(temp_storage)
    doc_id = "test123"
    content = "This is a test document"
    metadata = {
        "filename": "test.txt",
        "file_path": "/path/to/test.txt",
        "file_size": 100,
    }

    search.index_document(doc_id, content, metadata)

    # Verify the document was indexed
    assert doc_id in search.index
    assert search.index[doc_id]["content"] == content
    assert search.index[doc_id]["metadata"] == metadata

def test_document_search(temp_storage):
    search = DocumentSearch(temp_storage)
    
    # Index test documents
    search.index_document(
        "doc1",
        "The quick brown fox jumps over the lazy dog",
        {"filename": "doc1.txt", "file_path": "/doc1.txt", "file_size": 100}
    )
    search.index_document(
        "doc2",
        "The lazy cat sleeps all day",
        {"filename": "doc2.txt", "file_path": "/doc2.txt", "file_size": 100}
    )

    # Test search functionality
    results = search.search("lazy")
    assert len(results) == 2
    assert any(r["doc_id"] == "doc1" for r in results)
    assert any(r["doc_id"] == "doc2" for r in results)

    results = search.search("fox")
    assert len(results) == 1
    assert results[0]["doc_id"] == "doc1"

def test_document_deletion(temp_storage):
    search = DocumentSearch(temp_storage)
    doc_id = "test123"
    
    search.index_document(
        doc_id,
        "Test content",
        {"filename": "test.txt", "file_path": "/test.txt", "file_size": 100}
    )
    
    assert doc_id in search.index
    search.delete_document(doc_id)
    assert doc_id not in search.index 