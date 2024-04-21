#!/usr/bin/env python

import numpy as np
from scipy.spatial.transform import Rotation


def slots(msg):
    return [getattr(msg, var) for var in msg.__slots__]

def xyzw(q):
    return np.array([q[1], q[2], q[3], q[0]])

def normalize(q):
    n = np.linalg.norm(q)
    return q / n

def centroid(P, w=None):

    if w is None:
        return np.mean(P, axis=0, keepdims=True)

    assert len(P) == len(w)
    assert np.all(w >= 0)

    return np.average(P, axis=0, weights=w)[None]

def align(P0, P1, Pw=None, V0=None, V1=None, Vw=None):
    """Compute absolute orientation of points and vectors.

    Args:
        P0 (np.ndarray): Source points.
        P1 (np.ndarray): Target points.
        Pw (np.ndarray): Source point weights.
        V0 (np.ndarray): Source vectors.
        V1 (np.ndarray): Target vectors.
        Vw (np.ndarray): Source vector weights.
    """
    assert P0.shape == P1.shape
    assert (V0 is None) == (V1 is None)
    assert (Pw is None) == (Vw is None)
    assert P0.shape[1] == 3
    if Pw is not None:
        assert Pw.shape[0] == P0.shape[0]
        assert np.all(Pw >= 0)
    if Vw is not None:
        assert Vw.shape[0] == V0.shape[0]
        assert np.all(Vw >= 0)
    
    if isinstance(P0, list):
        P0 = np.array(P0)
    if isinstance(P1, list):
        P1 = np.array(P1)
    if isinstance(Pw, list):
        Pw = np.array(Pw)
    if isinstance(V0, list):
        V0 = np.array(V0)
    if isinstance(V1, list):
        V1 = np.array(V1)
    if isinstance(Vw, list):
        Vw = np.array(Vw)

    # Compute centroids.
    # c0 = np.mean(P0, axis=0, keepdims=True)
    # c1 = np.mean(P1, axis=0, keepdims=True)
    c0 = centroid(P0, Pw)
    c1 = centroid(P1, Pw)

    # Compute centered vectors.
    P0c = P0 - c0
    P1c = P1 - c1

    if V0 is not None:
        assert V0.shape == V1.shape
        if not isinstance(V0, np.ndarray):
            V0 = np.array(V0)
        if not isinstance(V1, np.ndarray):
            V1 = np.array(V1)
        P0c = np.concatenate([P0c, V0], axis=0)
        P1c = np.concatenate([P1c, V1], axis=0)
        if Vw is not None:
            assert Vw.shape == V0.shape[:1]
            if not isinstance(Vw, np.ndarray):
                Vw = np.array(Vw)
            Pw = np.concatenate([Pw, Vw], axis=0)

    # Compute matrix M.
    if Pw is None:
        M = np.dot(P0c.T, P1c)
    else:
        M = np.dot(P0c.T, P1c * Pw[:, None])
    ((xx, xy, xz),
     (yx, yy, yz),
     (zx, zy, zz)) = M
    # Compose matrix N.
    N = np.array([
        [xx + yy + zz,      yz - zy,       zx - xz,       xy - yx],
        [     yz - zy, xx - yy - zz,       xy + yx,       zx + xz],
        [     zx - xz,      xy + yx, -xx + yy - zz,       yz + zy],
        [     xy - yx,      zx + xz,       yz + zy, -xx - yy + zz],
    ])

    # Compute eigenvector corresponding to largest eigenvalue.
    _, eigvec = np.linalg.eigh(N)
    q = eigvec[:, -1]
    
    R = Rotation.from_quat(xyzw(q))

    # Compute translation vector.
    t = c1 - R.apply(c0)

    # Compose transform.
    T = np.eye(4)
    # T[:3, :3] = R.as_matrix()
    T[:3, :3] = R.as_dcm()
    # T = quaternion_matrix(xyzw(q))
    T[:3, 3:] = t.T
    # print(T)

    return T


def test_align():
    R = np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1],
    ], dtype=np.float64)
    t = np.array([[1], [0], [0]], dtype=np.float64)
    A = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])
    B = (np.dot(R, A.T) + t).T
    T_est = align(A, B)
    R_est = T_est[:3, :3]
    t_est = T_est[:3, 3:]
    assert np.allclose(R, R_est)
    assert np.allclose(t, t_est)


def main():
    test_align()


if __name__ == '__main__':
    main()
