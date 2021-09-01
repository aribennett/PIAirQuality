from setuptools import setup, find_packages

setup(
    name='PIAirQuality',
    version='1.0.0',
    url='https://github.com/aribennett/PIAirQuality',
    author='Ari Bennett',
    author_email='aridbennett@gmail.com',
    description='Raspberry pi aqi reporting and logger',
    packages=find_packages(),    
    install_requires=['pyserial', 'adafruit-io', 'python-dotenv'],
)