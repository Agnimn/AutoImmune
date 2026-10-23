"""Tests for AutoImmune Evidence Dashboard generator."""
import re
from pathlib import Path

import pytest

from tools.make_dashboard import build_dashboard_data, determine_first_stop, generate_dashboard, render_html

REPO = Path(__file__).resolve().parents[1]


def test_build_dashboard_data_reconciles_with_evidence():
    evidence_path = REPO / "results" / "evidence.jsonl"
    data = build_dashboard_data(REPO, evidence_path, REPO / "results", REPO / "docs")
    
    assert len(data["evidence_rows"]) == 25
    assert len(data["units"]) == 25
    assert set(data["distinct_faults"]) == {"F01", "F04", "F06"}
    
    # Decisions reconciliation
    assert data["decision_counts"]["AUTO_APPLY"] == 6
    assert data["decision_counts"]["ESCALATE"] == 1
    assert data["decision_counts"]["REJECT"] == 18
    
    # Deployments and rollbacks must be 0 in gates-only evidence
    assert data["deployed_count"] == 0
    assert data["rollback_count"] == 0
    assert sum(data["approval_counts"].values()) == 0


def test_first_stop_distribution():
    evidence_path = REPO / "results" / "evidence.jsonl"
    data = build_dashboard_data(REPO, evidence_path, REPO / "results", REPO / "docs")
    stops = data["first_stop_counts"]
    
    assert stops["V0"] == 9
    assert stops["V1"] == 3
    assert stops["V2"] == 4
    assert stops["V3"] == 2
    assert stops["SURVIVED"] == 7
    assert sum(stops.values()) == 25


def test_generate_dashboard_creates_self_contained_offline_html(tmp_path):
    out_html = tmp_path / "dashboard.html"
    generate_dashboard(
        repo_root=REPO,
        evidence_path=REPO / "results" / "evidence.jsonl",
        results_dir=REPO / "results",
        docs_dir=REPO / "docs",
        out_path=out_html,
    )
    
    assert out_html.exists()
    content = out_html.read_text(encoding="utf-8")
    assert len(content) > 10000
    assert "<!DOCTYPE html>" in content
    
    # Confirm title and absence of "Phase 7" in visible header & title
    assert "<title>AutoImmune — Evidence Dashboard</title>" in content
    header_slice = content[:content.find("</header>")]
    assert "Phase 7" not in header_slice

    # Confirm zero external network dependencies / CDNs
    assert "http://" not in content
    assert "https://" not in content
    
    # Confirm all 9 required sections are rendered
    assert "Executive Overview" in content
    assert "LLM vs Scripted" in content
    assert "Validation Gates" in content
    assert "Per-Fault Breakdown" in content
    assert "Candidate Review" in content
    assert "Policy Comparison" in content
    assert "Approval &amp; Rollback" in content or "Approval & Rollback" in content
    assert "Acceptance Checks" in content
    assert "Known Limitations" in content
    
    # Verify specific integrity facts
    assert "AUTO_APPLY != Deployment" in content or "AUTO_APPLY" in content
    assert "0/0 (N/A)" in content
    assert "qwen2.5-coder:7b" in content
    assert "0 of 9" in content


def test_gate_statuses_and_error_handling(tmp_path):
    out_html = tmp_path / "dashboard.html"
    generate_dashboard(REPO, REPO / "results" / "evidence.jsonl", REPO / "results", REPO / "docs", out_html)
    content = out_html.read_text(encoding="utf-8")
    
    # Verify F06 Docker EOF error candidate is displayed with tool error, not a pass
    assert "F06-scripted-05420f6c" in content
    assert "Docker EOF tooling error" in content or "tool error" in content
    
    # Verify F04 localization failure is displayed
    assert "0/8" in content
