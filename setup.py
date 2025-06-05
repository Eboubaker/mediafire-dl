from setuptools import setup

setup(
    name="mediafire-dl",
    version="0.1.0",
    description="Simple command-line script to download files from mediafire while bypassing cf challange, code is based on Juvenal-Yescas/mediafire-dl",
    url="https://github.com/Eboubaker/mediafire-dl",
    author="Eboubaker Bekkouche",
    author_email="eboubakkar@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="scraping mediafire download selenium seleniumbase",
    py_modules=['mediafire_dl'],
    install_requires=[
        "seleniumbase==4.39.2",
        "tqdm==4.64.1",
        "six==1.17.0",
        "requests==2.32.3",
        "pyautogui==0.9.54",
    ],
    entry_points={
        "console_scripts": ["mediafire-dl=mediafire_dl:main"],
    },
)
