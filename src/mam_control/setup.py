from setuptools import setup
import os
from glob import glob

package_name = 'mam_control'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'),  glob('config/*.yaml')),
        (os.path.join('share', package_name, 'launch'),  glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ali Yazbeck',
    maintainer_email='ali.yazbeck1412@gmail.com',
    description='Mecanum kinematics node',
    license='MIT',
    entry_points={
        'console_scripts': [
            'mecanum_kinematics_node = mam_control.mecanum_kinematics_node:main',
        ],
    },
)
