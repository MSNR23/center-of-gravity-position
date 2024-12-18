import sympy as sp

def quaternion_to_rotation_matrix(q):
    """Convert quaternion to rotation matrix symbolically."""
    qw, qx, qy, qz = q
    R = sp.Matrix([
        [1 - 2 * (qy**2 + qz**2), 2 * (qx * qy - qw * qz), 2 * (qx * qz + qw * qy)],
        [2 * (qx * qy + qw * qz), 1 - 2 * (qx**2 + qz**2), 2 * (qy * qz - qw * qx)],
        [2 * (qx * qz - qw * qy), 2 * (qy * qz + qw * qx), 1 - 2 * (qx**2 + qy**2)]
    ])
    return R

def compute_rotation_matrix_pitch(theta):
    """Compute rotation matrix for pitch (y-axis) rotation."""
    R = sp.Matrix([
        [sp.cos(theta), 0, sp.sin(theta)],
        [0, 1, 0],
        [-sp.sin(theta), 0, sp.cos(theta)]
    ])
    return R

def main():
    # Define symbolic parameters
    t = sp.symbols('t')
    l1, lg1, lg2 = sp.symbols('l1 lg1 lg2')  # Link lengths and center of mass distances

    # Generalized coordinates
    qw1, qx1, qy1, qz1 = [sp.Function(f'q1{i}')(t) for i in ['w', 'x', 'y', 'z']]  # Shoulder quaternion
    theta2 = sp.Function('theta2')(t)  # Elbow pitch angle

    # Compute rotation matrices
    R1 = quaternion_to_rotation_matrix([qw1, qx1, qy1, qz1])  # Shoulder rotation
    R2 = compute_rotation_matrix_pitch(theta2)  # Elbow rotation

    # Compute center of mass positions
    O1 = sp.Matrix([0, 0, 0])  # Origin of link 1
    C1 = O1 + R1 * sp.Matrix([lg1, 0, 0])  # Center of mass for link 1
    O2 = O1 + R1 * sp.Matrix([l1, 0, 0])  # Origin of link 2 (end of link 1)
    C2 = O2 + R2 * sp.Matrix([lg2, 0, 0])  # Center of mass for link 2

    # Save results to a text file
    with open("center_of_mass_positions.txt", "w") as file:
        file.write("Link 1 Center of Mass:\n")
        file.write(str(C1) + "\n\n")
        file.write("Link 2 Center of Mass:\n")
        file.write(str(C2) + "\n")

if __name__ == "__main__":
    main()
