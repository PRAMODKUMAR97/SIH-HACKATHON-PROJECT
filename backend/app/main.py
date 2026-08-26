from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import date
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from .demo_data import DETECTIONS, boundary_geojson

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "frontend"
EXPORTS = ROOT / "exports"
EXPORTS.mkdir(exist_ok=True)
app = FastAPI(title="KHANAN-NETRA", version="0.1.0")

def filtered(status: str | None = None, risk: str | None = None, min_confidence: float = 0, min_area: float = 0):
    rows = DETECTIONS
    # Browsers can expose window.status, so accept an old UI's undefined value
    # as the same as the default "all statuses" filter.
    if status and status not in ("ALL", "undefined"): rows = [x for x in rows if status in x["status"]]
    if risk and risk != "ALL": rows = [x for x in rows if x["risk_level"] == risk]
    return [x for x in rows if x["probability"] >= min_confidence and x["area_ha"] >= min_area]

@app.get("/api/detections")
def detections(status: str | None = None, risk: str | None = None, min_confidence: float = 0, min_area: float = 0):
    return {"demo": True, "items": filtered(status, risk, min_confidence, min_area)}

@app.get("/api/summary")
def summary():
    rows = DETECTIONS
    illegal = [x for x in rows if not x["status"].startswith("LEGAL")]
    return {"demo": True, "monitored_area_km2": 382, "total":len(rows), "high":sum(x["risk_level"]=="HIGH" for x in rows), "legal":sum(x["status"].startswith("LEGAL") for x in rows), "suspicious":len(illegal), "area":round(sum(x["area_ha"] for x in rows),1), "risk_score":round(sum(x["risk"] for x in rows)/len(rows))}

@app.get("/api/boundaries")
def boundaries(): return boundary_geojson()

@app.get("/api/detections/{detection_id}")
def detail(detection_id: str):
    for x in DETECTIONS:
        if x["id"] == detection_id:
            x = dict(x)
            x["explanation"] = f"Mining probability: {x['probability']:.0%}. Surface change: {x['change_db']} dB. Risk classification: {x['risk_level']}. This is AI-supported DEMO DATA, requiring field verification; it is not a legal judgment."
            return x
    raise HTTPException(404, "Detection not found")

def selection(ids: str | None):
    wanted = set(ids.split(",")) if ids else {x["id"] for x in DETECTIONS}
    return [x for x in DETECTIONS if x["id"] in wanted]

@app.get("/api/export/kml")
def kml(ids: str | None = None):
    body = "".join(f"<Placemark><name>{x['id']}</name><description>{escape(x['status'])}; risk {x['risk']}; confidence {x['probability']:.0%}; DEMO DATA</description><Point><coordinates>{x['longitude']},{x['latitude']},0</coordinates></Point></Placemark>" for x in selection(ids))
    return Response(f'<?xml version="1.0"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>KHANAN-NETRA DEMO</name>{body}</Document></kml>', media_type="application/vnd.google-earth.kml+xml", headers={"Content-Disposition":"attachment; filename=khanan-netra-demo.kml"})

@app.get("/api/export/gpx")
def gpx(ids: str | None = None):
    body = "".join(f'<wpt lat="{x["latitude"]}" lon="{x["longitude"]}"><name>{x["id"]}</name><desc>Risk {x["risk"]}; {escape(x["status"])}</desc></wpt>' for x in selection(ids))
    return Response(f'<?xml version="1.0"?><gpx version="1.1" creator="KHANAN-NETRA">{body}</gpx>', media_type="application/gpx+xml", headers={"Content-Disposition":"attachment; filename=khanan-netra-demo.gpx"})

@app.get("/api/report")
def report(ids: str | None = None):
    rows = selection(ids); path = EXPORTS / "khanan-netra-demo-report.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4); styles = getSampleStyleSheet(); story=[]
    story += [Paragraph("KHANAN-NETRA", styles["Title"]), Paragraph("AI-Powered Satellite Mining Intelligence & Surveillance", styles["Heading2"]), Paragraph(f"DEMO DATA — AI-generated monitoring/evidence-support report — {date.today().isoformat()}", styles["BodyText"]), Spacer(1,12)]
    story.append(Paragraph(f"Selected detections: {len(rows)} | High-risk: {sum(x['risk_level']=='HIGH' for x in rows)} | Estimated area: {sum(x['area_ha'] for x in rows):.1f} ha", styles["BodyText"])); story.append(Spacer(1,12))
    data=[["ID","Coordinates","Area ha","Probability","Status","Risk"]] + [[x["id"],f"{x['latitude']:.4f}, {x['longitude']:.4f}",x["area_ha"],f"{x['probability']:.0%}",x["status"],x["risk"]] for x in rows[:15]]
    t=Table(data, repeatRows=1, colWidths=[66,90,48,58,150,38]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#12304a")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.3,colors.grey),("FONTSIZE",(0,0),(-1,-1),7),("VALIGN",(0,0),(-1,-1),"TOP")]))
    story += [t, Spacer(1,12), Paragraph("Recommendation: high-risk locations require field verification. This report does not determine legal liability and all observations are synthetic demonstration data.", styles["BodyText"])]
    doc.build(story); return FileResponse(path, media_type="application/pdf", filename=path.name)

app.mount("/", StaticFiles(directory=STATIC, html=True), name="frontend")
