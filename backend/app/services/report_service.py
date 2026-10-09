"""Discovery Report Generator (HTML/Printable format).

Compliant with Section 5.12 of SKYTRACE AI specification.
Generates self-contained, evidence-linked HTML scientific discovery reports.
"""

from typing import Any, Dict
from app.models.schemas import DISCLAIMER_TEXT, ScientificDiscoveryPassport


class ReportService:
    """Generates standalone HTML scientific discovery reports from Discovery Passports."""

    @staticmethod
    def generate_html_report(passport: ScientificDiscoveryPassport) -> str:
        """Render self-contained HTML report with embedded styles and charts."""
        p = passport
        analysis = p.analysis
        checks_html = "".join(
            f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #1e3a5f; font-family: monospace;">{c.name}</td>
                <td style="padding: 8px; border-bottom: 1px solid #1e3a5f;">
                    <span style="display: inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;
                        background: {'#064e3b; color: #34d399' if c.status == 'PASS' else '#78350f; color: #fbbf24' if c.status == 'CAUTION' else '#881337; color: #f87171'};">
                        {c.status}
                    </span>
                </td>
                <td style="padding: 8px; border-bottom: 1px solid #1e3a5f; color: #cbd5e1; font-size: 12px;">{c.details}</td>
            </tr>
            """
            for c in p.false_alarm_investigation.checks
        )

        alternatives_html = "".join(
            f"<li>{alt}</li>" for alt in p.false_alarm_investigation.possible_alternatives
        )

        follow_up_html = "".join(
            f"<li>{sug}</li>" for sug in p.follow_up_suggestions
        )

        limitations_html = "".join(
            f"<li>{lim}</li>" for lim in p.limitations
        )

        catalog_matches_html = (
            "".join(
                f"""<li><strong>{m.get('catalog')}:</strong> {m.get('counterpart_id')} (sep: {m.get('angular_separation_arcsec')}\") - {m.get('notes', '')}</li>"""
                for m in p.known_object_cross_check.matches
            )
            if p.known_object_cross_check.matches
            else "<li>No counterparts detected within search radius.</li>"
        )

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SKYTRACE AI Discovery Report — {p.source_identity.get('source_id')}</title>
    <style>
        body {{
            background: #020813;
            color: #e2e8f0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 40px;
            line-height: 1.6;
        }}
        .report-container {{
            max-width: 900px;
            margin: 0 auto;
            background: #061527;
            border: 1px solid #1e3a8a;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        }}
        .disclaimer-banner {{
            background: #7c2d12;
            color: #fed7aa;
            border: 1px solid #ea580c;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 13px;
            text-align: center;
            letter-spacing: 0.05em;
            margin-bottom: 30px;
            text-transform: uppercase;
        }}
        h1, h2, h3, h4 {{
            color: #7dd3fc;
            margin-top: 0;
            font-family: monospace;
        }}
        .header-meta {{
            display: flex;
            justify-content: space-between;
            border-bottom: 2px solid #1e3a8a;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .score-box {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 30px;
        }}
        .card {{
            background: #020b18;
            border: 1px solid #1e3a5f;
            border-radius: 10px;
            padding: 16px;
        }}
        .card-label {{
            font-size: 11px;
            color: #94a3b8;
            text-transform: uppercase;
            font-family: monospace;
        }}
        .card-value {{
            font-size: 24px;
            font-weight: bold;
            color: #38bdf8;
            font-family: monospace;
            margin-top: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th {{
            background: #0a1f38;
            color: #7dd3fc;
            text-align: left;
            padding: 10px;
            font-family: monospace;
            font-size: 12px;
        }}
        ul {{
            margin: 0;
            padding-left: 20px;
            color: #cbd5e1;
            font-size: 13px;
        }}
        li {{
            margin-bottom: 6px;
        }}
        .fits-box {{
            background: #01060e;
            border: 1px solid #1e3a5f;
            border-radius: 8px;
            padding: 16px;
            font-family: monospace;
            font-size: 11px;
            color: #38bdf8;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        @media print {{
            body {{ background: #fff; color: #000; padding: 0; }}
            .report-container {{ border: none; box-shadow: none; padding: 20px; }}
            .disclaimer-banner {{ background: #fee2e2; color: #991b1b; border-color: #ef4444; }}
            h1, h2, h3, h4 {{ color: #0369a1; }}
            .card {{ background: #f8fafc; border-color: #cbd5e1; }}
            .card-value {{ color: #0284c7; }}
            th {{ background: #e2e8f0; color: #0f172a; }}
            .fits-box {{ background: #f1f5f9; color: #0f172a; }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="disclaimer-banner">
            ⚠ {p.disclaimer}
        </div>

        <div class="header-meta">
            <div>
                <h1>SKYTRACE AI — Scientific Discovery Report</h1>
                <p style="margin: 0; font-family: monospace; color: #94a3b8; font-size: 13px;">
                    Candidate ID: <strong>{p.source_identity.get('source_id')}</strong> | IAU: <strong>{p.source_identity.get('iau_designation')}</strong>
                </p>
                <p style="margin: 4px 0 0 0; font-family: monospace; color: #64748b; font-size: 12px;">
                    Passport ID: {p.passport_id} | Release: {analysis.get('algorithm_version')}
                </p>
            </div>
            <div style="text-align: right; font-family: monospace; font-size: 12px; color: #94a3b8;">
                <div>Field: {p.source_identity.get('region_name')}</div>
                <div>Epochs: {p.source_identity.get('usable_epoch_count')} passes</div>
                <div>Generated: {p.generated_at}</div>
            </div>
        </div>

        <div class="score-box">
            <div class="card">
                <div class="card-label">Scientific Interestingness</div>
                <div class="card-value" style="color: #fbbf24;">{analysis.get('interestingness_score'):.1f} / 100</div>
                <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Heuristic prioritization metric</div>
            </div>
            <div class="card">
                <div class="card-label">Evidence Confidence</div>
                <div class="card-value">{analysis.get('evidence_confidence', {}).get('numeric_value', 0):.0f}%</div>
                <div style="font-size: 11px; color: #34d399; margin-top: 4px;">Tier: {analysis.get('evidence_confidence', {}).get('tier')}</div>
            </div>
            <div class="card">
                <div class="card-label">Scientific Priority</div>
                <div class="card-value">{analysis.get('scientific_priority')}</div>
                <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Triage category</div>
            </div>
        </div>

        <div class="card" style="margin-bottom: 24px;">
            <h3>Astrophysical Summary & Evidence</h3>
            <p style="color: #cbd5e1; font-size: 13px; margin: 0 0 12px 0;">
                {p.position_and_motion.assessment} {p.photometry.assessment}
            </p>
            <ul>
                {"".join(f"<li>{r}</li>" for r in analysis.get('why_interesting', []))}
            </ul>
        </div>

        <div class="card" style="margin-bottom: 24px;">
            <h3>Data Quality & False-Alarm Investigation</h3>
            <p style="font-size: 12px; color: #94a3b8; margin-top: 0;">
                Assessment: <strong>{p.false_alarm_investigation.assessment}</strong>
            </p>
            <table>
                <thead>
                    <tr>
                        <th>Quality Check</th>
                        <th>Status</th>
                        <th>Findings & Metrics</th>
                    </tr>
                </thead>
                <tbody>
                    {checks_html}
                </tbody>
            </table>
            <div style="margin-top: 16px;">
                <h4 style="font-size: 12px; margin-bottom: 6px;">Possible Alternative Explanations</h4>
                <ul>
                    {alternatives_html}
                </ul>
            </div>
        </div>

        <div class="card" style="margin-bottom: 24px;">
            <h3>Known-Object Catalog Cross-Check</h3>
            <p style="font-size: 12px; color: #94a3b8; margin: 0 0 8px 0;">
                Status: <strong>{p.known_object_cross_check.status}</strong> (Radius: {p.known_object_cross_check.search_radius_arcsec:.1f}\")
            </p>
            <ul>
                {catalog_matches_html}
            </ul>
            <p style="font-size: 11px; color: #94a3b8; font-style: italic; margin-top: 10px;">
                {p.known_object_cross_check.limitations}
            </p>
        </div>

        <div class="card" style="margin-bottom: 24px;">
            <h3>Observatory Follow-Up Suggestions</h3>
            <ul>
                {follow_up_html}
            </ul>
        </div>

        <div class="card" style="margin-bottom: 24px;">
            <h3>Mandatory Scientific Limitations</h3>
            <ul>
                {limitations_html}
            </ul>
        </div>

        {f'''
        <div class="card">
            <h3>Standard 80-Column FITS Header Card</h3>
            <div class="fits-box">{p.fits_header_card}</div>
        </div>
        ''' if p.fits_header_card else ''}

        <div style="text-align: center; margin-top: 30px; font-size: 11px; color: #64748b; font-family: monospace;">
            NASA Space Apps Challenge 2026 — Planet X and SPHEREx | Powered by SKYTRACE AI
        </div>
    </div>
</body>
</html>"""
        return html_doc
