import pytest
from pathlib import Path
from snipvault import vault


@pytest.fixture
def tmp_vault(tmp_path):
    return tmp_path / "vault.json"


def test_add_and_get(tmp_vault):
    vault.add("hello", "print('hello')", path=tmp_vault)
    entry = vault.get("hello", path=tmp_vault)
    assert entry["snippet"] == "print('hello')"
    assert entry["tags"] == []


def test_add_with_tags(tmp_vault):
    vault.add("greet", "echo hi", tags=["bash", "util"], path=tmp_vault)
    entry = vault.get("greet", path=tmp_vault)
    assert entry["tags"] == ["bash", "util"]


def test_get_missing(tmp_vault):
    assert vault.get("nope", path=tmp_vault) is None


def test_delete(tmp_vault):
    vault.add("tmp", "x = 1", path=tmp_vault)
    assert vault.delete("tmp", path=tmp_vault) is True
    assert vault.get("tmp", path=tmp_vault) is None


def test_delete_missing(tmp_vault):
    assert vault.delete("ghost", path=tmp_vault) is False


def test_list_all(tmp_vault):
    vault.add("a", "aaa", path=tmp_vault)
    vault.add("b", "bbb", path=tmp_vault)
    data = vault.list_all(path=tmp_vault)
    assert set(data.keys()) == {"a", "b"}


def test_search_by_name(tmp_vault):
    vault.add("curl_example", "curl https://example.com", path=tmp_vault)
    results = vault.search("curl", path=tmp_vault)
    assert "curl_example" in results


def test_search_by_snippet(tmp_vault):
    vault.add("fetch", "wget https://example.com", path=tmp_vault)
    results = vault.search("wget", path=tmp_vault)
    assert "fetch" in results


def test_search_by_tag(tmp_vault):
    vault.add("loop", "for i in range(10): pass", tags=["python"], path=tmp_vault)
    results = vault.search("python", path=tmp_vault)
    assert "loop" in results


def test_search_no_match(tmp_vault):
    vault.add("x", "y", path=tmp_vault)
    assert vault.search("zzz", path=tmp_vault) == {}
