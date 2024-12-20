import os
import numpy as np
import configparser
from scipy.interpolate import griddata
from matplotlib import pyplot as plt


class MeshRectangle:
    """Clase para calcular una malla rectangular.

    :param key: Nombre de la malla.
    :param x1: Coordenada X del primer punto de la malla.
    :param x2: Coordenada X del segundo punto de la malla.
    :param y1: Coordenada Y del primer punto de la malla.
    :param y2: Coordenada Y del segundo punto de la malla.
    :param dx: Resolucion en X de la malla._
    :param dy: Resolucion en Y de la malla.
    :param file_mesh_ini_save: Ruta de la carpeta donde se guardara el archivo MeshMain.ini.
    :param file_mesh_ini: Archivo Mesh.ini."""

    def __init__(self, key, x1=None, x2=None, y1=None, y2=None, dx=100, dy=100,
                 file_mesh_ini_save=None, file_mesh_ini=None):

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

            if file_mesh_ini_save is not None and not file_mesh_ini_save.exists():
                self.save_conf(file_mesh_ini_save, key)

    def read_conf(self, file_mesh_ini, key):
        """Lee el archivo Mesh.ini y carga los parametros de la malla rectangular.

        :param file_mesh_ini: Archivo Mesh.ini.
        :param key: Nombre de la malla."""

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

    def save_conf(self, file_mesh_ini_save, key):
        """Guarda los parametros de la malla rectangular en un archivo MeshMain.ini.

        :param file_mesh_ini_save: Ruta de la carpeta donde se guardara el archivo MeshMain.ini.
        :param key: Nombre de la malla."""

        with open(file_mesh_ini_save, 'w') as f:
            f.write('[{:s}}]'.format(key))
            f.write('xmin = {:f}'.format(self.xmin))
            f.write('ymin = {:f}'.format(self.ymin))
            f.write('dx = {:f}'.format(self.dx))
            f.write('dy = {:f}'.format(self.dy))
            f.write('nx = {:f}'.format(self.nx))
            f.write('ny = {:f}'.format(self.ny))

    def exec(self, file_batimetria_dat, factor_select=1):
        """Calcula la batimetria en la malla rectangular..

        :param file_batimetria_dat: Nombre del archivo .dat donde se encuentra la batimetria.
        :param factor_select: Factor de reduccion de puntos de la batimetria."""

        # Leo la batimetria.
        bathymetry = np.loadtxt(file_batimetria_dat)
        xb, yb, zb = bathymetry[:, 0], bathymetry[:, 1], bathymetry[:, 2]

        # Calculo las dimensiones de la malla.
        xmax = self.xmin + self.nx * self.dx
        ymax = self.ymin + self.ny * self.dy

        x_ext = np.arange(self.xmin, xmax, self.dx)
        y_ext = np.arange(self.ymin, ymax, self.dy)

        self.x, self.y = np.meshgrid(x_ext, y_ext)
        self.y = np.flipud(self.y)

        # Reducir el número de puntos de la batimetría escogiendo puntos aleatorios.
        indices = np.random.choice(len(xb), int(len(xb) * factor_select), replace=False)
        xb_s = xb[indices]
        yb_s = yb[indices]
        zb_s = zb[indices]

        self.z = griddata((xb_s, yb_s), zb_s, (self.x, self.y), method='linear')

    def save(self, file_save_dat):
        """Guarda la profundidad de la batimetria en la malla en un archivo .dat.

        :param file_save_dat: Nombre del archivo .dat donde se guardara la batimetria."""

        f_out = open(file_save_dat, 'w')
        for iDepth_mesh in self.z:
            for ij_depth_mesh in iDepth_mesh:
                if ij_depth_mesh == 0 or np.isnan(ij_depth_mesh):
                    f_out.write('NaN\t')
                else:
                    f_out.write('{:5.6f}'.format(ij_depth_mesh) + "\t")
            f_out.write("\n")
        f_out.close()

    def plot(self):
        """Grafica la batimetria en la malla rectangular."""

        z = self.z.copy() * -1
        z[z >= 0] = np.NaN

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
