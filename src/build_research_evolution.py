"""Assemble the required Research-Evolution.pdf without changing official Edition A."""
import hashlib
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "Research-Evolution.pdf"
EDITION_A = ROOT / "submission" / "Edition A.pdf"
EDITION_B_SOURCE = ROOT / "docs" / "research-evolution-edition-b.md"
EXPECTED_A_HASH = "24087f84b272baba2eb9c6a3cb83f495c47e5e48f5270e833dd3fe3a2f4ba2b1"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="FinanceBody", fontName="Helvetica", fontSize=9.2, leading=12.5, spaceAfter=7))
styles.add(ParagraphStyle(name="FinanceSmall", fontName="Helvetica", fontSize=8, leading=10.4, spaceAfter=5))
styles["Title"].fontSize = 17
styles["Title"].leading = 21
styles["Heading2"].fontSize = 11
styles["Heading2"].leading = 14


def para(text, style="FinanceBody"):
    return Paragraph(text, styles[style])


def page(canvas, doc):
    canvas.setFillColor(colors.HexColor("#536173"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(42, 25, "FIN439 | Pierce Appleton | Research evolution | Revised October 20, 2026")
    canvas.drawRightString(570, 25, str(doc.page))


def to_pdf(story):
    stream = BytesIO()
    SimpleDocTemplate(stream, pagesize=(612, 792), leftMargin=42, rightMargin=42, topMargin=38, bottomMargin=44).build(story, onFirstPage=page, onLaterPages=page)
    stream.seek(0)
    return PdfReader(stream)


def markdown_story(path):
    result = []
    for raw in path.read_text(encoding="utf8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            result.append(para(line[2:], "Title"))
        elif line.startswith("## "):
            result.append(para(line[3:], "Heading2"))
        else:
            import html
            import re
            escaped = html.escape(line)
            escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
            escaped = re.sub(r"\*(.+?)\*", r"<i>\1</i>", escaped)
            escaped = re.sub(r"`(.+?)`", r"\1", escaped)
            result.append(para(escaped))
    return result


def main():
    digest = hashlib.sha256(EDITION_A.read_bytes()).hexdigest()
    if digest != EXPECTED_A_HASH:
        raise ValueError("Edition A hash changed; refusing to assemble")
    a_reader = PdfReader(str(EDITION_A))
    if len(a_reader.pages) != 5:
        raise ValueError("Expected five unchanged Edition A pages")

    addendum = to_pdf([
        para("Dated correction and revision addendum", "Title"),
        para("October 20, 2026 | Follows the five unchanged Edition A pages"),
        para("The Edition B PDF uploaded with the first Project 1 submission incorrectly said Edition A's September 1, 2026 valuation date preceded publication of the June 30, 2026 Form 10-Q. The 10-Q was published August 4, 2026, so September 1 followed it. This revision corrects that date-order statement. The submitted PDF is preserved separately as Edition B.pdf."),
        para("The first uploaded Edition B used a watch/defer portfolio label. On October 20, Pierce explicitly adopted the current action <b>do not initiate at the October 5 reference close of $189.40</b>. The revised Edition B following this page uses that action. The valuation date and information cutoff remain October 5; the October 20 adoption date describes the human decision, not new market information."),
        para("Edition A has not been modified. Its SHA-256 is " + EXPECTED_A_HASH + ". The independent October 6 code snapshot remains preserved at commit 890b973. Later corrections and AI use are disclosed in the separate validation record."),
    ])

    evidence_rows = [
        ["Edition A position or question", "Post-checkpoint evidence or method", "Effect on current action"],
        ["Watch/defer; insufficient margin of safety", "Integrated FCFF base $30.12; low/high $16.66/$65.91 versus $189.40", "Pierce adopted do not initiate; no position"],
        ["Can growth support the price?", "Revenue drivers, 0/5/10-year maturity fades and reverse DCF", "Even high case with 10-year fade stays below price; longer runway requires new evidence"],
        ["Cash, taxes and SBC dilution", "Restricted cash excluded; cash rolled to cutoff; NOL sensitivity; existing awards counted in share bridge", "Avoid overstating attributable equity or mixing accounting bases"],
        ["What would reverse the view?", "Reported segment growth, collections, margins, compensation, hosting needs and entry price", "Rebuild analysis if sustained operating evidence or a lower price changes margin of safety"],
    ]
    evidence_table = Table([[para(v, "FinanceSmall") for v in row] for row in evidence_rows], colWidths=[138, 205, 185], repeatRows=1)
    evidence_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.HexColor("#778da3")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    evidence = to_pdf([
        para("A-to-B evidence map", "Title"),
        para("The unchanged Edition A is the baseline; later code and valuation changes do not retroactively alter it."),
        evidence_table,
        Spacer(1, 12),
        para("No-material-change statement", "Heading2"),
        para("The immediate trade remains no position. The current do-not-initiate label states the action more directly than Edition A's watch/defer posture. The model's numerical values are post-checkpoint analyses, not values assigned to Edition A. Source and assumption limits remain in the decision memo and validation record."),
    ])
    revised_b = to_pdf(markdown_story(EDITION_B_SOURCE))
    writer = PdfWriter()
    for reader in (a_reader, addendum, revised_b, evidence):
        for source_page in reader.pages:
            writer.add_page(source_page)
    writer.add_metadata({"/Title": "FIN439 Research Evolution - Edition A and revised Edition B", "/Author": "Pierce Appleton"})
    with OUT.open("wb") as stream:
        writer.write(stream)
    if hashlib.sha256(EDITION_A.read_bytes()).hexdigest() != EXPECTED_A_HASH:
        raise ValueError("Edition A changed during assembly")
    print(OUT, "pages", len(PdfReader(str(OUT)).pages))


if __name__ == "__main__":
    main()
