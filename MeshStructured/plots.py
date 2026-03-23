import numpy as np
from matplotlib import pyplot as plt
from MeshStructured.coordinates import COORD


def plot(x, y, z, coord_type, ax=None, fname_png=None, _show=True, dpi=300):
    """Grafica la batimetria en la malla rectangular.
    :param fname_png: [str] Nombre del archivo de salida.
    :param _show: [bool] Mostrar la figura.
    :param ax: [matplotlib.axes.Axes] Eje donde se graficara la batimetria.
    :param dpi: [int] DPI de la figura."""

    z *= -1
    z[z >= 0] = np.nan

    if ax is None:
        fig, ax = plt.subplots(1, 1)
        _show = True if _show else False
    else:
        fig = ax.figure

    ax.set_title('Batimetria en la malla rectangular')
    if coord_type == COORD.UTM:
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
    else:
        ax.set_xlabel('Lon (º)')
        ax.set_ylabel('Lat (º)')
    ax.set_aspect('equal')
    pc = ax.pcolor(x, y, z, cmap='Blues_r', shading='auto', edgecolors="k", linewidth=0.5)
    cbar = fig.colorbar(pc)
    cbar.set_label("(m)", labelpad=-0.1)

    if _show:
        plt.show()
    elif fname_png is not None:
        plt.savefig(fname_png, dpi=dpi)

    return ax


def plot_3d(x, y, z, coord_type, ax=None, fname_png=None, _show=True, dpi=300):
    """Grafica la batimetria en la malla rectangular en 3D."""

    z *= -1
    z[z == 0] = np.nan

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(50, 135)
    else:
        fig = ax.figure

    ax.plot_surface(x, y, z, cmap='Blues_r')

    if coord_type == COORD.UTM:
        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
    else:
        ax.set_xlabel('Lon [º]')
        ax.set_ylabel('Lat [º]')
    ax.set_zlabel('Z [m]')

    if _show:
        plt.show()
    elif fname_png is not None:
        plt.savefig(fname_png, dpi=dpi)

    return ax
