"""Package metadata for tutorclickhouse."""
import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    """Load README file which populates long_description field."""
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as file:
        return file.read()


def load_about():
    """Load about file which stores the package version."""
    about = {}
    with io.open(
        os.path.join(HERE, "tutorclickhouse", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as file:
        exec(file.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-clickhouse",
    version=ABOUT["__version__"],
    url="https://github.com/bmtcril/tutor-contrib-clickhouse",
    project_urls={
        "Code": "https://github.com/bmtcril/tutor-contrib-clickhouse",
        "Issue tracker": "https://github.com/bmtcril/tutor-contrib-clickhouse/issues",
    },
    license="AGPLv3",
    author="Brian Mesick",
    description="Clickhouse plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=["tutor"],
    entry_points={"tutor.plugin.v1": ["clickhouse = tutorclickhouse.plugin"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
