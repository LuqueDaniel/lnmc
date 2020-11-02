# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
import setuptools

setuptools.setup(
    name="lnmc",
    version="1.0.4",
    license="AGPLv3+",
    description="Allows to create symbolic link in batches from a YAML file "
    "and consolidate them in a specific directory.",
    url="https://github.com/LuqueDaniel/lnmc",
    author="Daniel Luque",
    author_email="danielluque14@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
    ],
    py_modules=["lnmc"],
    python_requires=">=3.6",
    install_requires=["Click>=7.1", "PyYAML>5.0"],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "dev": ["pylint", "mypy", "black>=20.8b1", "isort>=5.6", "pre-commit>=2.4"],
    },
    entry_points={"console_scripts": ["lnmc=lnmc:lnmc"]},
    include_package_data=True,
    data_files=[("", ["LICENSE", "README.md"])],
)
