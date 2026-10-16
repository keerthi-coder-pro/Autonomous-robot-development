#!/usr/bin/env python3
"""Generate Centurion-style B.Tech project report PDF for the virtual robot project."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
GRAPHS = ROOT / "docs" / "graphs"
OUT = ROOT / "docs" / "Virtual_Autonomous_Robot_Project_Report.pdf"
OUT_DOWNLOADS = Path.home() / "Downloads" / "Virtual_Autonomous_Robot_Project_Report.pdf"

STUDENT_NAME = "[Keerthi Chinnari]"
REG_NO = "230301120534"
GUIDE = "Mr. Saswat Panda"
DEPT = "Department of Electronic and Communication Engineering"
CAMPUS = "Bhubaneswar Campus"
UNI = "Centurion University of Technology and Management"
MONTH_YEAR = "October, 2026"
PROJECT_TITLE = (
    "Development of a Virtual Autonomous Robot using ROS2 and Gazebo"
)
SUBTITLE = (
    "Autonomous Obstacle Detection and Avoidance in Simulation"
)


class ReportPDF(FPDF):
    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Times", "", 10)
        self.cell(0, 10, f"{self.page_no()}", align="C")

    def chapter_title(self, num: int, title: str) -> None:
        self.set_font("Times", "B", 14)
        self.multi_cell(0, 8, f"CHAPTER {num}: {title.upper()}")
        self.ln(2)

    def section(self, title: str) -> None:
        self.set_font("Times", "B", 12)
        self.multi_cell(0, 7, title)
        self.ln(1)

    def body(self, text: str) -> None:
        self.set_font("Times", "", 11)
        self.set_x(self.l_margin)
        self.multi_cell(self.epw, 6, text)
        self.ln(2)

    def bullet_list(self, items: list[str]) -> None:
        self.set_font("Times", "", 11)
        for item in items:
            self.set_x(self.l_margin)
            self.multi_cell(self.epw, 6, f"- {item}")
        self.ln(2)


def build() -> None:
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(25, 25, 25)

    # --- Title page ---
    pdf.add_page()
    pdf.ln(25)
    pdf.set_font("Times", "B", 16)
    pdf.multi_cell(0, 10, PROJECT_TITLE, align="C")
    pdf.ln(4)
    pdf.set_font("Times", "", 13)
    pdf.multi_cell(0, 8, SUBTITLE, align="C")
    pdf.ln(15)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 8, "A PROJECT REPORT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 7, "Submitted by", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 8, STUDENT_NAME, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 7, f"Reg No-{REG_NO}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.multi_cell(
        0,
        7,
        "in partial fulfilment for the award of the\ndegree of\nBACHELOR OF TECHNOLOGY\nin\nELECTRONIC COMMUNICATION AND ENGINEERING",
        align="C",
    )
    pdf.ln(20)
    pdf.set_font("Times", "B", 12)
    pdf.multi_cell(
        0,
        7,
        f"{DEPT}\nSCHOOL OF ENGINEERING AND TECHNOLOGY\n{CAMPUS.upper()}\n{UNI}\nODISHA",
        align="C",
    )
    pdf.ln(15)
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 8, MONTH_YEAR, align="C")

    # --- Bonafide ---
    pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.multi_cell(0, 7, f"{DEPT}\nSCHOOL OF ENGINEERING AND TECHNOLOGY\n{CAMPUS.upper()}\nBONAFIDE CERTIFICATE")
    pdf.ln(6)
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(
        0,
        6,
        f'Certified that this project report "{PROJECT_TITLE}" is the Bonafide work of '
        f'"{STUDENT_NAME}" who carried out the project work under my supervision. This is to '
        "further certify to the best of my knowledge, that this project has not been carried "
        "out earlier in this institute and the university.",
    )
    pdf.ln(20)
    pdf.cell(0, 7, f"({GUIDE})")
    pdf.ln(5)
    pdf.cell(0, 7, "Assistant Professor of ECE, SoET")
    pdf.ln(15)
    pdf.multi_cell(0, 6, "Certified that the above-mentioned project has been duly carried out as per the norms of the college and statutes of the university")
    pdf.ln(25)
    pdf.cell(0, 7, "SIGNATURE\nHOD/DEAN")
    pdf.ln(10)
    pdf.cell(0, 7, "DEPARTMENT SEAL")

    # --- Declaration ---
    pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 8, "DECLARATION", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(
        0,
        6,
        f'I hereby declare that the project entitled "{PROJECT_TITLE}" submitted for the '
        '"Minor Project" of 7th semester B. Tech in Electronic Communication Engineering is my '
        "original work and the project has not formed the basis for the award of any Degree / "
        "Diploma or any other similar titles in any other University / Institute.",
    )
    pdf.ln(15)
    pdf.cell(0, 7, f"Name of the Student: {STUDENT_NAME}")
    pdf.ln(5)
    pdf.cell(0, 7, "Signature of the Student: ____________________")
    pdf.ln(5)
    pdf.cell(0, 7, f"Registration No: {REG_NO}")
    pdf.ln(5)
    pdf.cell(0, 7, "Place: Bhubaneswar")
    pdf.ln(5)
    pdf.cell(0, 7, "Date: ____________________")

    # --- Acknowledgements ---
    pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 8, "ACKNOWLEDGEMENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("Times", "", 11)
    ack = (
        f"I wish to express my profound gratitude to {GUIDE}, {DEPT}, SoET, {CAMPUS}, "
        f"who guided me through the design and implementation of this robotics simulation project. "
        "I thank the Head of the Department and the Dean, School of Engineering and Technology, "
        f"{CAMPUS}, for their support during the course of this investigation. "
        "I am highly grateful to my guide for invaluable suggestions on ROS 2, Gazebo, and autonomous navigation. "
        "I am indebted to my parents for their constant encouragement throughout my endeavour."
    )
    pdf.multi_cell(0, 6, ack.replace("  ", " "))
    pdf.ln(10)
    pdf.cell(0, 7, f"Name of the Student: {STUDENT_NAME}")
    pdf.ln(5)
    pdf.cell(0, 7, f"Registration No: {REG_NO}")

    # --- Abstract ---
    pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 8, "ABSTRACT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(
        0,
        6,
        "Autonomous mobile robots must perceive obstacles and alter their motion without human "
        "intervention. Building and testing such systems on physical hardware is expensive and "
        "risky; simulation on Linux using the Robot Operating System 2 (ROS 2) and Gazebo provides "
        "a safe, repeatable platform for algorithm development. "
        "This project presents the development of a virtual differential-drive robot equipped with "
        "a 360-degree lidar sensor in Gazebo Classic on Ubuntu 22.04 with ROS 2 Humble. "
        "The robot operates in a custom obstacle arena with walls, boxes, and cylinders. "
        "An obstacle detector node processes LaserScan messages, divides the field of view into "
        "front, left, and right sectors, and publishes an ObstacleReport message. "
        "A reactive obstacle avoider node subscribes to this report and publishes velocity commands "
        "on /cmd_vel to move forward, slow down, turn toward the clearer side, or reverse when "
        "critically close. "
        "The complete system is integrated through ROS 2 launch files and validated in simulation. "
        "Performance is documented using time-series graphs of obstacle distance, robot speed, "
        "decision states, and alert timelines. The report covers system architecture, software "
        "modules, parameter tuning, test procedure, results, limitations, and future improvements "
        "such as Nav2 path planning and deployment on a real robot platform.",
    )

    # --- TOC ---
    pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 8, "TABLE OF CONTENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    toc = [
        "CHAPTER 1: INTRODUCTION .......................................................... 7",
        "CHAPTER 2: LITERATURE REVIEW .................................................... 8",
        "CHAPTER 3: SYSTEM ARCHITECTURE ................................................. 10",
        "CHAPTER 4: ROBOT MODEL AND GAZEBO WORLD ...................................... 12",
        "CHAPTER 5: OBSTACLE DETECTION AND AVOIDANCE ................................... 14",
        "CHAPTER 6: ROS 2 SOFTWARE IMPLEMENTATION ..................................... 16",
        "CHAPTER 7: TESTING, GRAPHS, AND RESULTS ...................................... 18",
        "CHAPTER 8: APPLICATIONS, LIMITATIONS, AND FUTURE SCOPE ....................... 22",
        "CHAPTER 9: CONCLUSION ........................................................ 23",
        "REFERENCES ................................................................... 24",
        "APPENDIX ..................................................................... 25",
    ]
    pdf.set_font("Times", "", 11)
    for line in toc:
        pdf.cell(0, 7, line, new_x="LMARGIN", new_y="NEXT")

    # --- Chapter 1 ---
    pdf.add_page()
    pdf.chapter_title(1, "INTRODUCTION")
    pdf.section("1.1 Background")
    pdf.body(
        "Mobile robotics is widely used in warehouse automation, surveillance, agriculture, and "
        "service applications. A fundamental capability is obstacle detection combined with "
        "collision avoidance while the robot continues toward its goal. Modern robotics software "
        "stacks separate hardware drivers, perception, planning, and control into communicating "
        "modules. ROS 2 is the de facto middleware for such systems, and Gazebo simulates physics, "
        "sensors, and actuators before real-world deployment."
    )
    pdf.section("1.2 Problem Statement")
    pdf.body(
        "To design and implement a virtual autonomous robot on Ubuntu Linux using ROS 2 Humble and "
        "Gazebo that detects obstacles using lidar and autonomously avoids them in a simulated "
        "environment without manual teleoperation."
    )
    pdf.section("1.3 Objectives")
    pdf.bullet_list(
        [
            "To install and integrate Ubuntu, ROS 2, and Gazebo for robotics simulation.",
            "To model a differential-drive mobile robot with lidar in URDF and spawn it in Gazebo.",
            "To implement obstacle detection from LaserScan data using sector-based analysis.",
            "To implement reactive obstacle avoidance publishing geometry_msgs/Twist on /cmd_vel.",
            "To demonstrate and document results using simulation logs and performance graphs.",
        ]
    )
    pdf.section("1.4 Scope and Limitations")
    pdf.body(
        "The project covers simulation only (no physical robot), reactive local avoidance (no global "
        "SLAM or Nav2 path planner), and Gazebo Classic. Dead-end traps and dynamic obstacles are "
        "not fully addressed."
    )
    pdf.section("1.5 Methodology")
    pdf.bullet_list(
        [
            "Literature review of ROS 2, Gazebo, and obstacle avoidance methods.",
            "URDF/Xacro robot design and Gazebo world creation.",
            "ROS 2 package development (messages, detector, avoider, bringup).",
            "Simulation testing and graph generation.",
            "Report documentation.",
        ]
    )

    # --- Chapter 2 ---
    pdf.add_page()
    pdf.chapter_title(2, "LITERATURE REVIEW")
    pdf.section("2.1 Mobile Robot Locomotion")
    pdf.body(
        "Differential-drive robots use two independently driven wheels and a castor. Kinematic "
        "control uses linear velocity v and angular velocity omega. This configuration is common "
        "in TurtleBot-class platforms and is well supported in Gazebo through gazebo_ros_diff_drive."
    )
    pdf.section("2.2 ROS 2 Middleware")
    pdf.body(
        "ROS 2 uses DDS for publish-subscribe communication. Nodes exchange typed messages on topics "
        "such as sensor_msgs/LaserScan and geometry_msgs/Twist. Launch files start multiple nodes "
        "with parameters. Humble Hawksbill on Ubuntu 22.04 is a long-term support pairing used "
        "in education and industry."
    )
    pdf.section("2.3 Gazebo Simulation")
    pdf.body(
        "Gazebo Classic provides rigid-body dynamics, ray-based lidar, and plugin interfaces to ROS. "
        "Simulated time (use_sim_time) synchronises sensor and control nodes with the physics engine."
    )
    pdf.section("2.4 Obstacle Avoidance Approaches")
    pdf.body(
        "Methods range from simple reactive rules (bug algorithms, potential fields) to map-based "
        "planning (A*, D*, Nav2 costmaps). Reactive methods are computationally light and suitable "
        "for local avoidance when a global map is unavailable. This project implements a rule-based "
        "policy with distance thresholds for stop, turn, and reverse behaviours."
    )
    pdf.section("2.5 Summary")
    pdf.body(
        "Simulation with ROS 2 and Gazebo is an established approach to teach and validate autonomous "
        "navigation before hardware integration."
    )

    # --- Chapter 3 ---
    pdf.add_page()
    pdf.chapter_title(3, "SYSTEM ARCHITECTURE")
    pdf.section("3.1 Block Diagram")
    pdf.body(
        "Gazebo publishes /scan from the lidar plugin. The obstacle_detector node converts scans to "
        "ObstacleReport on /obstacle_report. The obstacle_avoider node publishes /cmd_vel to the "
        "diff-drive plugin. Robot state publisher broadcasts TF from URDF. Odometry is available on /odom."
    )
    pdf.section("3.2 Software Packages")
    pdf.body(
        "virtual_robot_description (URDF, world), virtual_robot_msgs (ObstacleReport), "
        "obstacle_avoidance (detector, avoider, policy, plot_logger), virtual_robot_bringup (launch)."
    )
    pdf.section("3.3 Hardware / Platform Requirements")
    pdf.body(
        "Ubuntu 22.04, ROS 2 Humble, Gazebo Classic, Python 3.10+. Docker desktop image provided "
        "for cross-platform development with noVNC on port 6080."
    )

    # --- Chapter 4 ---
    pdf.add_page()
    pdf.chapter_title(4, "ROBOT MODEL AND GAZEBO WORLD")
    pdf.section("4.1 URDF Model")
    pdf.body(
        "The robot consists of a rectangular chassis (0.42 m x 0.24 m), two driven wheels "
        "(radius 0.06 m, separation 0.31 m), a rear castor, and a lidar link mounted forward on "
        "the body. Gazebo plugins implement differential drive and ray sensor output as LaserScan."
    )
    pdf.section("4.2 Lidar Configuration")
    pdf.body(
        "Horizontal scan: 360 samples over -pi to +pi rad, range 0.12 m to 8.0 m, update rate 8 Hz, "
        "visualised in Gazebo as blue rays."
    )
    pdf.section("4.3 Obstacle World")
    pdf.body(
        "The obstacles.world file defines a 9.6 m square arena with four walls and seven coloured "
        "obstacles (boxes and cylinders). The robot spawns at (-3.2, -3.2) m with yaw 0.785 rad."
    )

    # --- Chapter 5 ---
    pdf.add_page()
    pdf.chapter_title(5, "OBSTACLE DETECTION AND AVOIDANCE")
    pdf.section("5.1 Sector Analysis")
    pdf.body(
        "Each lidar range reading is mapped to an angle in the robot frame. Readings are grouped into "
        "front (|angle| <= 0.50 rad), left (0.50 to 1.40 rad), and right (-1.40 to -0.50 rad). "
        "The minimum valid range in each sector is stored. Nearest obstacle distance and angle are "
        "tracked over the forward half-plane."
    )
    pdf.section("5.2 Avoidance Policy")
    pdf.body(
        "If front range < critical_range (0.35 m): reverse and turn. "
        "Else if front range < stop_range (0.70 m): turn toward the side with larger clearance, "
        "with commit_seconds to reduce oscillation. "
        "Else if front range < slow_range (1.15 m): forward at slow_speed. "
        "Else: forward at forward_speed with optional side bias when one flank is closer than "
        "side_influence (0.85 m)."
    )
    pdf.section("5.3 Parameters")
    pdf.body(
        "Tunable values are stored in avoidance.yaml: forward_speed 0.22 m/s, turn_speed 0.90 rad/s, "
        "reverse_speed 0.08 m/s, stop_range 0.70 m, critical_range 0.35 m."
    )

    # --- Chapter 6 ---
    pdf.add_page()
    pdf.chapter_title(6, "ROS 2 SOFTWARE IMPLEMENTATION")
    pdf.section("6.1 Obstacle Detector Node")
    pdf.body(
        "Python node obstacle_detector subscribes to /scan with sensor QoS, calls analyze_scan(), "
        "fills ObstacleReport, sets front_blocked when front_range < stop_range, and publishes at "
        "each scan callback."
    )
    pdf.section("6.2 Obstacle Avoider Node")
    pdf.body(
        "Python node obstacle_avoider runs a 10 Hz timer, reads the latest ObstacleReport, invokes "
        "AvoidancePolicy.step(), publishes Twist on /cmd_vel and a string label on /avoidance_action."
    )
    pdf.section("6.3 Launch Integration")
    pdf.body(
        "simulation.launch.py starts gazebo_ros, robot_state_publisher, delayed spawn_entity, "
        "and delayed detector/avoider nodes. Command: ros2 launch virtual_robot_bringup bringup.launch.py"
    )
    pdf.section("6.4 Unit Tests")
    pdf.body(
        "test_policy.py verifies sector analysis, turn behaviour when front blocked, and reverse at "
        "critical range using pytest without Gazebo."
    )

    # --- Chapter 7 ---
    pdf.add_page()
    pdf.chapter_title(7, "TESTING, GRAPHS, AND RESULTS")
    pdf.section("7.1 Test Environment")
    pdf.body(
        "Tests were conducted in Docker (tiryoh/ros2-desktop-vnc:humble, linux/amd64) and verified "
        "with colcon build, pytest, and live simulation. Gazebo Real Time Factor was approximately "
        "0.85 to 0.95 on the test machine."
    )
    pdf.section("7.2 Functional Observations")
    pdf.bullet_list(
        [
            "Lidar rays correctly intersect walls and obstacles.",
            "obstacle_detector logs front/left/right ranges every 2 s.",
            "obstacle_avoider publishes turn, reverse, and forward actions.",
            "Robot navigates the arena without continuous manual cmd_vel.",
        ]
    )
    pdf.section("7.3 Results Tables")
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 7, "Table 1: Avoidance threshold parameters", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 10)
    rows = [
        ("Parameter", "Value", "Purpose"),
        ("stop_range", "0.70 m", "Front blocked; start turn"),
        ("critical_range", "0.35 m", "Emergency reverse"),
        ("slow_range", "1.15 m", "Reduce forward speed"),
        ("forward_speed", "0.22 m/s", "Cruise speed"),
        ("turn_speed", "0.90 rad/s", "In-place turn rate"),
    ]
    col_w = (40, 30, 80)
    for row in rows:
        pdf.cell(col_w[0], 7, row[0], border=1)
        pdf.cell(col_w[1], 7, row[1], border=1)
        pdf.cell(col_w[2], 7, row[2], border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 7, "Table 2: ROS 2 topics used in validation", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 10)
    topics = [
        ("/scan", "sensor_msgs/LaserScan", "Lidar input"),
        ("/obstacle_report", "virtual_robot_msgs/ObstacleReport", "Detection output"),
        ("/cmd_vel", "geometry_msgs/Twist", "Motor command"),
        ("/avoidance_action", "std_msgs/String", "Behaviour label"),
        ("/odom", "nav_msgs/Odometry", "Wheel odometry"),
    ]
    for t in topics:
        pdf.cell(45, 7, t[0], border=1)
        pdf.cell(55, 7, t[1], border=1)
        pdf.cell(50, 7, t[2], border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.section("7.4 Graphical Results")
    pdf.body(
        "Figure 1 shows the six-panel dashboard: robot path, forward speed, nearest obstacle distance "
        "with stop threshold, front clearance, decision state (forward/slow/turn/reverse), and "
        "obstacle alert timeline. These graphs demonstrate the link between perception and control."
    )
    dash = GRAPHS / "presentation_dashboard.png"
    if dash.exists():
        pdf.add_page()
        pdf.set_font("Times", "B", 11)
        pdf.cell(0, 7, "Fig. 1: Simulation results dashboard", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.image(str(dash), x=10, w=190)
    pdf.section("7.5 Discussion")
    pdf.body(
        "Reactive avoidance succeeds in open arenas but may fail in narrow dead ends. Graphs show "
        "velocity reductions and state changes coinciding with drops in front clearance. Parameter "
        "tuning trades safety (larger stop_range) against agility (higher forward_speed)."
    )

    # --- Chapter 8 ---
    pdf.add_page()
    pdf.chapter_title(8, "APPLICATIONS, LIMITATIONS, AND FUTURE SCOPE")
    pdf.section("8.1 Applications")
    pdf.bullet_list(
        [
            "Warehouse AGV prototyping and operator training.",
            "University labs for ROS 2 and autonomous systems courses.",
            "Algorithm comparison before hardware purchase.",
        ]
    )
    pdf.section("8.2 Limitations")
    pdf.bullet_list(
        [
            "No global path planning or map building (SLAM).",
            "Gazebo Classic; migration to new Gazebo recommended.",
            "Single robot, static obstacles only in base world.",
        ]
    )
    pdf.section("8.3 Future Scope")
    pdf.bullet_list(
        [
            "Integrate Nav2 stack with costmap and global planner.",
            "Deploy on TurtleBot 3 or similar hardware.",
            "Add camera-based detection and sensor fusion.",
            "Record rosbag datasets for machine-learning classifiers.",
        ]
    )

    # --- Chapter 9 ---
    pdf.add_page()
    pdf.chapter_title(9, "CONCLUSION")
    pdf.body(
        "This project successfully developed a virtual autonomous robot using ROS 2 and Gazebo on "
        "Ubuntu Linux. The system integrates lidar-based obstacle detection with a reactive avoidance "
        "controller in a unified launch workflow. Simulation results and graphs confirm that the robot "
        "responds to proximity data by adjusting linear and angular velocity. The modular ROS 2 "
        "package structure provides a foundation for advanced navigation and real-robot deployment."
    )

    # --- References ---
    pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 8, "REFERENCES", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    refs = [
        "[1] Open Robotics, ROS 2 Documentation - Humble, docs.ros.org, 2024.",
        "[2] Open Robotics, Gazebo Classic Documentation, gazebosim.org, 2024.",
        "[3] M. Quigley et al., ROS: an open-source Robot Operating System, ICRA Workshop, 2009.",
        "[4] S. Thrun, W. Burgard, D. Fox, Probabilistic Robotics, MIT Press, 2005.",
        "[5] gazebo_ros_pkgs, ROS 2 Gazebo integration, github.com/ros-simulation.",
        "[6] Navigation2 (Nav2) Documentation, navigation.ros.org, 2024.",
    ]
    pdf.set_font("Times", "", 11)
    for r in refs:
        pdf.multi_cell(0, 6, r)
        pdf.ln(1)

    # --- Appendix ---
    pdf.add_page()
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 8, "APPENDIX", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 7, "Appendix A: How to Run the Project", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 10)
    appendix = (
        "1. docker compose up --build\n"
        "2. Browser: http://127.0.0.1:6080/ (password: ubuntu)\n"
        "3. source ~/workspace/install/setup.bash\n"
        "4. ros2 launch virtual_robot_bringup bringup.launch.py\n"
        "5. Graphs: python3 scripts/generate_presentation_graphs.py\n"
        "6. Live plot: rqt_plot /obstacle_report/front_range"
    )
    pdf.multi_cell(0, 6, appendix)
    pdf.ln(4)
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 7, "Appendix B: Source Code Locations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Times", "", 10)
    pdf.multi_cell(
        0,
        6,
        "policy.py - sector logic\n"
        "detector_node.py - /scan to /obstacle_report\n"
        "avoider_node.py - /cmd_vel publisher\n"
        "robot.urdf.xacro - robot and sensors\n"
        "simulation.launch.py - full stack launch",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    OUT_DOWNLOADS.write_bytes(OUT.read_bytes())
    print(f"Wrote: {OUT}")
    print(f"Wrote: {OUT_DOWNLOADS}")


if __name__ == "__main__":
    build()
