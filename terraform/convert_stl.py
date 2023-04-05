import os
import numpy as np
import trimesh


# Get the path to your home directory
home_dir = os.path.expanduser('~')
# Set a file path within your home directory
file_path = os.path.join(home_dir, 'Copernicuscrater3Xv.stl')
# Load the STL file
stl_mesh = trimesh.load(file_path)

# Rescale the vertex coordinates to fit in a 100x100x100 array
vertices = stl_mesh.vertices / stl_mesh.vertices.max() * 100

# Extract the vertex coordinates of each triangle
triangles = vertices[stl_mesh.faces]

# Create a 3D NumPy array with the vertex coordinates
array = np.zeros((100, 100, 100), dtype=bool)

for triangle in triangles:
    xmin, ymin, zmin = triangle.min(axis=0).astype(int)
    xmax, ymax, zmax = triangle.max(axis=0).astype(int)
    array[xmin:xmax+1, ymin:ymax+1, zmin:zmax+1] = True

# Set file path for output
output_path = os.path.join(home_dir, 'array.txt')
# Save the array to a text file
np.savetxt(output_path, np.array_str(array.astype(int), max_line_width=np.inf).replace('[', '[[').replace(']', ']]').replace('\n ', '\n').replace(' ', ',').replace('[,', '['), fmt='%s')
