# © 2019 Daniel Luque
# License AGPLv3 (http://www.gnu.org/licenses/agpl-3.0-standalone.html)
import setuptools


setuptools.setup(
    name='lnmc',
    version='1.0.0',
    description="Allows to create symbolic link in batches from a YAML file "
                "and consolidate them in a specific directory.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Systems Administration',
        "Topic :: Utilities",
        "Topic :: System :: Shells",
    ],
    license="AGPLv3+",
    author='Daniel Luque',
    author_email='danielluque14@gmail.com',
    url='https://github.com/LuqueDaniel/lnmc',
    py_modules=['lnmc'],
    install_requires=[
        'Click',
        'PyYAML'
    ],
    entry_points=dict(
        console_scripts=['lnmc=lnmc:lnmc']),
    test_suite='tests',
)
