"""Score Shadow AI audit responses and generate a remediation report."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from html import escape
from pathlib import Path
from typing import Literal


Answer = Literal["yes", "partial", "no", "na"]


@dataclass(frozen=True)
class Question:
    id: str
    label: str
    good_when: Literal["yes", "no"]
    weight: float = 1.0
    section: str = ""


QUESTION_SETS: dict[str, list[Question]] = {
    "rgpd": [
        Question("rgpd_finalite_documentee", "Finalite documentee", "yes"),
        Question("rgpd_base_legale", "Base legale identifiee", "yes"),
        Question("rgpd_dpa_fournisseurs", "DPA en place", "yes"),
        Question("rgpd_transferts_hors_ue", "Transferts hors UE encadres", "yes"),
        Question("rgpd_droits_personnes", "Droits des personnes operationnels", "yes"),
        Question("rgpd_chiffrement", "Chiffrement en transit et au repos", "yes"),
        Question("rgpd_retention", "Politique de retention definie", "yes"),
        Question("rgpd_detection_pii", "Detection PII avant envoi LLM", "yes"),
        Question("rgpd_dpia", "DPIA realise", "yes"),
        Question("rgpd_registre_traitements", "Registre des traitements a jour", "yes"),
    ],
    "cloud_act": [
        Question("cloud_openai_usage", "Usage OpenAI/ChatGPT", "no"),
        Question("cloud_azure_usage", "Usage Azure OpenAI/Copilot", "no"),
        Question("cloud_google_usage", "Usage Gemini/Vertex", "no"),
        Question("cloud_aws_usage", "Usage Bedrock", "no"),
        Question("cloud_infra_us", "Infrastructure cloud US", "no"),
        Question("cloud_provider_us_links", "Fournisseur avec lien juridique US", "no"),
        Question("cloud_sovereign_provider", "Hebergeur souverain europeen", "yes"),
        Question("cloud_pii_sent_to_us", "PII envoyee a des services US", "no"),
        Question("cloud_sensitive_data_sent", "Donnees sensibles envoyees a des services US", "no"),
        Question("cloud_end_to_end_encryption", "Chiffrement E2E avec cles client", "yes"),
    ],
    "shadow_ai": [
        Question("shadow_traffic_known_ai_domains", "Trafic vers domaines IA publics", "no"),
        Question("shadow_api_calls_external_ai", "Appels API externes IA", "no"),
        Question("shadow_copy_paste_behavior", "Copier/coller massif vers IA", "no"),
        Question("shadow_personal_ai_subscriptions", "Abonnements IA personnels", "no"),
        Question("shadow_no_official_policy", "Absence de politique IA", "no"),
        Question("shadow_no_official_tooling", "Absence d'outil IA officiel", "no"),
        Question("shadow_informal_training", "Formations IA informelles non encadrees", "no"),
        Question("shadow_unknown_data_exposure", "Exposition de donnees non cartographiee", "no"),
        Question("shadow_incident_monitoring", "Monitoring incidents IA en place", "yes"),
        Question("shadow_remediation_plan", "Plan de remediation formel", "yes"),
    ],
}


def _risk_for_answer(question: Question, answer: Answer) -> float | None:
    if answer == "na":
        return None
    if question.good_when == "yes":
        if answer == "yes":
            return 0.0
        if answer == "partial":
            return 0.5
        return 1.0
    if answer == "no":
        return 0.0
    if answer == "partial":
        return 0.5
    return 1.0


def _risk_level(score: float) -> str:
    if score >= 75:
        return "critique"
    if score >= 50:
        return "eleve"
    if score >= 25:
        return "modere"
    return "faible"


def _load_answers(path: Path) -> dict[str, dict[str, Answer]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    answers: dict[str, dict[str, Answer]] = {}
    for key in QUESTION_SETS:
        raw = payload.get(key, {})
        if not isinstance(raw, dict):
            raise ValueError(f"Section '{key}' must be an object.")
        answers[key] = {}
        for question_id, answer in raw.items():
            normalized = str(answer).strip().lower()
            if normalized not in {"yes", "partial", "no", "na"}:
                raise ValueError(
                    f"Invalid answer for {question_id}: {answer}. Use yes|partial|no|na."
                )
            answers[key][question_id] = normalized  # type: ignore[assignment]
    return answers


def _compute(answers: dict[str, dict[str, Answer]]) -> dict[str, object]:
    sections: dict[str, object] = {}
    weighted_sum = 0.0
    weighted_total = 0.0
    priorities: list[dict[str, object]] = []

    for section_name, questions in QUESTION_SETS.items():
        subtotal = 0.0
        subweight = 0.0
        missing: list[str] = []

        for question in questions:
            answer = answers.get(section_name, {}).get(question.id)
            if answer is None:
                missing.append(question.id)
                continue
            risk = _risk_for_answer(question, answer)
            if risk is None:
                continue
            subtotal += risk * question.weight
            subweight += question.weight
            if risk >= 0.5:
                priorities.append(
                    {
                        "section": section_name,
                        "question_id": question.id,
                        "label": question.label,
                        "answer": answer,
                        "risk_points": risk * question.weight,
                    }
                )

        section_score = (subtotal / subweight * 100) if subweight else 0.0
        sections[section_name] = {
            "score": section_score,
            "risk_level": _risk_level(section_score),
            "answered_weight": subweight,
            "missing_questions": missing,
        }
        weighted_sum += subtotal
        weighted_total += subweight

    overall_score = (weighted_sum / weighted_total * 100) if weighted_total else 0.0
    priorities.sort(key=lambda item: item["risk_points"], reverse=True)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall": {
            "score": overall_score,
            "risk_level": _risk_level(overall_score),
        },
        "sections": sections,
        "priorities": priorities[:10],
    }


def _write_markdown(path: Path, summary: dict[str, object]) -> None:
    overall = summary["overall"]
    sections = summary["sections"]
    priorities = summary["priorities"]

    lines = [
        "# Rapport de score Shadow AI",
        "",
        f"- Genere le: {summary['generated_at']}",
        f"- Score global: **{overall['score']:.1f}/100** ({overall['risk_level']})",
        "",
        "## Scores par section",
        "",
        "| Section | Score | Niveau |",
        "|---|---:|---|",
    ]

    for name in ("rgpd", "cloud_act", "shadow_ai"):
        info = sections[name]
        lines.append(f"| {name} | {info['score']:.1f}/100 | {info['risk_level']} |")

    lines.extend(
        [
            "",
            "## Priorites de remediation",
            "",
            "| Section | Question | Reponse |",
            "|---|---|---|",
        ]
    )

    if priorities:
        for item in priorities:
            lines.append(f"| {item['section']} | {item['label']} | {item['answer']} |")
    else:
        lines.append("| - | Aucune priorite critique detectee | - |")

    lines.extend(
        [
            "",
            "## Legend",
            "",
            "- `0-24.9`: risque faible",
            "- `25-49.9`: risque modere",
            "- `50-74.9`: risque eleve",
            "- `75-100`: risque critique",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def _write_html(path: Path, summary: dict[str, object]) -> None:
    overall = summary["overall"]
    sections = summary["sections"]
    priorities = summary["priorities"]

    section_rows: list[str] = []
    for name in ("rgpd", "cloud_act", "shadow_ai"):
        info = sections[name]
        section_rows.append(
            "<tr>"
            f"<td>{escape(name)}</td>"
            f"<td>{info['score']:.1f}/100</td>"
            f"<td>{escape(str(info['risk_level']))}</td>"
            "</tr>"
        )

    priority_rows: list[str] = []
    if priorities:
        for item in priorities:
            priority_rows.append(
                "<tr>"
                f"<td>{escape(str(item['section']))}</td>"
                f"<td>{escape(str(item['label']))}</td>"
                f"<td>{escape(str(item['answer']))}</td>"
                "</tr>"
            )
    else:
        priority_rows.append(
            "<tr><td>-</td><td>Aucune priorite critique detectee</td><td>-</td></tr>"
        )

    html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rapport de score Shadow AI</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem auto; max-width: 920px; line-height: 1.4; color: #1f2937; }}
    h1, h2 {{ color: #111827; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0 2rem; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.5rem; text-align: left; }}
    th {{ background: #f3f4f6; }}
    .meta {{ margin: 0 0 1rem; color: #374151; }}
    ul {{ padding-left: 1.2rem; }}
  </style>
</head>
<body>
  <h1>Rapport de score Shadow AI</h1>
  <p class="meta">Genere le: {escape(str(summary['generated_at']))}</p>

  <h2>Score global</h2>
  <table>
    <thead>
      <tr><th>Score</th><th>Niveau de risque</th></tr>
    </thead>
    <tbody>
      <tr><td>{overall['score']:.1f}/100</td><td>{escape(str(overall['risk_level']))}</td></tr>
    </tbody>
  </table>

  <h2>Scores par section</h2>
  <table>
    <thead>
      <tr><th>Section</th><th>Score</th><th>Niveau</th></tr>
    </thead>
    <tbody>
      {''.join(section_rows)}
    </tbody>
  </table>

  <h2>Priorites de remediation</h2>
  <table>
    <thead>
      <tr><th>Section</th><th>Question</th><th>Reponse</th></tr>
    </thead>
    <tbody>
      {''.join(priority_rows)}
    </tbody>
  </table>

  <h2>Legend</h2>
  <ul>
    <li><code>0-24.9</code>: risque faible</li>
    <li><code>25-49.9</code>: risque modere</li>
    <li><code>50-74.9</code>: risque eleve</li>
    <li><code>75-100</code>: risque critique</li>
  </ul>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def _write_template(path: Path) -> None:
    template: dict[str, dict[str, str]] = {}
    for section, questions in QUESTION_SETS.items():
        template[section] = {question.id: "partial" for question in questions}
    path.write_text(json.dumps(template, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute Shadow AI risk score from checklist responses."
    )
    parser.add_argument("--responses", help="Path to JSON responses file.")
    parser.add_argument(
        "--output-json",
        default="rapport/score-summary.json",
        help="Output JSON summary path.",
    )
    parser.add_argument(
        "--output-md",
        default="rapport/score-summary.md",
        help="Output Markdown report path.",
    )
    parser.add_argument(
        "--output-html",
        default=None,
        help="Optional output HTML report path.",
    )
    parser.add_argument(
        "--init-template",
        action="store_true",
        help="Generate a response template JSON and exit.",
    )
    parser.add_argument(
        "--template-path",
        default="questionnaire/reponses-template.json",
        help="Template path used with --init-template.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.init_template:
        template_path = Path(args.template_path)
        template_path.parent.mkdir(parents=True, exist_ok=True)
        _write_template(template_path)
        print(f"Template written: {template_path}")
        return 0

    if not args.responses:
        parser.error("--responses is required unless --init-template is used.")
        return 2

    response_path = Path(args.responses)
    if not response_path.exists():
        print(f"Response file not found: {response_path}")
        return 2

    try:
        answers = _load_answers(response_path)
    except ValueError as exc:
        print(f"Input error: {exc}")
        return 2

    summary = _compute(answers)

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_markdown(output_md, summary)

    output_html: Path | None = None
    if args.output_html:
        output_html = Path(args.output_html)
        output_html.parent.mkdir(parents=True, exist_ok=True)
        _write_html(output_html, summary)

    print(f"Global score: {summary['overall']['score']:.1f}/100 ({summary['overall']['risk_level']})")
    print(f"JSON report : {output_json}")
    print(f"MD report   : {output_md}")
    if output_html:
        print(f"HTML report : {output_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
