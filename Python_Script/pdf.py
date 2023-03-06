from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


def create_pdf(date, datatype, minimum, maximum, average):
    pdf = canvas.Canvas(date + "_" + datatype + ".pdf")
    my_text = "Minimum: " + minimum + "\nMaximum: " + maximum + "\nAverage: " + average
    textobject = pdf.beginText(2 * cm, 29.7 * cm - 2 * cm)
    for line in my_text.splitlines(False):
        textobject.textLine(line.rstrip())
    # pdf.drawCentredString(x=100, y=100, text=datatype)
    pdf.drawText(textobject)
    pdf.save()
