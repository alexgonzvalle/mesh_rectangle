import numpy as np
import scipy.spatial.qhull as qhull


def interp_weights(xy, uv, d=2):
    tri = qhull.Delaunay(xy)
    simplex = tri.find_simplex(uv)
    vertices = np.take(tri.simplices, simplex, axis=0)
    temp = np.take(tri.transform, simplex, axis=0)
    delta = uv - temp[:, d]
    bary = np.einsum('njk,nk->nj', temp[:, :d, :], delta)
    return vertices, np.hstack((bary, 1 - bary.sum(axis=1, keepdims=True)))


def interpolate_var(values, vtx, wts):
    return np.einsum('nj,nj->n', np.take(values, vtx), wts)


def interpolate(x_mesh, y_mesh, x, y, var):
    """Interpolar variable en la malla rectangular.
    :param x: [np.array] Coordenadas X de la variable.
    :param y: [np.array] Coordenadas Y de la variable.
    :param var: [np.array] Variable a interpolar.
    :return: [np.array] Coordenadas X de la malla, [np.array] Coordenadas Y de la malla, [np.array] Variable interpolar en la malla."""

    vtx, wts = interp_weights(np.vstack((x, y)).T, np.vstack((x_mesh.ravel(), y_mesh.ravel())).T)
    var_mesh = interpolate_var(var.flatten(), vtx, wts).reshape(x_mesh.shape[0], x_mesh.shape[1])

    return x_mesh, y_mesh, var_mesh