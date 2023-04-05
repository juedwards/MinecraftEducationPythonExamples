import numpy as np
from stl import mesh

# Load the STL file and parse it
mesh_data = mesh.Mesh.from_file('Copernicuscrater3Xv.stl')

# Extract the vertices from the mesh data
vertices = mesh_data.vectors.reshape(-1, 3)

# Create the 3D array from the vertices
x, y, z = vertices.T
x_range = np.arange(np.ceil(x.min()), np.floor(x.max()) + 1)
y_range = np.arange(np.ceil(y.min()), np.floor(y.max()) + 1)
z_range = np.arange(np.ceil(z.min()), np.floor(z.max()) + 1)
xx, yy, zz = np.meshgrid(x_range, y_range, z_range, indexing='ij')
voxel_array = np.zeros(xx.shape, dtype=bool)

for triangle in mesh_data.vectors:
    coords = triangle.flatten().reshape(3, 3)
    voxel_coords = np.stack((np.interp(coords[:, 0], x_range, np.arange(x_range.size)),
                             np.interp(coords[:, 1], y_range, np.arange(y_range.size)),
                             np.interp(coords[:, 2], z_range, np.arange(z_range.size))), axis=1)
    voxel_coords = np.round(voxel_coords).astype(int)
    voxel_array[voxel_coords[:, 0], voxel_coords[:, 1], voxel_coords[:, 2]] = True

# Save the 3D array as a text file
np.savetxt('Output.txt', voxel_array.astype(int), fmt='%d')
