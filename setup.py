from setuptools import setup, find_packages

setup(
    name="website",
    packages=find_packages(),
    version="0.1",
    description="Flask Note App",
    author="Your Name",
    install_requires=[
        "flask",
        "flask-login",
        "flask-sqlalchemy",
        "flask-wtf",
        "flask-migrate",
        "flask-mailman",
        "flask-talisman",
        "python-dotenv",
    ],
) 