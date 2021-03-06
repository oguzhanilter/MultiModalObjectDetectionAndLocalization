import numpy as np
import sensor_msgs.point_cloud2 as pc2

Z_UPWARDS   = 2

def filter_ground(point3D, ground_percentage, upward = Z_UPWARDS):
    """ Filter the ground according to given percentage. 
    Args:
        point3D                   : 3D point translated point cloud 

    Returns:
        non_groun_point3D         : indices of points that are not ground
    """

    if upward < 0:
        indices = np.nonzero(point3D[:,-upward] < max(point3D[:,-upward])*(100-ground_percentage)/100)[0]
        
    else:
        indices = np.nonzero(point3D[:,upward] > min(point3D[:,upward])*(100-ground_percentage)/100)[0]
    
    return point3D[indices]

def pointcloud2_to_xyzi(pointcloud2):
    """ pointcloud2 to xyzi numpu array transformation
    Args:
        pointcloud2  : pointcloud2 ros message

    Returns:
        xyzi         : numpy array of nx4 of coordinate of lidar points 
    """
    pc_list = pc2.read_points_list(pointcloud2, skip_nans=True)
    xyzi = np.zeros((len(pc_list),4))
    for ind, p in enumerate(pc_list):
        xyzi[ind,0] = p[0]
        xyzi[ind,1] = p[1]
        xyzi[ind,2] = p[2]
        xyzi[ind,3] = p[3]
    return xyzi

def check_validity_image_info(K, w, h):
    l = [K,w,h]
    if all( x is not None for x in l ) and K[2,2] > 0 and w > 0 and h > 0 :
        return True
    else:
        return False

def check_validity_lidar2camera_transformation(R,t):
    l = [R,t]
    if all( x is not None for x in l ):
        return True
    else:
        return False
