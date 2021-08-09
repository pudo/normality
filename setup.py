from setuptools import setup, find_packages  # type: ignore

with open("README.md") as f:
    long_description = f.read()

setup(
    name="normality",
    version="2.2.3",
    description="Micro-library to normalize text strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="text unicode normalization slugs",
    author="Friedrich Lindenberg",
    author_email="friedrich@pudo.org",
    url="http://github.com/pudo/normality",
    license="MIT",
    package_data={"banal": ["py.typed"]},
    packages=find_packages(exclude=["ez_setup", "examples", "test"]),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=["banal >= 1.0.1", "text-unidecode", "chardet"],
    extras_require={
        "icu": [
            "pyicu >= 1.9.3",
        ],
        "dev": [
            "pyicu >= 1.9.3",
            "mypy",
            "pytest",
            "types-chardet",
        ],
    },
    test_suite="test",
)
