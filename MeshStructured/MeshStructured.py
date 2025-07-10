import os
import numpy as np
import configparser
from scipy.interpolate import griddata
import scipy.spatial.qhull as qhull
from matplotlib import pyplot as plt
from matplotlib.path import Path
import logging


class MeshStructured:
    """Clase para calcular una malla rectangular.
    :param key: Nombre de la malla.
    :param dx: Resolucion en X de la malla._
    :param dy: Resolucion en Y de la malla."""

    def __init__(self, key, coord_type='UTM'):
        self.logger = logging.getLogger('mi_logger')
        if self.logger is None:
            # Configuración del logger
            logger = logging.getLogger('mi_logger')
            logger.setLevel(logging.INFO)

            # Formato
            formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

            # Archivo
            file_handler = logging.FileHandler('mesh_structured.log', mode='w', encoding='utf-8')
            file_handler.setFormatter(formatter)

            # Consola
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            # Agregar manejadores al logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        self.logger.info(f'Iniciando malla estructurada {key}.')

        self.key = key
        self.coord_type = coord_type

        self.xmin = None
        self.ymin = None

        self.x = []
        self.y = []
        self.z = []

        self.dx = None
        self.dy = None
        self.nx = None
        self.ny = None
        self.lx = None
        self.ly = None

        self.fname_out = ''

    def load(self, x1=None, x2=None, y1=None, y2=None, dx=100, dy=100, file_mesh_ini_save=None, file_mesh_ini=None):
        """ Cargar malla
            :param x1: Coordenada X del primer punto de la malla.
            :param x2: Coordenada X del segundo punto de la malla.
            :param y1: Coordenada Y del primer punto de la malla.
            :param y2: Coordenada Y del segundo punto de la malla.
            :param file_mesh_ini_save: Ruta de la carpeta donde se guardara el archivo MeshMain.ini.
            :param file_mesh_ini: Archivo Mesh.ini."""

        if file_mesh_ini is not None:
            self.read_conf(file_mesh_ini)
        else:
            if x1 is not None and x2 is not None and y1 is not None and y2 is not None:
                self.logger.info(f'Cargar malla rectangular por coordenadas x1: {x1}, x2: {x2}, y1: {y1}, y2: {y2}')

                self.xmin = min(x1, x2)
                self.ymin = min(y1, y2)
                xmax = max(x1, x2)
                ymax = max(y1, y2)

                width = xmax - self.xmin
                heigth = ymax - self.ymin

                self.dx = dx
                self.dy = dy

                self.nx = round(width / self.dx)
                self.ny = round(heigth / self.dy)

                self.lx = self.nx * self.dx
                self.ly = self.ny * self.dy

                if file_mesh_ini_save is not None:
                    self.save_conf(file_mesh_ini_save)

        self.logger.info(f'Malla rectangular {self.key} correcta.')

    def read_conf(self, file_mesh_ini):
        """Lee el archivo Mesh.ini y carga los parametros de la malla rectangular.

        :param file_mesh_ini: Archivo Mesh.ini."""

        if os.path.exists(file_mesh_ini):
            try:
                self.logger.info(f'Cargar fichero de configuración {file_mesh_ini} para la malla rectangular {self.key}')

                if self.coord_type == 'LONLAT':
                    var_x = 'lonmin'
                    var_y = 'latmin'
                    var_dx = 'dlon'
                    var_dy = 'dlat'
                    var_nx = 'nlon'
                    var_ny = 'nlat'
                else:
                    var_x = 'xmin'
                    var_y = 'ymin'
                    var_dx = 'dx'
                    var_dy = 'dy'
                    var_nx = 'nx'
                    var_ny = 'ny'

                config_obj = configparser.ConfigParser()
                config_obj.read(file_mesh_ini)

                data = config_obj[self.key]
                self.xmin = float(data[var_x]) if var_x in data else self.xmin
                self.ymin = float(data[var_y]) if var_y in data else self.ymin
                self.dx = float(data[var_dx]) if var_dx in data else self.dx
                self.dy = float(data[var_dy]) if var_dy in data else self.dy
                self.nx = int(data[var_nx]) if var_nx in data else self.nx
                self.ny = int(data[var_ny]) if var_ny in data else self.ny
                self.lx = self.nx * self.dx
                self.ly = self.ny * self.dy
            except Exception as e:
                self.logger.error(e.args[0])
                raise ValueError(e.args[0])
        else:
            self.logger.error(f'El archivo {file_mesh_ini} no existe.')
            raise ValueError(f'El archivo {file_mesh_ini} no existe.')

    def save_conf(self, file_mesh_ini_save):
        """Guarda los parametros de la malla rectangular en un archivo MeshMain.ini.

        :param file_mesh_ini_save: Ruta de la carpeta donde se guardara el archivo MeshMain.ini."""

        if self.coord_type == 'LONLAT':
            var_x = 'lonmin'
            var_y = 'latmin'
            var_dx = 'dlon'
            var_dy = 'dlat'
            var_nx = 'nlon'
            var_ny = 'nlat'
        else:
            var_x = 'xmin'
            var_y = 'ymin'
            var_dx = 'dx'
            var_dy = 'dy'
            var_nx = 'nx'
            var_ny = 'ny'

        with open(file_mesh_ini_save, 'w') as f:
            f.write(f'[{self.key}]\n')
            f.write(f'{var_x} = {self.xmin}\n')
            f.write(f'{var_y} = {self.ymin}\n')
            f.write(f'{var_dx} = {self.dx}\n')
            f.write(f'{var_dy} = {self.dy}\n')
            f.write(f'{var_nx} = {self.nx}\n')
            f.write(f'{var_ny} = {self.ny}\n')

        self.logger.info(f'Guardado fichero de configuración {file_mesh_ini_save} para la malla rectangular {self.key}.')

    def exec(self, xb, yb, zb, xc=None, yc=None, factor_select=1):
        """Calcula la batimetria en la malla rectangular..
        :param xb: Vector de coordenadas X de la batimetría
        :param yb: Vector de coordenadas Y de la batimetría
        :param zb: Vector de coordenadas Z de la batimetría
        :param xc: Vector de coordenadas X del contorno (opcional)
        :param yc: Vector de coordenadas Y del contorno (opcional)
        :param factor_select: Factor de reduccion de puntos de la batimetria."""

        # Calculo las dimensiones de la malla.
        xmax = self.xmin + self.nx * self.dx
        ymax = self.ymin + self.ny * self.dy

        x_ext = np.arange(self.xmin, xmax, self.dx)
        y_ext = np.arange(self.ymin, ymax, self.dy)

        self.x, self.y = np.meshgrid(x_ext, y_ext)
        self.y = np.flipud(self.y)
        self.xmin, self.ymin = np.nanmin(self.x), np.nanmin(self.y)

        self.logger.info(f'Calculo de la batimetria en la malla rectangular {self.key} correcto.')

        # Reducir el número de puntos de la batimetría escogiendo puntos aleatorios.
        indices = np.random.choice(len(xb), int(len(xb) * factor_select), replace=False)
        xb_s = xb[indices]
        yb_s = yb[indices]
        zb_s = zb[indices]
        self.logger.info(f'Reduccion de puntos de la batimetria correcto. Factor de reduccion: {factor_select}.')

        self.z = griddata((xb_s, yb_s), zb_s, (self.x, self.y), method='linear')
        self.logger.info(f'Interpolacion de la batimetria correcta.')

        if xc is not None and yc is not None:
            points = np.vstack((self.x.ravel(), self.y.ravel())).T
            contorno = Path(np.vstack((xc, yc)).T)
            mask = contorno.contains_points(points).reshape(self.x.shape)
            self.z = np.where(mask, self.z, np.nan)
            self.logger.info(f'Mascara de contorno aplicada a la batimetria correcta.')

    def enabled(self):
        """Comprueba si la malla rectangular tiene batimetria."""

        return self.x is not None

    def save(self, file_save_dat):
        """Guarda la profundidad de la batimetria en la malla en un archivo .dat.

        :param file_save_dat: Nombre del archivo .dat donde se guardara la batimetria."""

        self.fname_out = file_save_dat
        f_out = open(self.fname_out, 'w')
        for iDepth_mesh in self.z:
            for ij_depth_mesh in iDepth_mesh:
                if ij_depth_mesh == 0 or np.isnan(ij_depth_mesh):
                    f_out.write('NaN\t')
                else:
                    f_out.write('{:5.6f}'.format(ij_depth_mesh) + "\t")
            f_out.write("\n")
        f_out.close()

        self.logger.info(f'Guardado de la batimetria en el fichero {self.fname_out} correcto.')

    def plot(self, ax=None, fname_png=None, _show=True):
        """Grafica la batimetria en la malla rectangular.
        :param fname_png: [str] Nombre del archivo de salida.
        :param _show: [bool] Mostrar la figura.
        :param ax: [matplotlib.axes.Axes] Eje donde se graficara la batimetria."""

        z = self.z.copy() * -1
        z[z >= 0] = np.nan

        if ax is None:
            fig, ax = plt.subplots(1, 1)
            _show = True if _show else False
        else:
            fig = ax.figure

        ax.set_title('Batimetria en la malla rectangular')
        if self.coord_type == 'UTM':
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
        else:
            ax.set_xlabel('Lon (º)')
            ax.set_ylabel('Lat (º)')
        ax.set_aspect('equal')
        pc = ax.pcolor(self.x, self.y, z, cmap='Blues_r', shading='auto', edgecolors="k", linewidth=0.5)
        cbar = fig.colorbar(pc)
        cbar.set_label("(m)", labelpad=-0.1)

        if _show:
            plt.show()
        elif _save:
            plt.savefig(fname_png, dpi=300)

        return ax

    def plot_3d(self):
        """Grafica la batimetria en la malla rectangular en 3D."""

        z = self.z.copy() * -1
        z[z == 0] = np.nan

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(50, 135)
        ax.plot_surface(self.x, self.y, z, cmap='Blues_r')
        if self.coord_type == 'UTM':
            ax.set_xlabel('X [m]')
            ax.set_ylabel('Y [m]')
        else:
            ax.set_xlabel('Lon [º]')
            ax.set_ylabel('Lat [º]')
        ax.set_zlabel('Z [m]')
        plt.show()

    def set_var(self, x, y, var):
        """Interpolar variable en la malla rectangular.
        :param x: [np.array] Coordenadas X de la variable.
        :param y: [np.array] Coordenadas Y de la variable.
        :param var: [np.array] Variable a interpolar.
        :return: [np.array] Coordenadas X de la malla, [np.array] Coordenadas Y de la malla, [np.array] Variable interpolar en la malla."""

        def interp_weights(xy, uv, d=2):
            tri = qhull.Delaunay(xy)
            simplex = tri.find_simplex(uv)
            vertices = np.take(tri.simplices, simplex, axis=0)
            temp = np.take(tri.transform, simplex, axis=0)
            delta = uv - temp[:, d]
            bary = np.einsum('njk,nk->nj', temp[:, :d, :], delta)
            return vertices, np.hstack((bary, 1 - bary.sum(axis=1, keepdims=True)))

        def interpolate(values, vtx, wts):
            return np.einsum('nj,nj->n', np.take(values, vtx), wts)

        x_ = np.arange(self.xmin, self.xmin + self.nx * self.dx, self.dx)
        y_ = np.arange(self.ymin, self.ymin + self.ny * self.dy, self.dy)
        x_mesh, y_mesh = np.meshgrid(x_, y_)

        vtx, wts = interp_weights(np.vstack((x, y)).T, np.vstack((x_mesh.ravel(), y_mesh.ravel())).T)
        var_mesh = interpolate(var.flatten(), vtx, wts).reshape(x_mesh.shape[0], x_mesh.shape[1])

        self.logger.info(f'Interpolacion de la variable en la malla estructurada correcta.')

        return x_mesh, y_mesh, var_mesh