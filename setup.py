from setuptools import setup, find_packages

setup(
    name="gustav_kolibri_backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.2",
        "pydantic[email]>=2.5.2",
        "python-dotenv>=1.0.0",
        "supabase>=2.0.3",
    ],
    extras_require={
        "test": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "httpx>=0.25.2",
            "python-multipart>=0.0.6",
        ],
    },
) 