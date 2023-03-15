import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gaussquality",
    version="1.0.0",
    author="Elaine Ho",
    author_email="mselaineho@gmail.com",
    description="Image quality assessment with Gaussian Mixture Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elainehoml/GaussQuality",
    project_urls={
        "Bug Tracker": "https://github.com/elainehoml/GaussQuality/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=["gaussquality"],
    install_requires=[
       "numpy",
       "scipy",
       "pandas",
       "matplotlib",
       "scikit-image",
       "scikit-learn",
   ],
   extras_require={
        "test": ["unittest", "coverage"]
   }
   
)