"""Optional Word version of a resume-helper HTML document (same content, simple ATS-safe styling).

Usage: python build_docx.py work/resume.html "Out/Jane Doe Resume.docx"
Reads the template structure: h1, .headline, .contact, h2, .role-head (.role-title, .role-org, .dates), li, p.
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Mm


class Walker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.stack, self.buf, self.cls, self.rtl = [], [], [], None, False
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html" and a.get("dir") == "rtl":
            self.rtl = True
        if tag in ("style", "script", "svg", "title"):
            self.skip += 1
            return
        c = a.get("class", "")
        if tag in ("h1", "h2", "li") or (tag == "p" and self.cls is None) or c == "role-head":
            if self.cls is None:
                self.cls = c or tag
                self.buf = []
        if tag == "strong":
            self.buf.append(("b", ""))
        if tag == "span" and c == "dates":
            self.buf.append(("tab", ""))
        if tag == "a" and self.cls == "contact" and self.buf:
            self.buf.append(("t", "  |  "))
        self.stack.append((tag, c))

    def handle_endtag(self, tag):
        if tag in ("style", "script", "svg", "title"):
            self.skip -= 1
            return
        if not self.stack:
            return
        t, c = self.stack.pop()
        if tag == "strong":
            self.buf.append(("/b", ""))
        if self.cls and ((c or t) == self.cls) and t in ("h1", "h2", "li", "p", "div"):
            self.blocks.append((self.cls, self.buf))
            self.cls, self.buf = None, []

    def handle_data(self, data):
        if self.skip or self.cls is None:
            return
        if data.strip() or (self.buf and data == " "):
            self.buf.append(("t", re.sub(r"\s+", " ", data)))


def main():
    src, out = sys.argv[1], sys.argv[2]
    w = Walker()
    w.feed(pathlib.Path(src).read_text(encoding="utf-8"))
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(16)
    sec.top_margin = sec.bottom_margin = Mm(13)
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Arial", Pt(10)
    st.paragraph_format.space_after = Pt(1)
    accent = RGBColor(0x1A, 0x1A, 0x1A)

    for cls, parts in w.blocks:
        para = doc.add_paragraph(style="List Bullet" if cls == "li" else None)
        if w.rtl:
            para.paragraph_format.element.get_or_add_pPr().append(para.paragraph_format.element.makeelement(qn("w:bidi"), {}))
        if cls == "role-head":
            para.paragraph_format.tab_stops.add_tab_stop(Mm(178), WD_TAB_ALIGNMENT.RIGHT)
            para.paragraph_format.space_before = Pt(4)
        bold = cls in ("h1", "h2", "headline", "role-head")
        for kind, val in parts:
            if kind == "b":
                bold = True
            elif kind == "/b":
                bold = cls in ("h1", "h2", "headline")
            elif kind == "tab":
                para.add_run("\t")
                bold = False
            else:
                r = para.add_run(val)
                r.bold = bold
                if w.rtl:
                    r.font.rtl = True
                if cls == "h1":
                    r.font.size, r.font.color.rgb = Pt(18), accent
                elif cls == "h2":
                    r.font.size = Pt(11)
                    r.text = r.text.upper()
        if cls == "h2":
            para.paragraph_format.space_before = Pt(8)
    doc.save(out)
    print(f"OK -> {out}")


if __name__ == "__main__":
    main()
