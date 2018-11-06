from distutils.core import setup
import re

def parse_pipfile():
    with open("Pipfile","r") as file:
        pipenvfile=file.read().replace("\"","").replace("\'", '')
    # packages_re = re.compile(r"\[\bpackages\b\][+-=*\"a-zA-z0-9]*") #?!(\[\w+\])
    packages_re = re.compile(r"\[\w+\]")
    res = packages_re.findall(pipenvfile)
    results = []
    for r in res:
        a = re.search("{}".format(r.replace("[", "\[").replace("]", "\]")), pipenvfile)
        results.append(a)
    results = sorted(results, key=lambda a: a.span(0)[0])
    packages_span = [0,0]
    for i, res in enumerate(results):
        if "packages" in res.group(0):
            if len(results) > i:
                packages_span = [res.span(0)[1],results[i+1].span(0)[0]]
            break
    package_re = re.compile(r".+(?=\s\=)")
    return package_re.findall(pipenvfile[packages_span[0]:packages_span[1]])

setup(
    name="TapasFlashTool",
    version="0.1",
    packages=["TapasFlashTool",],
    author = "Stefan Steinmueller",
    author_email = "stefan.steinmueller@siemens.com",
    install_requires=parse_pipfile(),
    package_data={"":["*.py", "*.md", "*.txt"]}
)

