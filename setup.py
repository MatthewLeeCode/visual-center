from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='visual-center',
    author='Matthew Lee',
    description='For finding the visual center of a polygon.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatthewLeeCode/visual-center",
    version='0.1.2',
    packages=['visual_center'],
    install_requires=[
        'opencv-python==4.6.0.66'
    ],
    python_requires='>=3.10',
)