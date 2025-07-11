from setuptools import setup, find_packages

setup(
    name="parallelstone-manager",
    version="1.0.0",
    description="FastAPI Minecraft server management API with RabbitMQ notifications",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.14",
        "uvicorn==0.35.0",
        "pydantic==2.11.7",
        "pydantic-settings==2.10.1",
        "python-dotenv==1.1.1",
        "python-telegram-bot==22.2",
        "pika==1.3.2",
    ],
    python_requires=">=3.8",
    author="Parallelstone Manager",
    author_email="",
    url="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)