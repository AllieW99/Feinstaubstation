from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


def create_pdf(date, datatype, minimum, maximum, average, graph):
    pdf = canvas.Canvas(date + "_" + datatype + ".pdf")

    my_text = "Minimum: " + minimum + "\nMaximum: " + maximum + "\nAverage: " + average
    textobject = pdf.beginText(2 * cm, 22 * cm)
    for line in my_text.splitlines(False):
        textobject.textLine(line.rstrip())

    pdf.setFontSize(20)
    pdf.drawCentredString(x=10.5 * cm, y=28 * cm, text=datatype + " " + date)
    pdf.setFontSize(12)
    pdf.drawText(textobject)
    pdf.drawInlineImage(image=graph, x=6 * cm, y=18 * cm)
    pdf.save()
