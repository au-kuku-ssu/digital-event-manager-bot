pip install reportlab

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import blue, black
import os
import textwrap

# Для выравнивания по ширене
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

def register_fonts():
    # Путь к файлу Times New Roman
    # Обычный
    font_path = "./fonts/times.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("Файл шрифта 'times.ttf' не найден.")

    pdfmetrics.registerFont(TTFont('TimesNewRoman', font_path))

    # Курсив
    font_path = "./fonts/timesi.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("Файл шрифта 'timesi.ttf' не найден.")

    pdfmetrics.registerFont(TTFont('TimesNewRomanItalic', font_path))


    # Жирный
    font_path = "./fonts/timesbd.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("Файл шрифта 'timesbd.ttf' не найден.")

    pdfmetrics.registerFont(TTFont('TimesNewRomanBold', font_path))

    # Жирный курсив
    font_path = "./fonts/timesbi.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("Файл шрифта 'timesbi.ttf' не найден.")

    pdfmetrics.registerFont(TTFont('TimesNewRomanBoldItalic', font_path))



def Write_Session(c, text, x, y, max_width, line_height):
    width, height = A4
    lines = text.strip().split('\n')

    styles = {
        "bold_blue": ParagraphStyle(name="BoldBlue", fontName="TimesNewRomanBold", fontSize=14, leading=16, alignment=TA_JUSTIFY, textColor=blue),
        "italic": ParagraphStyle( name="Italic", fontName="TimesNewRomanItalic", fontSize=14, leading=16, alignment=TA_JUSTIFY, textColor=blue),
        "bolditalic": ParagraphStyle( name="BoldItalic", fontName="TimesNewRomanBoldItalic", fontSize=14, leading=16, alignment=TA_JUSTIFY, textColor=blue)
    }

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        if i == 0:
            style = styles["bold_blue"]
            para = Paragraph(f'Poster Session: {line}', style)
        elif i == 1:
            style = styles["bold_blue"]
            para = Paragraph(line, style)
        elif i == 2:
            style = styles["bold_blue"]
            para = Paragraph(f'Time-limit: {line}', style)
        elif i == 3:
            style = styles["italic"]
            para = Paragraph(line, style)
        else:
            if '(' in line and ')' in line:
              name = line[:line.index('(')].strip()
              parens = line[line.index('('):].strip()
              # Жирный курсив для имени, обычный курсив для скобок
              text_formatted = f'<font name="TimesNewRomanBoldItalic">{name}</font> <font name="TimesNewRomanItalic">{parens}</font>'
            else:
              text_formatted = f'<font name="TimesNewRomanBoldItalic">{line}</font>'
            para = Paragraph(text_formatted, styles["bolditalic"])

        w, h = para.wrap(max_width, y)
        if y - h < 30 * mm:
            c.showPage()
            y = height - 30 * mm
        para.drawOn(c, x, y - h)
        y -= h + 2 * mm

    return y

def Speakers_in_Session(c, text, x, y, max_width, line_height):
    from reportlab.lib.units import mm
    c.setFillColor(black)

    # Определяем стили
    styles = {
        "names": ParagraphStyle(name="Names", fontName="TimesNewRomanBold", fontSize=14, leading=16, alignment=TA_JUSTIFY),
        "language": ParagraphStyle(name="Language", fontName="TimesNewRomanItalic", fontSize=14, leading=16, alignment=TA_JUSTIFY),
        "description": ParagraphStyle(name="Description", fontName="TimesNewRoman", fontSize=12, leading=14, alignment=TA_JUSTIFY),
        "advisors": ParagraphStyle(name="Advisors", fontName="TimesNewRomanItalic", fontSize=10, leading=12, alignment=TA_JUSTIFY),
    }

    width, height = A4

    for block in text.strip().split("&&&"):
        lines = block.strip().split("\n")
        if len(lines) < 4:
            continue  # пропускаем неполные блоки

        block_parts = [
            (lines[0], styles["names"]),
            (lines[1], styles["language"]),
            (lines[2], styles["description"]),
            (lines[3], styles["advisors"])
        ]

        for part_text, style in block_parts:
            para = Paragraph(part_text.strip(), style)
            w, h = para.wrap(max_width, y)
            if y - h < 30 * mm:
                c.showPage()
                y = height - 30 * mm
            para.drawOn(c, x, y - h)
            y -= h + 2 * mm  # интервал между параграфами

        y -= 5 * mm  # отступ между блоками

    return y

def List_of_Speakers(c, text, x, y, max_width):
    width, height = A4

    styles = {
        "section": ParagraphStyle(name="Section", fontName="TimesNewRomanBold", fontSize=14, leading=16, alignment=TA_JUSTIFY),
        "item": ParagraphStyle(name="Item", fontName="TimesNewRoman", fontSize=14, leading=18, alignment=TA_JUSTIFY, leftIndent=10),
    }

    blocks = text.strip().split("\n")
    if not blocks:
        return y

    # Первая строка — заголовок секции
    section_title = blocks[0]
    para = Paragraph(f'Секция: {section_title}', styles["section"])
    w, h = para.wrap(max_width, y)
    if y - h < 30 * mm:
        c.showPage()
        y = height - 30 * mm
    para.drawOn(c, x, y - h)
    y -= h + 6 * mm  # Отступ ПОСЛЕ заголовка (пустая строка)

    # Остальные строки — список
    for line in blocks[1:]:
        if not line.strip():  # пропускаем пустые строки
            continue
        bullet = '•'
        para = Paragraph(f'{bullet} {line.strip()}', styles["item"])
        w, h = para.wrap(max_width, y)
        if y - h < 30 * mm:
            c.showPage()
            y = height - 30 * mm
        para.drawOn(c, x, y - h)
        y -= h + 2 * mm

    return y

def create_pdf(event_name, Session_text, Speakers, ListText):
    register_fonts()
    file_name = f"Отчет_{event_name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4


    margin_left = 25 * mm
    margin_top = height - 30 * mm
    line_height = 5 * mm # расстояние между строками
########
    y = Write_Session(
        c,
        Session_text.strip(),
        x=margin_left,
        y=margin_top,
        max_width=width - 2 * margin_left,
        line_height=line_height,
    )

    y -= 10 * mm  # Добавим пустую строку

    y = Speakers_in_Session(
        c,
        Speakers.strip(),
        x=margin_left,
        y=y,
        max_width=width - 2 * margin_left,
        line_height=line_height,
    )
##########
    y -= 10 * mm  # Добавим пустую строку

    y = List_of_Speakers(
    c,
    ListText,
    x=margin_left,
    y=y - 10 * mm,  # Отступ перед списком
    max_width=width - 2 * margin_left,
    )


    c.save()
    print(f"PDF-файл успешно создан: {file_name}")
	
with open("./Session.txt", "r", encoding="utf-8") as f:
  Session_text = f.read()
with open("./Speakers_in_Session.txt", "r", encoding="utf-8") as f:
  Speakers = f.read()
with open("./List_of_Speakers.txt", "r", encoding="utf-8") as f:
    ListText = f.read()

create_pdf("test name", Session_text, Speakers, ListText)
