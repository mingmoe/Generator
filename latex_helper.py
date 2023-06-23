import subprocess
import shutil
import os
from typing import List, Optional
from . import shared
import time

from aqt.utils import showInfo, qconnect


def get_latexmk_path() -> str:
    p = shutil.which("latexmk")

    if p is None:
        raise RuntimeError("failed to find xelatex compiler")

    return p


def run_latexmk_for_xelatex(file: str, command, debug: bool) -> Optional[str]:
    file = os.path.abspath(file)
    args = [get_latexmk_path(), "-pdf", "-xelatex", "-file-line-error",
            "-halt-on-error", "-interaction=nonstopmode"]
    args.extend(command)
    args.append(file)
    showInfo(str(args))
    if debug:
        process = subprocess.Popen(args, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=shared.root_dir)
    else:
        process = subprocess.Popen(args, stdout=None, stderr=None,
                                   cwd=shared.root_dir)

    stdout = ""
    stderr = ""
    if debug:
        while process.poll() is None:
            stdout += process.stdout.read()
            stderr += process.stderr.read()

            time.sleep(1)

        stdout += process.stdout.read()
        stderr += process.stderr.read()
    else:
        process.wait()

    if process.returncode != 0:
        if debug:
            return "ERROR\nSTDOUT:\n" + stdout + \
                "\nSTDERR:\n" + stderr
        else:
            return "please open the debug mode"
    return None


def str_to_latex_str(string: str) -> str:
    return string.replace('#', '\\#{}').replace('$', '\\${}') \
        .replace('%', '\\%{}').replace('&', '\\&{}').replace('{', '\\{{}').replace('}', '\\}{}') \
        .replace('_', '\\_{}').replace('^', '\\^{}').replace('~', '\\~{}').replace('\\', '\\textbackslash{}')


class LaTeXDocument:
    template_file: str = os.path.join(shared.root_dir, "template.tex")
    """
    模板文件
    """

    source_file: str = os.path.join(shared.root_dir, "input.tex")
    """
    源文件
    """

    output_dir: str = os.path.join(shared.root_dir, "output/")
    """
    输出文件夹
    """

    pages: List[str] = []
    """
    每一页的源代码
    """

    first_source: str

    debug: bool

    def build(self) -> Optional[str]:
        with open(self.source_file, mode="w", encoding="utf-8") as f:
            f.truncate(0)
            f.write(self.first_source)
            f.write('\n')
            for page in self.pages:
                f.write(page)
                f.write("\n\\clearpage\n")

        command = [f"-output-directory={self.output_dir}"]

        return run_latexmk_for_xelatex(
            self.template_file,
            command,
            self.debug
        )

    def get_output_pdf_path(self) -> str:
        return os.path.join(self.output_dir, os.path.basename(self.template_file.replace(".tex", ".pdf")))
