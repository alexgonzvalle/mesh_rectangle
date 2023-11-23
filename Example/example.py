from MeshRectangle import MeshRectangle

file_bati_path = r'D:\Development\repos\Garachico\Operacional_Garachico\RESOURCES\SWAN\Batimetria_NUEVA_V2.dat'
file_conf_path = 'Garachico/mesh.ini'

# mesh_main = MeshRectangle('Main', file_mesh_ini=file_conf_path)
# mesh_main.exec(file_bati_path)
# mesh_main.save('Garachico/Bathymetry_mesh_main.dat')
# mesh_main.plot()

mesh_nested = MeshRectangle('Nested', file_mesh_ini=file_conf_path)
mesh_nested.exec(file_bati_path)
# mesh_nested.save('Garachico/Bathymetry_mesh_nested.dat')
mesh_nested.plot()
