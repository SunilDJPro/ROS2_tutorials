from setuptools import find_packages, setup

package_name = 'Py_PubSub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sunildj',
    maintainer_email='tce.sunilprasath@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],

    entry_points = {
        'console_scripts': [
            'py_pub = Py_PubSub.py_pub:main',
            'py_sub = Py_PubSub.py_sub:main',
        ],

    },

    

)
