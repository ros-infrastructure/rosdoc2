from setuptools import setup

package_name = 'examples_rclpy_minimal_publisher'

setup(
    name=package_name,
    version='0.16.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Mikael Arguedas',
    author_email='mikael@osrfoundation.org',
    maintainer='First Maintainer, Second Maintainer',
    maintainer_email='maint1@example.com, maint2@example.com',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Examples of minimal publishers using rclpy.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisher_old_school =minimal_publisher_py.publisher_old_school:main',
            'publisher_local_function ='
            'minimal_publisher_py.publisher_local_function:main',
            'publisher_member_function ='
            'minimal_publisher_py.publisher_member_function:main',
        ],
    },
)
