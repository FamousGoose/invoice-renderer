
from reportlab.pdfgen.canvas import Canvas

def drawText(c: Canvas, text: str, x: float, y: float, font_size: int = 12, font: str = "Helvetica") -> None:
    c.setFont("Helvetica", font_size)
    c.drawString(x, y, text)

def drawCentredText(c: Canvas, text: str, x: float, y: float, font_size: int = 12, font: str = "Helvetica") -> None:
    c.setFont("Helvetica", font_size)
    c.drawCentredString(x, y, text)