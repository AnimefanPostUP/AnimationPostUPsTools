

#Combiner for the Transformation Matrix
def combine_into_transformation_matrix(translation, scale, rotation):
    """Combine translation, scale, and rotation into a transformation matrix"""
    # Create 4x4 transformation matrix
    transformation_matrix = np.eye(4)

    # Set translation
    transformation_matrix[:3, 3] = translation

    # Set scale
    transformation_matrix[:3, :3] *= scale

    # Set rotation
    transformation_matrix[:3, :3] = np.dot(transformation_matrix[:3, :3], rotation)

    return transformation_matrix

    
#Calculation of the Center of the Vertex Positions
def get_vertex_Center(vertex_positions):
    """Get the center of the given vertex positions"""
    center = mathutils.Vector((0, 0, 0))
    for vertex_position in vertex_positions:
        center += vertex_position
    center /= len(vertex_positions)
    return center

#Detects Changes in Vertex Positions to detect changes in scale
def calculate_average_distance(vertex_positions, center):
    """Calculate the average distance of vertices from the center"""
    distances = [np.linalg.norm(vertex_position - center) for vertex_position in vertex_positions]
    return sum(distances) / len(distances)

#Calculation of Rotation Changes
def calculate_rotation_matrix(old_positions, new_positions, old_center, new_center):
    """Calculate the rotation matrix from old positions to new positions"""
    # Subtract centers from positions
    old_positions_centered = [pos - old_center for pos in old_positions]
    new_positions_centered = [pos - new_center for pos in new_positions]

    # Convert lists to numpy arrays
    old_positions_centered = np.array(old_positions_centered)
    new_positions_centered = np.array(new_positions_centered)

    # Calculate rotation matrix using SVD
    H = np.dot(new_positions_centered.T, old_positions_centered)
    U, S, Vt = np.linalg.svd(H)
    rotation_matrix = np.dot(Vt.T, U.T)

    return rotation_matrix

#Caculculation to find Translation
def calculateCenterOfPoints(points, axis=0):
    return  np.mean(points, axis)

#Original Function currently that is used.
def calculate_vertex_transformation(src_points, dst_points ):
       # Subtract centroids
    src_center = calculateCenterOfPoints(src_points)
    dst_center = calculateCenterOfPoints(dst_points)
    
    src_points_centered = src_points - src_center
    dst_points_centered = dst_points - dst_center

    # Compute rotation
    H = np.dot(src_points_centered.T, dst_points_centered)
    U, S, Vt = np.linalg.svd(H)
    rotation_matrix = np.dot(Vt.T, U.T)

    # Check for reflection
    if np.linalg.det(rotation_matrix) < 0:
        Vt[-1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)

    # Ensure smallest rotation
    d = (np.linalg.det(Vt) * np.linalg.det(U)) < 0.0
    if d:
        S[-1] = -S[-1]
        Vt[-1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)

    # Check for reflection
    if np.linalg.det(rotation_matrix) < 0:
        # Flip the sign of the last column of Vt
        Vt[-1, :] *= -1
        rotation_matrix = np.dot(Vt.T, U.T)
        
    #rotation_matrix = np.linalg.inv(rotation_matrix)
    
    # Compute scale
    src_points_transformed = np.dot(src_points_centered, rotation_matrix)
    scale_x = np.linalg.norm(dst_points_centered[:, 0]) / np.linalg.norm(src_points_transformed[:, 0])
    scale_y = np.linalg.norm(dst_points_centered[:, 1]) / np.linalg.norm(src_points_transformed[:, 1])
    scale_z = np.linalg.norm(dst_points_centered[:, 2]) / np.linalg.norm(src_points_transformed[:, 2])
    scale_matrix = np.diag([scale_x, scale_y, scale_z])
    
    # Debug non-matrix values
    print("Position:", dst_center - src_center)
    print("Scale:", scale_matrix)
    print("Rotation:", rotation_matrix)


    # Create transformation matrix
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = np.dot(scale_matrix, rotation_matrix)
    transformation_matrix[:3, 3] = dst_center - src_center
    
    #transformation_matrix[:3, :3] = rotation_matrix
    #transformation_matrix[:3, 3] = dst_center - rotation_matrix @ src_center
    

    return transformation_matrix, src_center, dst_center


def multiply_matrix(matrix, positions):
    """
    Multiply a matrix by a list of positions.
    
    Args:
        matrix (list[list[float]]): The matrix to be multiplied.
        positions (list[list[float]]): The list of positions to be multiplied.
    
    Returns:
        list[list[float]]: The resulting positions after multiplication.
    """
    result = []
    for position in positions:
        new_position = [sum(a * b for a, b in zip(row, position)) for row in matrix]
        result.append(new_position)
    return result