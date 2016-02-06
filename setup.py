from distutils.core import setup

setup(
    name='syscon',
    version='0.8',
    author='syscon',
    author_email='py.syscon@googlemail.com',
    packages=['syscon'],
    scripts=[],
    url='',
    license=open('LICENSE.txt').read(),
    description='System remote control via local network',
    long_description=open('README.txt').read(),
    data_files=[('syscon/win', ['sysconx/win/mousemove.exe', 'sysconx/win/mouseclick.exe'])],
)
