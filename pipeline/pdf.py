import datetime
import random

from fpdf import FPDF


def generate_pdf(report):
    print("Generating PDF.")
    report_number = random.randint(100, 1000)
    name_list = report.inferences.get("names")
    location_list = report.inferences.get("locations")
    comments = report.post.get_text_evidence()
    contact_list = report.leads
    thread_url = report.post.url
    face_match = report.leads
    num_images = len(report.post.photos)

    locations = ", ".join(location_list)
    names = ", ".join(name_list)
    contact_info = ", ".join(contact_list)

    thread_id = thread_url.split("/")[4]

    if face_match:
        face_match = "Yes"
    else:
        face_match = "No"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "", 13.0)
    pdf.set_line_width(0.0)
    pdf.rect(15.0, 15.0, 170.0, 245.0)
    pdf.set_line_width(0.0)
    pdf.line(100.0, 15.0, 100.0, 57.0)
    pdf.set_font("arial", "B", 14.0)
    pdf.set_xy(140.0, 25.5)
    pdf.cell(ln=0, h=9.5, align="L", w=60.0, txt=f"{report_number}", border=0)
    pdf.set_xy(115.0, 27.5)
    pdf.cell(ln=0, h=5.5, align="L", w=50.0, txt="Report ID:", border=0)
    pdf.set_font("arial", "B", 12.0)
    pdf.set_xy(25.0, 25.5)
    pdf.cell(ln=0, h=10.0, align="L", w=98.0, txt="CONFIDENTIAL REPORT", border=0)
    pdf.set_font("arial", "", 12.0)
    pdf.set_xy(118.0, 40.0)
    pdf.cell(ln=0, h=7.0, align="L", w=60.0, txt="Date:", border=0)
    pdf.set_xy(133.0, 40.0)
    pdf.cell(
        ln=0, h=7.0, align="L", w=40.0, txt=f"{str(datetime.date.today())}", border=0
    )
    pdf.set_font("times", "", 8.0)
    pdf.set_xy(25.0, 38)
    pdf.cell(
        ln=0,
        h=7.0,
        align="L",
        w=40.0,
        txt="This automatically generated report details a potential",
        border=0,
    )
    pdf.set_xy(25.0, 42)
    pdf.cell(
        ln=0,
        h=7.0,
        align="L",
        w=40.0,
        txt="illegal and non-consensual uploading of intimate photos.",
        border=0,
    )
    pdf.set_xy(25.0, 46)
    pdf.cell(
        ln=0,
        h=7.0,
        align="L",
        w=40.0,
        txt="It is intended as evidence or use for law enforcement",
        border=0,
    )
    pdf.set_line_width(0.0)
    pdf.line(15.0, 57.0, 185.0, 57.0)
    pdf.set_font("times", "B", 13.0)
    pdf.set_xy(66.0, 59.0)
    pdf.cell(ln=0, h=6.0, align="L", w=13.0, txt="Extracted Information:", border=0)
    pdf.set_font("times", "", 12.0)
    pdf.set_xy(17.0, 64.0)
    pdf.cell(ln=0, h=6.0, align="L", w=18.0, txt="Names(s):", border=0)
    pdf.set_xy(38.0, 64.0)
    pdf.set_font("times", "", 9.0)
    pdf.cell(ln=0, h=6.0, align="L", w=125.0, txt=f"{names}", border=0)
    pdf.set_font("times", "", 12.0)
    pdf.set_xy(17.0, 69.0)
    pdf.cell(ln=0, h=6.0, align="L", w=18.0, txt="Location(s):", border=0)
    pdf.set_xy(38.0, 69.0)
    pdf.set_font("times", "", 9.0)
    pdf.cell(ln=0, h=6.0, align="L", w=80.0, txt=f"{locations}", border=0)
    pdf.set_font("times", "", 12.0)
    pdf.set_xy(115.0, 69.0)
    pdf.cell(ln=0, h=6.0, align="L", w=18.0, txt="Contact Info: ", border=0)
    pdf.set_font("times", "", 9.0)
    pdf.set_xy(140.0, 69.0)
    pdf.cell(ln=0, h=6.0, align="L", w=42.0, txt=f"{contact_info}", border=0)
    pdf.set_line_width(0.0)
    pdf.line(15.0, 77.0, 185.0, 77.0)
    pdf.set_xy(17.0, 80.0)
    pdf.set_font("times", "B", 12.0)
    pdf.cell(ln=0, h=5.0, align="L", w=15.0, txt="Thread ID:", border=0)
    pdf.set_xy(40.0, 80.0)
    pdf.set_font("times", "", 9.0)
    pdf.cell(ln=0, h=5.0, align="L", w=70.0, txt=f"{thread_id}", border=0)
    pdf.set_xy(125.0, 80.0)
    pdf.set_font("times", "B", 12.0)
    pdf.cell(ln=0, h=5.0, align="L", w=20.0, txt="Website:", border=0)
    pdf.set_xy(142.0, 80.0)
    pdf.set_font("times", "", 9.0)
    pdf.cell(ln=0, h=5.0, align="L", w=40.0, txt=f"{thread_url}", border=0)
    pdf.set_line_width(0.0)
    pdf.line(15.0, 88.0, 185.0, 88.0)
    pdf.set_xy(17.0, 90.0)
    pdf.cell(ln=0, h=5.0, align="L", w=48.0, txt="Face Recognition Match:", border=0)
    pdf.set_xy(55.0, 90.0)
    pdf.cell(ln=0, h=5.0, align="L", w=20.0, txt=f"{face_match}", border=0)
    pdf.set_xy(125.0, 90.0)
    pdf.cell(ln=0, h=5.0, align="L", w=43.0, txt="# images:", border=0)
    pdf.set_xy(140.0, 90.0)
    pdf.cell(ln=0, h=5.0, align="L", w=20.0, txt=f"{num_images}", border=0)
    pdf.set_line_width(0.0)
    pdf.line(15.0, 95.0, 185.0, 95.0)
    pdf.set_line_width(0.0)
    pdf.line(155.0, 95.0, 155.0, 230.0)
    pdf.set_xy(20.0, 97.0)
    pdf.set_font("times", "B", 11.0)
    pdf.cell(ln=0, h=5.0, align="L", w=125.0, txt="Text Evidence:", border=0)
    pdf.set_xy(155.0, 97.0)
    pdf.cell(ln=0, h=5.0, align="R", w=20.0, txt="Notes", border=0)
    pdf.set_line_width(0.0)
    pdf.line(15.0, 102.0, 185.0, 102.0)

    counter = 0
    while comments and counter < 110:
        line = comments[:55]
        pdf.set_xy(20.0, 103.0 + counter)
        pdf.cell(ln=0, h=7.0, align="L", w=25.0, txt=f"{line}", border=0)
        comments = comments[55:]
        counter += 4

    pdf.set_line_width(0.0)
    pdf.line(15.0, 230.0, 185.0, 230.0)
    pdf.set_font("arial", "B", 12.0)
    pdf.set_xy(120.0, 235.0)
    pdf.cell(ln=0, h=9.0, align="R", w=25.0, txt="Report Processed:", border=0)
    pdf.set_xy(120.0, 243.0)
    pdf.rect(155.0, 236.0, 7.0, 7.0)
    pdf.cell(ln=0, h=9.0, align="R", w=25.0, txt="Flag for Review:", border=0)
    pdf.set_xy(120.0, 251.0)
    pdf.rect(155.0, 244.0, 7.0, 7.0)
    pdf.cell(ln=0, h=9.0, align="R", w=25.0, txt="Victim Notified:", border=0)
    pdf.set_line_width(0.0)
    pdf.rect(155.0, 252.0, 7.0, 7.0)
    pdf.set_font("courier", "", 10.0)
    pdf.set_xy(20.0, 253.0)
    pdf.cell(ln=0, h=7.0, align="L", w=120.0, txt="CONFIDENTIAL", border=0)
    pdf.output(f"../reports/report_{report_number}.pdf", "F")
