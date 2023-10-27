import os
import numpy as np
import configparser
from scipy.interpolate import griddata
from matplotlib import pyplot as plt


class MeshRectangle:
    """Clase para calcular una malla rectangular.

    :param dx: Resolucion en X de la malla.
    :param dy: Resolucion en Y de la malla.
    :param nx: Numero de nodos en X de la malla.
    :param ny: Numero de nodos en Y de la malla.
    :param xmin: Coordenada X minima de la malla.
    :param ymin: Coordenada Y minima de la malla.
    :param x: Coordenadas X de la malla.
    :param y: Coordenadas Y de la malla.
    :param z: Profundidad de la malla."""

    def __init__(self, key, x1=None, x2=None, y1=None, y2=None, dx=100, dy=100, folder_mesh=None, file_mesh_ini=None):
        self.x = []
        self.y = []
        self.z = []

        self.dx = dx
        self.dy = dy

        if file_mesh_ini is not None:
            self.read_conf(file_mesh_ini, key)
        else:
            self.xmin = min(x1, x2)
            self.ymin = min(y1, y2)
            xmax = max(x1, x2)
            ymax = max(y1, y2)

            width = xmax - self.xmin
            heigth = ymax - self.ymin

            self.nx = round(width / self.dx)
            self.ny = round(heigth / self.dy)

            if folder_mesh is not None and folder_mesh.exists():
                self.save_conf(folder_mesh.path, key)

    def read_conf(self, file_mesh_ini, key):
        """Lee el archivo Mesh.ini y carga los parametros de la malla rectangular.

        :param file_mesh_ini: Archivo Mesh.ini."""

        if os.path.exists(file_mesh_ini):
            config_obj = configparser.ConfigParser()
            config_obj.read(file_mesh_ini)

            data = config_obj[key]
            self.xmin = float(data['xmin'])
            self.ymin = float(data['ymin'])
            self.dx = int(data['dx']) if 'dx' in data else self.dx
            self.dy = int(data['dy']) if 'dy' in data else self.dy
            self.nx = int(data['nx']) if 'nx' in data else self.nx
            self.ny = int(data['ny']) if 'ny' in data else self.ny
        else:
            raise ValueError('El archivo {:s} no existe.'.format(file_mesh_ini))

    def save_conf(self, folder_mesh_path, key):
        """Guarda los parametros de la malla rectangular en un archivo MeshMain.ini.

        :param folder_mesh_path: Ruta de la carpeta donde se guardara el archivo MeshMain.ini."""

        with open(os.path.join(folder_mesh_path, 'MeshMain.ini'), 'w') as f:
            f.write('[{:s}}]'.format(key))
            f.write('xmin = {:f}'.format(self.xmin))
            f.write('ymin = {:f}'.format(self.ymin))
            f.write('dx = {:f}'.format(self.dx))
            f.write('dy = {:f}'.format(self.dy))
            f.write('nx = {:f}'.format(self.nx))
            f.write('ny = {:f}'.format(self.ny))

    def exec(self, file_batimetria_dat):
        """Calcula la batimetria en la malla rectangular..

        :param file_batimetria_dat: Nombre del archivo .dat donde se encuentra la batimetria.."""

        # Leo la batimetria.
        bathymetry = np.loadtxt(file_batimetria_dat)
        xb, yb, zb = bathymetry[:, 0], bathymetry[:, 1], bathymetry[:, 2]

        # Calculo las dimensiones de la malla.
        x_ext = np.arange(self.xmin, self.xmin + self.nx * self.dx, self.dx)
        y_ext = np.arange(self.ymin, self.ymin + self.ny * self.dy, self.dy)

        self.x, self.y = np.meshgrid(x_ext, y_ext)
        self.y = np.flipud(self.y)

        # Interpolo la batimetria en la malla.
        self.z = griddata((xb, yb), zb, (self.x, self.y))

    def save(self, file_save_dat):
        """Guarda la profundidad de la batimetria en la malla en un archivo .dat.

        :param file_save_dat: Nombre del archivo .dat donde se guardara la batimetria."""

        f_out = open(file_save_dat, 'w')
        for iDepth_mesh in self.z:
            for ij_depth_mesh in iDepth_mesh:
                if ij_depth_mesh == 0:
                    f_out.write('NaN\t')
                else:
                    f_out.write('{:5.6f}'.format(ij_depth_mesh) + "\t")
            f_out.write("\n")
        f_out.close()

    def plot(self):
        """Grafica la batimetria en la malla rectangular."""

        z = self.z.copy() * -1
        z[z == 0] = np.NaN

        fig, ax = plt.subplots()
        ax.set_title('Batimetria en la malla rectangular')
        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_aspect('equal')
        pc = ax.pcolor(self.x, self.y, z, cmap='Blues_r', shading='auto', edgecolors="k", linewidth=0.5)
        cbar = fig.colorbar(pc)
        cbar.set_label("(m)", labelpad=-0.1)
        plt.show()

    def plot_3d(self):
        """Grafica la batimetria en la malla rectangular en 3D."""

        z = self.z.copy() * -1
        z[z == 0] = np.NaN

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(50, 135)
        ax.plot_surface(self.x, self.y, z, cmap='Blues_r')
        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')
        plt.show()
