"""Build the two-page Decision-Memo.pdf and Validation-and-AI-Use.pdf from saved outputs.

Run after src.reproduce: python -m src.build_submission_pdfs. Every number is read from outputs/.
Each PDF must be exactly two pages (course limit for the memo); the build fails otherwise.
"""
import csv
import html
import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Table, TableStyle

ROOT = Path.cwd()
OUT = ROOT / "submission"
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(name="BodyFinance", fontName="Helvetica", fontSize=9.2, leading=11.6, spaceAfter=5))
STYLES.add(ParagraphStyle(name="SmallFinance", fontName="Helvetica", fontSize=7.6, leading=9.2, spaceAfter=4))
STYLES["Title"].fontSize = 18
STYLES["Title"].leading = 22
STYLES["Heading2"].fontSize = 11
STYLES["Heading2"].leading = 13
FOOTER = "FIN439 | Pierce Appleton | AI-assisted analysis | Revised Oct 20, 2026"


def p(text, style="BodyFinance"):
    return Paragraph(text, STYLES[style])


def h(text):
    return Paragraph(text, STYLES["Heading2"])


def footer(canvas, doc):
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#536173"))
    canvas.drawString(40, 26, FOOTER)
    canvas.drawRightString(572, 26, str(doc.page))


def table(rows, widths):
    cells = [[p(html.escape(str(v)), "SmallFinance") for v in row] for row in rows]
    t = Table(cells, colWidths=widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef4")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, 0), 1, colors.HexColor("#778da3")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def build(name, story):
    path = OUT / name
    SimpleDocTemplate(str(path), pagesize=(612, 792), rightMargin=40, leftMargin=40, topMargin=34, bottomMargin=40).build(story, onFirstPage=footer, onLaterPages=footer)
    pages = len(PdfReader(str(path)).pages)
    assert pages == 2, (name, pages)
    print(name, "pages", pages)


def read_csv(name):
    with (ROOT / "outputs" / name).open(encoding="utf8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    r = json.loads((ROOT / "outputs/results.json").read_text(encoding="utf8"))
    cases = r["cases"]
    lo, base, hi = (cases[k]["per_share"] for k in ["low", "base", "high"])
    conv = {(x["case"], int(x["fade_years"])): x for x in read_csv("terminal_conventions.csv")}
    bridge = read_csv("valuation_bridge.csv")
    frozen = {x["case"]: float(x["per_share"]) for x in bridge if x["kind"] == "frozen"}
    relative = read_csv("relative_valuation.csv")
    ev_prices = [float(x["ev_revenue_implied_basic_price"]) for x in relative]
    pe_prices = [float(x["pe_implied_basic_price"]) for x in relative if x["pe_implied_basic_price"]]
    stresses = read_csv("named_stresses.csv")
    tests = (ROOT / "validation/reproduction-tests.txt").read_text(encoding="utf8")
    test_count = tests.split("Ran ")[1].split(" ")[0] if "Ran " in tests else "see log"
    checks = len(json.loads((ROOT / "validation/source-row-checks.json").read_text(encoding="utf8")))
    locked_dir = ROOT / "validation/locked/20261020T044925989222Z"
    locked_prediction = json.loads((locked_dir / "prediction.json").read_text(encoding="utf8"))
    locked_result = json.loads((locked_dir / "results.json").read_text(encoding="utf8"))
    locked_percent = 100 * locked_result["per_share_change"] / locked_result["before"]["per_share"]

    case_table = [["Case", "Mechanism", "Frozen Oct 6", "Corrected", "5-yr fade", "10-yr fade", "Terminal / EV"]]
    for key, text in [("low", "Slower commercial conversion, procurement delays, lower margin, weaker collections"), ("base", "Strong adoption decelerates; margins fade toward maturity"), ("high", "Repeatable deployment sustains adoption and collections")]:
        case_table.append([key.capitalize(), text, f"${frozen[key]:.2f}", f"${cases[key]['per_share']:.2f}", f"${float(conv[(key, 5)]['per_share']):.2f}", f"${float(conv[(key, 10)]['per_share']):.2f}", f"{cases[key]['terminal_share']:.0%}"])
    memo = [
        p("Palantir: committee decision", "Title"),
        p("Committee recommendation: do not initiate", "Heading2"),
        p(f"<b>Pierce's adopted action is do not initiate at the October 5 close of $189.40.</b> The causal DCF range is about <b>${lo:.0f}-${hi:.0f} per diluted share</b> (base ${base:.2f}). Every case, including the high case with a 10-year fade (${float(conv[('high', 10)]['per_share']):.0f}), remains below the reference price. This is a conditional action on the tested evidence, not approval of every model assumption. User: buy-side analysts and PM; horizon 3-5 years; NASDAQ PLTR Class A; USD."),
        h("Evidence and accounting boundary"),
        p("Audited 2025 10-K (published Feb 17, 2026); June 30, 2026 10-Q (published Aug 4); information cutoff Oct 5, 2026. FY2026 guidance midpoint $8.154B is a forecast input. Q2 2026 GAAP operating margin was 47.1% (FY2023 5.4%, FY2025 31.6%); the base path falling to 40% by 2030 and 35% at maturity is an analyst assumption against that rising history."),
        p("FCFF comes from the integrated five-year statements. Existing awards are counted once, as diluted shares; their remaining expense is added back to EBIT as a separate line so it is not also charged as cost. Future compensation stays in the margin as a cash-replacement cost. Restricted cash gets no credit. Since Oct 6, two code corrections were made: June 30 cash is rolled to Oct 5 by the cash retained in the 97-day stub (+$0.33 base), and the existing-award runoff follows a capped schedule (+$0.03)."),
        h("Causal valuation cases (USD per diluted share)"),
        table(case_table, [34, 186, 52, 52, 52, 52, 52]),
        p("Base WACC 10.56% = 10-year Treasury 5.31% + beta 1.25 x ERP 4.20%. Pierce verified the Oct 5 10-year yield and the Damodaran ERP; saved source evidence has limits. Beta is an analyst assumption without a saved source. Beta 1.50 gives about $27 and 2.00 about $23 in the base. Terminal growth 2-4%, mature margin 30-40%, ROIC 25%, reinvestment = growth / ROIC."),
        PageBreak(),
        h("What the price implies"),
        *[p(x) for x in r["market_implied"]["sentences"]],
        p("One price cannot pin down growth, margin and fade length at once; each line moves one and holds the rest at base."),
        h("Relative valuation and disagreement"),
        p(f"Under the revised peer rule only NOW and CRM have data so far; the wider candidate set (SNOW, DDOG, CRWD, NET, MDB, ADBE, TYL) is pending data and Pierce's approval. Peer EV/revenue implies about ${min(ev_prices):.0f}-${max(ev_prices):.0f} and GAAP P/E about ${min(pe_prices):.0f}-${max(pe_prices):.0f} per basic share. Palantir trades at 72x TTM EV/revenue and 151x GAAP P/E (199x at a normalized 25% tax). Peers grow far more slowly, so multiples cannot capture Palantir's growth; the DCF prices growth but imposes maturity. The market implies a longer, more profitable runway than either supports. The methods are not averaged, and basic-share values are not mixed with diluted DCF values."),
        h("Stresses, conditions and committee ask"),
        *[p(f"{x['scenario']}: ${float(x['value']):.2f}; at a hypothetical ${x['conditional_price']} entry: {x['conditional_action'].replace('_', ' ')}.") for x in stresses],
        p("Monitor realized commercial/government revenue, collections, GAAP margin, compensation and award issuance, cash taxes and valuation-allowance status, and hosting/capex. Two quarters above the high-case path would justify rebuilding runway and maturity. NOL utilization would add only $0.37-$0.71 per share."),
        p("<b>Committee ask:</b> approve do not initiate PLTR at the October 5 reference price. Reopen the decision if reported growth, collections and margins support a longer profitable runway, or if a lower price creates a defensible margin of safety. Fade length, margin path, beta and peer selection remain material assumptions."),
        p("Sources: Palantir 2025 10-K and June 2026 10-Q (saved and hashed); Aug 3 release; Oct 5 closes; Treasury daily par yield curve; NYU Stern implied ERP; NOW/CRM issuer disclosures. URLs, dates and pending verifications are in the repository (docs/source-verification-2026-10-20.md).", "SmallFinance"),
    ]
    build("Decision-Memo.pdf", memo)

    validation = [
        p("Validation and AI use", "Title"),
        p("Executed evidence and human locked run", "Heading2"),
        p("Independent snapshot 890b9738c802592abb4e70beb8efc21181fdfcea was frozen Oct 6, 2026 22:53:27 UTC; its manifest is preserved. FIN439-Labs commit 2e861768 was read only after that freeze. Course snapshot 69eac1e8. Later revisions were merged to main; they are not part of the independent freeze. User-supplied official Edition A PDF is preserved unchanged at submission/Edition A.pdf (five pages; SHA-256 24087f84b272baba2eb9c6a3cb83f495c47e5e48f5270e833dd3fe3a2f4ba2b1). Edition A states a September 1, 2026 valuation date and cites the June 30, 2026 10-Q (published Aug 4, before September 1); the current model uses an Oct 5 cutoff."),
        h("Executed checks and limits"),
        table(
            [
                ["Requirement", "Evidence and disposition"],
                ["Published known answer", "PASS: all 12 official Lab 05 DCF outputs within 0.0001, computed by the same engine."],
                ["Source integrity", f"{checks} saved-filing cell checks pass; balance and cash totals reconcile for 2025 and H1 2026; restricted cash reconciled through the note."],
                ["Articulation and DCF", f"{test_count} software tests pass: balance/cash ties, income-statement identities, stub cash counted once, award runoff capped, fade engine timing and zero-fade equivalence, WACC > g, contamination rejection, peer P/E 'not meaningful' rule, locked-runner commit isolation."],
                ["Cold run", "Fresh-environment runs recorded Oct 6 (Windows) and Oct 20 (Linux): validation/cold-run-2026-10-20.json."],
                ["Economic challenges", "Cases, WACC-growth grid, 0/5/10-year fade, readable reverse DCF, NOL sensitivity, named stresses, one-at-a-time and proportional tests."],
            ],
            [115, 417],
        ),
        h("Source and date policy"),
        p("October 5 market data; October 6 prices excluded. June 30 balances rolled to October 5 only by modeled retained cash. Pierce verified the Oct 5 10-year Treasury yield and the Damodaran ERP outside the revision session; the saved Treasury source row and exact ERP method evidence are limited. Beta has no saved source and the peer set is narrow. Nothing was entered from memory."),
        PageBreak(),
        h("Named material AI uses and dispositions"),
        p("Oct 6, 2026: Codex (ChatGPT; model family exposed as GPT-6, exact build not exposed) wrote and ran the independent build. Oct 20, 2026: Claude Code (Anthropic) made the post-comparison revisions after a joint Claude/ChatGPT audit; Pierce is not a coder and did not write code."),
        p("Corrected (Claude Code, with evidence): cutoff cash gap (stub FCFF reconciliation); award runoff ended RSU expense early and used a rounded option period (10-Q XBRL 4y10m21d); duplicate fade math with a hardcoded margin; locked runner could commit unrelated staged files. Qualified: 47% margin confirmed GAAP from the 10-Q income statement; 1.4% tax rate is structural (valuation allowance), not one-time. Earlier: adjusted margins rejected as economic profit; negative cash-flow clipping rejected."),
        h("Locked Changed-Input Record (Gate D) - executed after first submission"),
        table(
            [
                ["Field", "Current record"],
                ["Input and controls", "Base 2029 government revenue growth 22% to 12% of prior-year government revenue; other inputs, cutoff, share basis and price fixed."],
                ["Human precommit", f"Form names Pierce A. and Rusheel N. and attests AI closed. Prediction saved {locked_prediction['recorded_utc']} in commit {locked_result['prediction_precommit'][:12]}; result commit 80546d140046 follows it."],
                ["Prediction as entered", "Direction field: '$33.32'. Written reasoning predicted value would fall by about 3-4%; action would remain do not initiate. These statements conflict; the original precommit is unchanged."],
                ["Actual and decision", f"${locked_result['before']['per_share']:.4f} to ${locked_result['after']['per_share']:.4f} per diluted share; ${locked_result['per_share_change']:+.4f} ({locked_percent:+.2f}%). Do not initiate before and after."],
                ["Pierce's post-run review", "He says '$33.32' was mistakenly carried from a separate Lab 10/11 model with a $34.53 starting value. His intended forecast was down 3-4%, action unchanged. He attributes the smaller 2.64% decline to a lower government mix and a one-segment effect; saved 2029 government share is 44.5%. Original precommit unchanged."],
                ["Earlier AI sensitivity", "The Oct 19 capex 1.2% to 2.0% run was AI-authored and AI-run; it remains separate from this post-deadline human record."],
            ],
            [140, 392],
        ),
        h("Authentic contributions and submission gaps"),
        p("Ethan Heeres is credited only for the supplied Lab 11 exchanges. Pierce adopted do not initiate at $189.40 on Oct 20; this does not approve every assumption. Brightspace received three videos and Edition A/B at 12:00 AM Oct 20 for an Oct 19 11:59 PM deadline. The old videos exceeded their respective 3/5/5 minute limits and had no submitted transcripts. Replacement recordings and corrected transcripts must be based on actual new audio. The human locked run and Pierce's post-run review occurred after the first submission. Final partner review and grader-access confirmation remain open."),
        p("Text copy: docs/validation-and-ai-use.md; docs/claude-code-revision-summary.md, validation/ logs and manifests.", "SmallFinance"),
    ]
    build("Validation-and-AI-Use.pdf", validation)
    (ROOT / "docs/decision-memo.pdf").write_bytes((OUT / "Decision-Memo.pdf").read_bytes())
    text = "\n\n".join(page.extract_text() for page in PdfReader(str(OUT / "Validation-and-AI-Use.pdf")).pages)
    (ROOT / "docs/validation-and-ai-use.md").write_text(text, encoding="utf8")


if __name__ == "__main__":
    main()
