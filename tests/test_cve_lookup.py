from __future__ import annotations

from integrations import cve_lookup

_NVD_SAMPLE = {
    "vulnerabilities": [
        {
            "cve": {
                "id": "CVE-2024-12345",
                "descriptions": [{"lang": "en", "value": "Prompt injection in an LLM agent allows instruction override."}],
                "metrics": {
                    "cvssMetricV31": [
                        {"cvssData": {"baseScore": 8.1, "baseSeverity": "HIGH"}}
                    ]
                },
                "published": "2024-09-01T00:00:00",
            }
        }
    ]
}

_OSV_SAMPLE = {
    "vulns": [
        {"id": "GHSA-xxxx", "summary": "Vulnerable dependency", "published": "2024-01-01"}
    ]
}


def test_keywords_from_finding_extracts_terms():
    kw = cve_lookup.keywords_from_finding(
        {"title": "Prompt injection boundary", "category": "LLM01", "affected_component": "Prompt layer"}
    )
    assert "injection" in kw.lower()
    assert "the" not in kw.lower().split()


def test_search_nvd_parses_records(monkeypatch):
    monkeypatch.setattr(cve_lookup, "_http_get_json", lambda url, params, timeout: _NVD_SAMPLE)
    records = cve_lookup.search_nvd("prompt injection llm", limit=5)
    assert records and records[0]["id"] == "CVE-2024-12345"
    assert records[0]["source"] == "NVD"
    assert "8.1" in records[0]["severity"]
    assert records[0]["url"].endswith("CVE-2024-12345")


def test_search_osv_parses_records(monkeypatch):
    monkeypatch.setattr(cve_lookup, "_http_post_json", lambda url, body, timeout: _OSV_SAMPLE)
    records = cve_lookup.search_osv("somepkg", ecosystem="PyPI")
    assert records and records[0]["id"] == "GHSA-xxxx"
    assert records[0]["source"] == "OSV"


def test_lookup_for_finding_with_match(monkeypatch):
    monkeypatch.setattr(cve_lookup, "_http_get_json", lambda url, params, timeout: _NVD_SAMPLE)
    out = cve_lookup.lookup_for_finding({"title": "Prompt injection", "category": "LLM01"})
    assert out["online"] is True
    assert out["match_count"] == 1
    assert out["candidate_novel"] is False
    assert "NVD" in out["sources_queried"]


def test_lookup_for_finding_flags_candidate_novel_on_empty(monkeypatch):
    monkeypatch.setattr(cve_lookup, "_http_get_json", lambda url, params, timeout: {"vulnerabilities": []})
    out = cve_lookup.lookup_for_finding({"title": "Some unusual novel weakness"})
    assert out["online"] is True
    assert out["match_count"] == 0
    assert out["candidate_novel"] is True
    assert "verify" in out["note"].lower()


def test_lookup_for_finding_offline_is_graceful(monkeypatch):
    def boom(*_args, **_kwargs):
        raise OSError("network down")

    monkeypatch.setattr(cve_lookup, "_http_get_json", boom)
    out = cve_lookup.lookup_for_finding({"title": "Prompt injection"})
    assert out["online"] is False
    assert out["candidate_novel"] is False  # cannot claim novelty if lookup failed
    assert out["errors"]
