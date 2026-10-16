from setuptools import setup

package_name = "obstacle_avoidance"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/config", ["config/avoidance.yaml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Virtual Robot Project",
    maintainer_email="dev@example.com",
    description="Lidar obstacle detection and reactive avoidance.",
    license="MIT",
    entry_points={
        "console_scripts": [
            "obstacle_detector = obstacle_avoidance.detector_node:main",
            "obstacle_avoider = obstacle_avoidance.avoider_node:main",
            "plot_logger = obstacle_avoidance.plot_logger_node:main",
            "direction_logger = obstacle_avoidance.direction_log_node:main",
        ],
    },
)
