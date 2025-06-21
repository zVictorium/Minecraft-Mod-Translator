from setuptools import setup, find_packages

setup(
    name="mod-translator",
    version="1.0.0",
    description="Minecraft Mod Translator - A tool for translating Minecraft mod files between languages.",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'mod-translator=app.commands.command_line:main',
            'mod-translator-app=app.commands.app:main',
        ],
    },
    install_requires=[
        "deep-translator>=1.9.0",
        "rich>=12.0.0",
        "questionary>=1.10.0",
        "pyfiglet>=0.8.post1",
    ],
)
