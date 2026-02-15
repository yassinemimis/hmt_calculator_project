"""
Fonctions d'interpolation et résolution d'équations (sans scipy)
"""
import numpy as np

def linear_interpolation(x_data, y_data, x):
    """Interpolation linéaire simple"""
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    
    if x <= x_data[0]:
        return float(y_data[0])
    if x >= x_data[-1]:
        return float(y_data[-1])
    
    for i in range(len(x_data) - 1):
        if x_data[i] <= x <= x_data[i+1]:
            slope = (y_data[i+1] - y_data[i]) / (x_data[i+1] - x_data[i])
            return float(y_data[i] + slope * (x - x_data[i]))
    
    return float(y_data[-1])


class Interpolator:
    """Classe d'interpolation compatible avec scipy.interpolate.interp1d"""
    
    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)
    
    def __call__(self, x_new):
        if isinstance(x_new, (list, np.ndarray)):
            return np.array([linear_interpolation(self.x, self.y, xi) 
                           for xi in x_new])
        else:
            return linear_interpolation(self.x, self.y, x_new)


def cubic_interpolation(x_data, y_data):
    """Retourne un interpolateur (version simplifiée)"""
    return Interpolator(x_data, y_data)


def simple_fsolve(func, x0, tol=1e-6, max_iter=100):
    """
    Résolution d'équation par méthode de Newton-Raphson
    Compatible avec scipy.optimize.fsolve
    """
    x = x0
    for i in range(max_iter):
        fx = func(x)
        if abs(fx) < tol:
            return [x]
        
        # Dérivée numérique
        h = 1e-8
        dfx = (func(x + h) - fx) / h
        
        if abs(dfx) < 1e-10:
            # Utiliser bisection si dérivée nulle
            return [bisection_method(func, x0 * 0.5, x0 * 1.5, tol)]
        
        x_new = x - fx / dfx
        
        # Éviter les valeurs négatives
        if x_new < 0:
            x_new = x / 2
        
        x = x_new
    
    return [x]


def bisection_method(func, a, b, tol=1e-6, max_iter=100):
    """Méthode de dichotomie"""
    if a < 0:
        a = 1e-6
    if b < a:
        b = a * 2
    
    for i in range(max_iter):
        c = (a + b) / 2
        fc = func(c)
        
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c
        
        fa = func(a)
        if fa * fc < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2