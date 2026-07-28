from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def build_pdf(case: dict) -> bytes:
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("METBO Shield", styles["Title"]),
        Paragraph("Email Threat Investigation Report", styles["Heading2"]),
        Spacer(1,12),
        Paragraph(f"<b>Case ID:</b> {case.get('case_id','')}", styles["BodyText"]),
        Paragraph(f"<b>Analyst:</b> {case.get('analyst','')}", styles["BodyText"]),
        Paragraph(f"<b>Hybrid Score:</b> {case.get('hybrid_score',0)}/100", styles["BodyText"]),
        Paragraph(f"<b>Classification:</b> {case.get('classification','')}", styles["BodyText"]),
        Spacer(1,12),
    ]
    rows = [["Category","Severity","Evidence","Points"]]
    for f in case.get("findings",[]):
        rows.append([f.get("category",""),f.get("severity",""),f.get("evidence",""),str(f.get("points",0))])
    table = Table(rows, colWidths=[70,60,330,45], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#263238")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),.5,colors.grey),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("FONTSIZE",(0,0),(-1,-1),8),
    ]))
    story.append(table)
    doc.build(story)
    return output.getvalue()
