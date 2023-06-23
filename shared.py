import os
import sys
from typing import List, Optional
import shutil

root_dir = os.path.dirname(os.path.abspath(__file__))
dependence_dir = os.path.join(root_dir, "dependence")
output_dir = os.path.join(root_dir, "output")


def inject_dependence() -> None:
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dependence"))


class LaTeXItem:
    image_path: str
    """
    要插入的图像路径
    """

    pdf_path: Optional[str]
    """
    要提供的pdf路径
    """




class DeckConfig:
    name: str

    search_option: str
    """
    搜索所需要的卡片的搜索设置
    """

    found_image_at_field: str = "正面"

    found_string_at_field: str = "知识笔记"

    image_x: int = 561
    """
    see PIL.image.thumbnail
    """

    image_y: int = 700
    """
    see PIL.image.thumbnail
    """


class Config:
    decks: List[DeckConfig]


def create_dir():
    from pathlib import Path

    Path(output_dir).mkdir(parents=True, exist_ok=True)


def clear_output_dir():
    try:
        shutil.rmtree(output_dir, ignore_errors=True)
    except BaseException:
        pass
    finally:
        create_dir()


clear_output_dir()

pre_html_translated = False

prehtml = """
<!DOCTYPE html>
<html>
<head>
<!-- MathJax Support -->
<script>
MathJax = {
  // configuration here, if needed
};
</script>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>

<script id="MathJax-script">
<MATHJAX>
</script>


<meta charset="utf-8">
<title>Generated Html</title>
</head>
<body>

<REPLACED>

<script>
MathJax.startup.document.state(0);
MathJax.texReset();
MathJax.typeset();
</script>

</body>
</html>
"""

def translate_perhtml():
    global pre_html_translated
    global prehtml
    if not pre_html_translated:
        pre_html_translated = True

    with open(os.path.join(root_dir,"mathjax.js"),encoding="utf-8") as f:
        js = f.read()
        prehtml = prehtml.replace("<MATHJAX>",js)


translate_perhtml()

def merge_html(html:str) -> str:
    global prehtml
    return prehtml.replace("<REPLACED>",html)