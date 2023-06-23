
import subprocess
import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
dependence = os.path.join(current,"dependence")

# subprocess.run(["pip","install",f"--target={dependence}","python-docx","Pillow"])
subprocess.run(['python','-m','pip','install','--upgrade','pip'])
# subprocess.run(["pip","install",f"--prefix={dependence}",'lxml',"python-docx","Pillow"])
subprocess.run(["pip","install",f"--target={dependence}",'lxml',"python-docx","Pillow","munch","imgkit"])

print("------------ note ------------")
print("you need to install https://wkhtmltopdf.org/ in your system!")
print("you may need xvfb ,see https://pypi.org/project/imgkit/")
print("you need to install https://www.tug.org/texlive/ in your system!")
