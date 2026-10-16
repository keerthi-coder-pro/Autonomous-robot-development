std_msgs/Header header
# Metres. A clear sector is reported as the lidar max range.
float32 front_range
float32 left_range
float32 right_range
float32 nearest_range
# Radians, robot frame. 0 is straight ahead.
float32 nearest_angle
uint16 obstacle_count
bool front_blocked
