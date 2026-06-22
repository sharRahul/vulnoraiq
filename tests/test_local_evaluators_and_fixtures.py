from __future__ import annotations

from core.evaluators import LocalEvaluatorSuite
from examples.local_demo_targets.owasp_fixture_targets import OwaspFixtureTarget


def test_local_evaluator_forbidden_contains() -> None:
    result = LocalEvaluatorSuite.forbidden_contains("safe response", ["blocked marker"])

    assert result.status == "pass"


def test_owasp_good_fixtures_pass() -> None:
    fixture = OwaspFixtureTarget()

    for index in range(1, 11):
        result = fixture.run(f"LLM{index:02d}", "good")
        assert result.status == "pass", result


def test_owasp_bad_fixtures_are_detected() -> None:
    fixture = OwaspFixtureTarget()

    for index in range(1, 11):
        result = fixture.run(f"LLM{index:02d}", "bad")
        assert result.status == "fail", result
        assert result.evaluator_results
