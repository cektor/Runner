from setuptools import setup

setup(
    name="Runner",
    version="1.0",
    packages=["runner"],
    data_files=[("share/applications", ["runner.desktop"])],
    entry_points={
        "console_scripts": [
            "runner=runner.main:main",
        ],
    },
    install_requires=[
        "speedtest-cli",
        "PyQt5",
    ],    
)
