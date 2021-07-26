import setuptools

if __name__ == "__main__":
    with open("README.md", "r") as f:
        long_description = f.read()

    requirements = [
        'numpy',
        'PyQt5',
        'pyserial',
        'pyqtgraph',
    ]

    setuptools.setup(
        name="SR770",
        version="0.0",
        author="",
        author_email="",
        description="Computer Interface for SR770",
        long_description=long_description,
        packages=setuptools.find_packages(),
        classifiers= "Princeton University. Dark Matter Radio",
        requires=requirements,
    )
