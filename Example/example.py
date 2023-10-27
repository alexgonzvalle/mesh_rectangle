from MeshRectangle import MeshRectangle
import os

file_bati_path = os.path.join('Garachico/batimetria.dat')
file_conf_path = 'Garachico/mesh.ini'

mesh_main = MeshRectangle('Main', file_mesh_ini=file_conf_path)
mesh_main.exec(file_bati_path)
mesh_main.save_dat(os.path.join('Garachico/Bathymetry_mesh_main.dat'))
mesh_main.plot_batimetria_malla_3d()

mesh_nested = MeshRectangle('Nested', file_mesh_ini=file_conf_path)
mesh_nested.exec(file_bati_path)
mesh_nested.save_dat(os.path.join('Garachico/Bathymetry_mesh_nested.dat'))
mesh_nested.plot_batimetria_malla_3d()
