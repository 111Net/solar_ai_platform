import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import sys
import io

# ---------- Inputs ----------
CSV_FILE = sys.argv[1] if len(sys.argv) > 1 else "test_report.csv"
PDF_FILE = sys.argv[2] if len(sys.argv) > 2 else "test_report.pdf"

# ---------- Load CSV ----------
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"CSV file {CSV_FILE} not found. Exiting.")
    sys.exit(1)

# ---------- Summary ----------
total_tests = len(df)
total_users = df['User'].nunique() if 'User' in df.columns else 0
total_success = df['Response'].apply(lambda x: 'error' not in str(x).lower()).sum() if 'Response' in df.columns else 0
total_failures = total_tests - total_success

# ---------- Bar chart: plans per user ----------
plans_df = df[df['Action']=="Create Solar Plan"] if 'Action' in df.columns else pd.DataFrame()
if not plans_df.empty:
    plans_per_user = plans_df.groupby('User').size()
    plt.figure(figsize=(6,3))
    plans_per_user.plot(kind='bar', color='skyblue')
    plt.title("Number of Solar Plans per User")
    plt.ylabel("Plans")
    plt.tight_layout()
    buf_bar = io.BytesIO()
    plt.savefig(buf_bar, format='PNG')
    plt.close()
else:
    buf_bar = None

# ---------- Pie chart: success vs failures ----------
if total_tests > 0:
    plt.figure(figsize=(4,4))
    plt.pie([total_success, total_failures], labels=["Success", "Failure"],
            autopct='%1.1f%%', colors=['green','red'])
    plt.title("Test Outcome")
    buf_pie = io.BytesIO()
    plt.savefig(buf_pie, format='PNG')
    plt.close()
else:
    buf_pie = None

# ---------- Create PDF ----------
c = canvas.Canvas(PDF_FILE, pagesize=letter)
width, height = letter
y = height - inch

# Title
c.setFont("Helvetica-Bold", 16)
c.drawString(inch, y, "Solar SaaS Integration Test Report")
y -= 0.5*inch

# Summary
c.setFont("Helvetica", 12)
c.drawString(inch, y, f"Total Users Tested: {total_users}")
y -= 0.25*inch
c.drawString(inch, y, f"Total Tests: {total_tests}")
y -= 0.25*inch
c.drawString(inch, y, f"Successful Tests: {total_success}")
y -= 0.25*inch
c.drawString(inch, y, f"Failed Tests: {total_failures}")
y -= 0.5*inch

# Draw charts if available
if buf_bar:
    buf_bar.seek(0)
    c.drawImage(ImageReader(buf_bar), inch, y-3*inch, width=6*inch, height=3*inch)
    y -= 3.25*inch

if buf_pie:
    buf_pie.seek(0)
    c.drawImage(ImageReader(buf_pie), inch, y-2.5*inch, width=4*inch, height=4*inch)
    y -= 4.25*inch

# Table header
if not df.empty:
    c.setFont("Helvetica-Bold", 10)
    x_list = [inch, 2.5*inch, 4*inch, 5.5*inch, 7*inch]
    headers = ["Timestamp", "User", "Action", "Input", "Response"]
    for i, h in enumerate(headers):
        c.drawString(x_list[i], y, h)
    y -= 0.2*inch
    c.setFont("Helvetica", 8)
    row_height = 0.18*inch

    # Table rows
    for idx, row in df.iterrows():
        if y < inch:
            c.showPage()
            y = height - inch
        c.drawString(x_list[0], y, str(row.get("Timestamp","")))
        c.drawString(x_list[1], y, str(row.get("User","")))
        c.drawString(x_list[2], y, str(row.get("Action","")))
        c.drawString(x_list[3], y, str(row.get("Input","")))
        response_text = str(row.get("Response",""))
        if len(response_text) > 50:
            response_text = response_text[:47] + "..."
        c.drawString(x_list[4], y, response_text)
        y -= row_height

# Save PDF
c.save()
print(f"PDF report with charts generated: {PDF_FILE}")