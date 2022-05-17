#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:23:19 2022

@author: bt704963
"""

import nmpyc as mpc 

# parameters
rho_W = 997
c_W = 4.1851
V_H = 7.4
k_WR = 510
k_G = 125
thau_G = 260
t_f = 24
P_max = 15000
T_ref = 22

h = 0.5
nx = 2
nu = 1
N = 30          # MPC horizon length
K = 500          # final time for the MPC loop

def T_amb(t):
    return 2.5 + 7.5*mpc.sin((2*mpc.pi*t)/t_f - (mpc.pi/2))

def f(t,x,u):
    y = mpc.array(2)
    y[0] = (-k_WR/(rho_W*c_W*V_H)*x[0] 
            + k_WR/(rho_W*c_W*V_H)*x[1] 
            + 1/(rho_W*c_W*V_H)*u[0])
    y[1] = (k_WR/(k_G*thau_G)*x[0] 
            - (k_WR + k_G)/(k_G*thau_G)*x[1] 
            + (1/thau_G)*T_amb(t))
    return y

def l(x,u):
    return (u[0]/P_max) + (x[1]-T_ref)**2


system = mpc.system(f, nx, nu, 'continuous', sampling_rate=h, method='euler')
objective = mpc.objective(l)

constraints = mpc.constraints()
constraints.add_bound('lower', 'control', mpc.array([0]))
constraints.add_bound('upper', 'control', mpc.array([P_max]))

model = mpc.model(objective,system,constraints)

x0 = mpc.array([22., 19.5])
res = model.mpc(x0,N,K)
res.plot()
