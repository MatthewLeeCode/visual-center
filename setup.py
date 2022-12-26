from setuptools import setup

setup(
    name='visual-center',
    version='0.1.0',
    packages=['visual-center'],
    install_requires=[
        'opencv-python==4.6.0.66',
        'pytest==7.2.0'
    ],
    python_requires='>=3.10',
)