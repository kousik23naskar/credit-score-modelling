from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    Returns a list of requirements from a given file
    '''
    with open(file_path) as file:
        requirements = [
            line.strip()
            for line in file.readlines()
            if line.strip() and line.strip() != HYPEN_E_DOT
        ]
    return requirements

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.1.0"
GIT_REPO_NAME = "credit-score-modelling"
GIT_REPO_USER_NAME = "kousik23naskar"
AUTHOR_USER_NAME = "Kousik Naskar"
SRC_REPO = "credit_score_modelling_with_optbinning"
AUTHOR_EMAIL = "kousik23naskar@gmail.com"

setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for Credit Scorecard generation using OptBinning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{GIT_REPO_USER_NAME}/{GIT_REPO_NAME}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=get_requirements('requirements.txt'),
    python_requires=">=3.12"
)
#NOTE:tthis set.py file is not required as the metadata is already present in the pyproject.toml file.
#      However, it is kept here for reference and future use if needed.