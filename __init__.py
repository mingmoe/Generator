import sys
import os
from typing import List
from datetime import datetime
import tempfile

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependence"))

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *

config = mw.addonManager.getConfig(__name__)

from docx import Document
from docx.shared import Inches
from PIL import Image
from PIL.Image import Resampling


def generate_docx(files: List[str]) -> None:
    document = Document()
    document.add_heading(f"The Economist - {datetime.today().strftime('%Y-%m-%d')}", 0)

    # 创建缩率图
    with tempfile.TemporaryDirectory() as tmpdirn:
        for file in files:
            with Image.open(file) as img:
                img.thumbnail((512, 512),Resampling.HAMMING)
                img.save(os.path.join(tmpdirn, os.path.basename(file)) + ".png", "PNG")

            document.add_picture(os.path.join(tmpdirn, os.path.basename(file)) + ".png")
            document.add_paragraph("\n\n\n")

    # 设置页边距
    document.sections[0].left_margin = (Inches(0.25))
    document.sections[0].right_margin = (Inches(0.25))
    document.sections[0].top_margin = (Inches(0.25))
    document.sections[0].bottom_margin = (Inches(0.25))

    # 添加页眉
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    header = document.sections[0].header
    paragraph = header.paragraphs[0]

    # 设置文字
    run = paragraph.add_run()
    font = run.font
    font.italic = True
    font.size = Pt(12)
    paragraph.text = "大明酱的Brainstorm.  Powered by MingMoe. With Love."
    paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 保存
    document.save((os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.docx")))
    os.startfile((os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.docx")))


def export_docx() -> None:
    found = mw.col.find_notes(f"{config['check_option']} tag:{config['tag']}")

    image_lists: List[str] = []

    for note_id in found:
        note = mw.col.get_note(note_id)
        files = mw.col.media.files_in_str(note.mid, note[config['field']])
        for file in files:
            file = mw.col.media.escape_media_filenames(file, True)
            image_lists.append(os.path.join(mw.col.media.dir(), file))

    showInfo(f"get cards: {len(found)}")
    generate_docx(image_lists)


action = QAction("export cards to docx", mw)

qconnect(action.triggered, export_docx)

mw.form.menuTools.addAction(action)
