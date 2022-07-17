# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Test of the life-cycle consumption model solutions
#  - this notebook undertakes various sanity checks for the source code, the SolveLifeCycle class.
# - author: Tao Wang
# - date: March 2022
# - this is a companion notebook to the paper "Perceived income risks"

import numpy as np
from interpolation import interp
import matplotlib as mp
import matplotlib.pyplot as plt
# %matplotlib inline
from time import time

# + code_folding=[]
## plot configuration 

plt.style.use('seaborn')
plt.rcParams["font.family"] = "Times New Roman" #'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['axes.labelweight'] = 'bold'

## Set the 
plt.rc('font', size=25)
# Set the axes title font size
plt.rc('axes', titlesize=20)
# Set the axes labels font size
plt.rc('axes', labelsize=20)
# Set the font size for x tick labels
plt.rc('xtick', labelsize=20)
# Set the font size for y tick labels
plt.rc('ytick', labelsize=20)
# Set the legend font size
plt.rc('legend', fontsize=20)
# Set the font size of the figure title
plt.rc('figure', titlesize=20)


# -

# ## The Model Class and Solver

from SolveLifeCycle import LifeCycle, solve_model_backward_iter,compare_2solutions

# ## Parameters

# + code_folding=[]
if __name__ == "__main__":

    ## parameters 
    ###################

    U = 0.2 ## transitory ue risk
    U0 = 0.0 ## transitory ue risk
    unemp_insurance = 0.15
    sigma_psi = 0.1 # permanent 
    sigma_eps = 0.0 # transitory 


    #λ = 0.0  ## tax rate
    #λ_SS = 0.0 ## social tax rate
    #transfer = 0.0  ## transfer 
    #pension = 1.0 ## pension


    ## life cycle 

    T = 40
    L = 60
    G = np.ones(L)
    YPath = np.cumprod(G)


    ## other parameters 

    ρ = 2
    R = 1.01
    β = 0.97
    x = 0.0
    theta = 0.0 ## extrapolation parameter 

    ## no persistent state
    b_y = 0.0

    ## wether to have zero borrowing constraint
    borrowing_cstr = True

# + code_folding=[]
## a deterministic income profile 
if __name__ == "__main__":

    plt.title('Deterministic Life-cycle Income Profile \n')
    plt.plot(YPath,'ro')
    plt.xlabel('Age')
    plt.ylabel(r'$\hat Y$')
# -

# ## Life-Cycle Problem 

# ### Consumption  the last period 

# + code_folding=[]
if __name__ == "__main__":
    lc_baseline = LifeCycle(sigma_psi = sigma_psi,
                   sigma_eps = sigma_eps,
                   U=U,
                   ρ=ρ,
                   R=R,
                   T=T,
                   L=L,
                   G=G,
                   β=β,
                   x=x,
                   borrowing_cstr = borrowing_cstr,
                   b_y= b_y,
                   unemp_insurance = unemp_insurance,
                   )


# + code_folding=[]
# Initial the end-of-period consumption policy of σ = consume all assets

if __name__ == "__main__":

    ## terminal consumption function

    m_init,σ_init = lc_baseline.terminal_solution()

# + code_folding=[]
if __name__ == "__main__":

    plt.title('Consumption in the last period')
    plt.plot(m_init[:,0,0],
             σ_init[:,0,0])

# + code_folding=[]
if __name__ == "__main__":

    from copy import copy
    from PrepareParameters import life_cycle_paras_y as lc_paras_Y
    ## make a copy of the imported parameters 
    lc_paras_y = copy(lc_paras_Y)
    lc_paras = lc_paras_y
    print(lc_paras)
# -

# ## A special case of no retirement 
#
# - the consumption function should be non-linear throughout life cycle because of income risks 

# + code_folding=[0]
if __name__ == "__main__":
    lc_no_ret = LifeCycle(
        ## primitives
                   ρ = lc_paras['ρ'],     ## relative risk aversion  
                   β = lc_paras['β'],     ## discount factor
                   borrowing_cstr = borrowing_cstr,
        
        ## prices 
                   R = lc_paras['R'],           ## interest factor
                   W = lc_paras['W'],           ## Wage rate
        
        ## life cycle 
        ##############################
                   T = lc_paras['L'],   ### let the retirement age be equal to life length!!!
        ################################
                   L = lc_paras['L'],
                   G = lc_paras['G'],
                   LivPrb = lc_paras['LivPrb'],       ## living probability 
        
        ## income risks 
                   x = 0.0,
                   b_y = 0.0,
                   sigma_psi = lc_paras['σ_ψ'],
                   sigma_eps = lc_paras['σ_θ'],
                   #ue_markov = True,
                   P = lc_paras['P'],
                   U = lc_paras['U'],
                   z_val = lc_paras['z_val'], ## markov state from low to high 
        
        ## initial conditions 
                    #sigma_p_init = lc_paras['σ_ψ_init'],
                    #init_b = lc_paras['init_b'],

        ## policy 
                   unemp_insurance = lc_paras['unemp_insurance'],
                   pension = lc_paras['pension'], ## pension
                   λ = lc_paras['λ'],  ## tax rate
                   λ_SS = lc_paras['λ_SS'], ## social tax rate
                   transfer = lc_paras['transfer'],  ## transfer 
                   bequest_ratio = lc_paras['bequest_ratio'],
         ## solutions 
                   #grid_max = 10
                   )

# + code_folding=[0]
if __name__ == "__main__":
    
    t_start = time()
    
   
    ## terminal solution
    m_init,σ_init = lc_no_ret.terminal_solution()

    ## solve backward
    ms_star_no_ret, σs_star_no_ret = solve_model_backward_iter(lc_no_ret,
                                                                 m_init,
                                                                 σ_init)

    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))

# + code_folding=[]
if __name__ == "__main__":

    ## plot c func at different age /asset grid
    years_left = [1,15,16,25]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_no_ret.L-year
        i = lc_no_ret.L-age
        m_plt,c_plt = ms_star_no_ret[i,:,0,0],σs_star_no_ret[i,:,0,0]
        axes[x].plot(m_plt,
                     c_plt,
                     label = 'No retirement',
                     lw = 3
                    )
        axes[x].legend()
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))
# -

# ## with extremely large grid 
#
# - the consumption function should be non-linear throughout life cycle because of income risks 

# + code_folding=[]
if __name__ == "__main__":
    lc_a_max = LifeCycle(
        ## primitives
                   ρ = lc_paras['ρ'],     ## relative risk aversion  
                   β = lc_paras['β'],     ## discount factor
                   borrowing_cstr = borrowing_cstr,
        
        ## prices 
                   R = lc_paras['R'],           ## interest factor
                   W = lc_paras['W'],           ## Wage rate
        
        ## life cycle 
        ##############################
                   T = lc_paras['L'],   ### let the retirement age be equal to life length!!!
        ################################
                   L = lc_paras['L'],
                   G = lc_paras['G'],
                   LivPrb = lc_paras['LivPrb'],       ## living probability 
        
        ## income risks 
                   x = 0.0,
                   b_y = 0.0,
                   sigma_psi = lc_paras['σ_ψ'],
                   sigma_eps = lc_paras['σ_θ'],
                   #ue_markov = True,
                   P = lc_paras['P'],
                   U = lc_paras['U'],
                   z_val = lc_paras['z_val'], ## markov state from low to high 
        
        ## initial conditions 
                    #sigma_p_init = lc_paras['σ_ψ_init'],
                    #init_b = lc_paras['init_b'],

        ## policy 
                   unemp_insurance = lc_paras['unemp_insurance'],
                   pension = lc_paras['pension'], ## pension
                   λ = lc_paras['λ'],  ## tax rate
                   λ_SS = lc_paras['λ_SS'], ## social tax rate
                   transfer = lc_paras['transfer'],  ## transfer 
                   bequest_ratio = lc_paras['bequest_ratio'],
         ## solutions 
                   grid_max = 20 ###!!!
                   )

# + code_folding=[]
if __name__ == "__main__":
    
    t_start = time()
    
    ## terminal solution
    m_init,σ_init = lc_a_max.terminal_solution()

    ## solve backward
    ms_star_a_max, σs_star_a_max = solve_model_backward_iter(lc_a_max,
                                                             m_init,
                                                             σ_init)

    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))

# + code_folding=[]
if __name__ == "__main__":

    ## plot c func at different age /asset grid
    years_left = [1,12,15,20]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_a_max.L-year
        i = lc_no_ret.L-age
        m_plt,c_plt = ms_star_a_max[i,:,0,0],σs_star_a_max[i,:,0,0]
        axes[x].plot(m_plt,
                     c_plt,
                     label = 'No retirement',
                     lw = 3
                    )
        axes[x].legend()
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))
# -

# ## A special case of different periods
#

# + code_folding=[]
if __name__ == "__main__":
    lc_2t = LifeCycle(
        ## primitives
                   ρ = lc_paras['ρ'],     ## relative risk aversion  
                   β = lc_paras['β'],     ## discount factor
                   borrowing_cstr = borrowing_cstr,
        
        ## prices 
                   R = lc_paras['R'],           ## interest factor
                   W = lc_paras['W'],           ## Wage rate
        
        ## life cycle 
        ##############################
                   T = 25,   ### let the retirement age be equal to life length!!!
        ################################
                   L = 25,
                   G = lc_paras['G'],
                   LivPrb = lc_paras['LivPrb'],       ## living probability 
        
        ## income risks 
                   x = 0.0,
                   b_y = 0.0,
                   sigma_psi = lc_paras['σ_ψ'],
                   sigma_eps = lc_paras['σ_θ'],
                   #ue_markov = True,
                   P = lc_paras['P'],
                   U = lc_paras['U'],
                   z_val = lc_paras['z_val'], ## markov state from low to high 
        
        ## initial conditions 
                    #sigma_p_init = lc_paras['σ_ψ_init'],
                    #init_b = lc_paras['init_b'],

        ## policy 
                   unemp_insurance = lc_paras['unemp_insurance'],
                   pension = lc_paras['pension'], ## pension
                   λ = lc_paras['λ'],  ## tax rate
                   λ_SS = lc_paras['λ_SS'], ## social tax rate
                   transfer = lc_paras['transfer'],  ## transfer 
                   bequest_ratio = lc_paras['bequest_ratio'],
         ## solutions 
                   #grid_max = 10
                   )

# + code_folding=[]
if __name__ == "__main__":
    
    t_start = time()
    
   
    ## terminal solution
    m_init,σ_init = lc_2t.terminal_solution()

    ## solve backward
    ms_star_2t, σs_star_2t = solve_model_backward_iter(lc_2t,
                                                       m_init,
                                                       σ_init)

    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))

# + code_folding=[]
if __name__ == "__main__":

    ## plot c func at different age /asset grid
    years_left = [0,14,24]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_2t.L-year
        i = lc_2t.L-age
        m_plt,c_plt = ms_star_2t[i,:,0,0],σs_star_2t[i,:,0,0]
        axes[x].plot(m_plt,
                     c_plt,
                     label = 'No retirement',
                     lw = 3
                    )
        axes[x].legend()
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))
# -

# ## No transitory risks 

# + code_folding=[]
if __name__ == "__main__":
    lc_no_trisk = LifeCycle(
        ## primitives
                   ρ = lc_paras['ρ'],     ## relative risk aversion  
                   β = lc_paras['β'],     ## discount factor
                   borrowing_cstr = borrowing_cstr,
        
        ## prices 
                   R = lc_paras['R'],           ## interest factor
                   W = lc_paras['W'],           ## Wage rate
        
        ## life cycle 
        ##############################
                   T = lc_paras['L'],   ### let the retirement age be equal to life length!!!
        ################################
                   L = lc_paras['L'],
                   G = lc_paras['G'],
                   LivPrb = lc_paras['LivPrb'],       ## living probability 
        
        ## income risks 
                   x = 0.0,
                   b_y= 0.0,
                   sigma_psi = lc_paras['σ_ψ'],
                   sigma_eps = 0.0,   ###!!!
                   #ue_markov = True,
                   P = lc_paras['P'],
                   U = lc_paras['U'],
                   z_val = lc_paras['z_val'], ## markov state from low to high 
                   sigma_psi_2mkv = lc_paras['σ_ψ_2mkv'],  ## permanent risks in 2 markov states
                   sigma_eps_2mkv = lc_paras['σ_θ_2mkv'],  ## transitory risks in 2 markov states
        
        ## initial conditions 
                    sigma_p_init = lc_paras['σ_ψ_init'],
                    init_b = lc_paras['init_b'],

        ## policy 
                   unemp_insurance = lc_paras['unemp_insurance'],
                   pension = lc_paras['pension'], ## pension
                   λ = lc_paras['λ'],  ## tax rate
                   λ_SS = lc_paras['λ_SS'], ## social tax rate
                   transfer = lc_paras['transfer'],  ## transfer 
                   bequest_ratio = lc_paras['bequest_ratio'],
         ## solutions 
                   #grid_max = 10
                   )

# + code_folding=[0]
if __name__ == "__main__":
    
    t_start = time()
    
   
    ## terminal solution
    m_init,σ_init = lc_no_trisk.terminal_solution()

    ## solve backward
    ms_star_no_trisk, σs_star_no_trisk = solve_model_backward_iter(lc_no_trisk,
                                                                 m_init,
                                                                 σ_init)

    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))
# -

if __name__ == "__main__":

    ## plot c func at different age /asset grid
    years_left = [1,15,16,19]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_no_trisk.L-year
        i = lc_no_trisk.L-age
        m_plt,c_plt = ms_star_no_trisk[i,:,0,0],σs_star_no_trisk[i,:,0,0]
        axes[x].plot(m_plt,
                     c_plt,
                     label = 'No t risks',
                     lw = 3
                    )
        axes[x].legend()
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))

# ## No permanent risks 

# + code_folding=[]
if __name__ == "__main__":
    lc_no_prisk = LifeCycle(
        ## primitives
                   ρ = lc_paras['ρ'],     ## relative risk aversion  
                   β = lc_paras['β'],     ## discount factor
                   borrowing_cstr = borrowing_cstr,
        
        ## prices 
                   R = lc_paras['R'],           ## interest factor
                   W = lc_paras['W'],           ## Wage rate
        
        ## life cycle 
        ##############################
                   T = lc_paras['L'],   ### let the retirement age be equal to life length!!!
        ################################
                   L = lc_paras['L'],
                   G = lc_paras['G'],
                   LivPrb = lc_paras['LivPrb'],       ## living probability 
        
        ## income risks 
                   x = 0.0,
                   b_y= 0.0,
                   sigma_psi = 0.01*lc_paras['σ_ψ'],   ###!!!
                   sigma_eps = lc_paras['σ_θ'],
                   #ue_markov = True,
                   P = lc_paras['P'],
                   U = lc_paras['U'],
                   z_val = lc_paras['z_val'], ## markov state from low to high 
                   sigma_psi_2mkv = lc_paras['σ_ψ_2mkv'],  ## permanent risks in 2 markov states
                   sigma_eps_2mkv = lc_paras['σ_θ_2mkv'],  ## transitory risks in 2 markov states
        
        ## initial conditions 
                    sigma_p_init = lc_paras['σ_ψ_init'],
                    init_b = lc_paras['init_b'],

        ## policy 
                   unemp_insurance = lc_paras['unemp_insurance'],
                   pension = lc_paras['pension'], ## pension
                   λ = lc_paras['λ'],  ## tax rate
                   λ_SS = lc_paras['λ_SS'], ## social tax rate
                   transfer = lc_paras['transfer'],  ## transfer 
                   bequest_ratio = lc_paras['bequest_ratio'],
         ## solutions 
                   #grid_max = 10
                   )

# + code_folding=[]
if __name__ == "__main__":
    
    t_start = time()
    
    ## terminal solution
    m_init,σ_init = lc_no_prisk.terminal_solution()

    ## solve backward
    ms_star_no_prisk, σs_star_no_prisk = solve_model_backward_iter(lc_no_prisk,
                                                                 m_init,
                                                                 σ_init)

    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))
# -

if __name__ == "__main__":

    ## plot c func at different age /asset grid
    years_left = [1,19,20,30]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_baseline.L-year
        i = lc_baseline.L-age
        m_plt,c_plt = ms_star_no_prisk[i,:,0,0],σs_star_no_prisk[i,:,0,0]
        axes[x].plot(m_plt,
                     c_plt,
                     label = 'No p risks',
                     lw = 3
                    )
        axes[x].legend()
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))

# ## subjective (low risk) versus objective (high risk)

# + code_folding=[]
if __name__ == "__main__":
    lc_obj = LifeCycle(
        ## primitives
                   ρ = lc_paras['ρ'],     ## relative risk aversion  
                   β = lc_paras['β'],     ## discount factor
                   borrowing_cstr = borrowing_cstr,
        
        ## prices 
                   R = lc_paras['R'],           ## interest factor
                   W = lc_paras['W'],           ## Wage rate
        
        ## life cycle 
                   T = lc_paras['L'],
                   L = lc_paras['L'],
                   G = lc_paras['G'],
                   LivPrb = lc_paras['LivPrb'],       ## living probability 
        
        ## income risks 
                   x = 0.0,
                   b_y= 0.0,
                   sigma_psi = lc_paras['σ_ψ'],
                   sigma_eps = lc_paras['σ_θ'],
                   ue_markov = True,
                   P = lc_paras['P'],
                   U = lc_paras['U'],
                   z_val = lc_paras['z_val'], ## markov state from low to high 
                   sigma_psi_2mkv = lc_paras['σ_ψ_2mkv'],  ## permanent risks in 2 markov states
                   sigma_eps_2mkv = lc_paras['σ_θ_2mkv'],  ## transitory risks in 2 markov states
        
        ## initial conditions 
                    sigma_p_init = lc_paras['σ_ψ_init'],
                    init_b = lc_paras['init_b'],

        ## policy 
                   unemp_insurance = lc_paras['unemp_insurance'],
                   pension = lc_paras['pension'], ## pension
                   λ = lc_paras['λ'],  ## tax rate
                   λ_SS = lc_paras['λ_SS'], ## social tax rate
                   transfer = lc_paras['transfer'],  ## transfer 
                   bequest_ratio = lc_paras['bequest_ratio'],
         ## solutions 
                   grid_max = 10
                   )
    lc_sub = LifeCycle(
        ## primitives
                   ρ = lc_paras['ρ'],     ## relative risk aversion  
                   β = lc_paras['β'],     ## discount factor
                   borrowing_cstr = borrowing_cstr,
        ## prices 
                   R = lc_paras['R'],           ## interest factor
                   W = lc_paras['W'],            ## Wage rate
        ## life cycle 
                   T = lc_paras['L'], ###!!!
                   L = lc_paras['L'],
                   G = lc_paras['G'],
                   LivPrb = lc_paras['LivPrb'],       ## living probability 
        
        ## income risks 
                   x = 0.0,
                   b_y= 0.0,
                   sigma_psi = lc_paras['σ_ψ_sub'],
                   sigma_eps = lc_paras['σ_θ_sub'],
                   subjective = True,
                   ue_markov = True,
                   P = lc_paras['P'],
                   U = lc_paras['U'],
                   z_val = lc_paras['z_val'], ## markov state from low to high
                   sigma_psi_2mkv = lc_paras['σ_ψ_2mkv'],  ## permanent risks in 2 markov states
                   sigma_eps_2mkv = lc_paras['σ_θ_2mkv'],  ## transitory risks in 2 markov states
                   sigma_psi_true = lc_paras['σ_ψ'], ## true permanent
                   sigma_eps_true = lc_paras['σ_θ'], ## true transitory
        
        ## initial conditions 
                    sigma_p_init = lc_paras['σ_ψ_init'],
                    init_b = lc_paras['init_b'],

        ## policy 
                   unemp_insurance = lc_paras['unemp_insurance'],
                   pension = lc_paras['pension'], ## pension
                   λ = lc_paras['λ'],  ## tax rate
                   λ_SS = lc_paras['λ_SS'], ## social tax rate
                   transfer = lc_paras['transfer'],  ## transfer 
                   bequest_ratio = lc_paras['bequest_ratio'],
        ## solutions 
                  grid_max = 10
                   )
    
 
    models = [lc_sub,lc_obj]
    model_names = ['subjective','objective']


# + code_folding=[]
if __name__ == "__main__":
    
    t_start = time()
    
    ms_stars =[]
    σs_stars = []

    for i,model in enumerate(models):
        ## terminal solution
        m_init,σ_init = model.terminal_solution()

        ## solve backward
        ms_star, σs_star = solve_model_backward_iter(model,
                                                     m_init,
                                                     σ_init)
        ms_stars.append(ms_star)
        σs_stars.append(σs_star)


    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))

# + code_folding=[]
sub_minus_obj = compare_2solutions(ms_stars,
                                  σs_stars)

plt.hist(sub_minus_obj.flatten(),
         bins=50)
plt.title('Consumption in subjective model(LPR) minus objective model ((HPR))')
print('should be positive')
# -

if __name__ == "__main__":

    m_grid = np.linspace(0.0,10.0,200)
    ## plot c func at different age /asset grid
    years_left = [1,19,20,21]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_baseline.L-year
        i = lc_baseline.L-age
        for k,model_name in enumerate(model_names):
            m_plt,c_plt = ms_stars[k][i,:,0,0],σs_stars[k][i,:,0,0]
            c_func = lambda m: interp(m_plt,c_plt,m)
            axes[x].plot(m_grid,
                         c_func(m_grid),
                         label = model_name,
                         lw = 3
                        )
        axes[x].legend()
        axes[x].set_xlim(0.0,np.max(m_grid))
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))

# ## low versus high risks 

sigma_eps_ls

# + code_folding=[]
if __name__ == "__main__":

    t_start = time()

    sigma_psi_ls = [lc_paras['σ_ψ_sub'],lc_paras['σ_ψ']]
    sigma_eps_ls = [lc_paras['σ_θ_sub'],lc_paras['σ_θ']]
    
    ms_stars =[]
    σs_stars = []
    
    for i,sigma_psi in enumerate(sigma_psi_ls):
        lc_baseline.T = L
        lc_baseline.sigma_psi = sigma_psi
        lc_baseline.sigma_eps = sigma_eps_ls[i]
        ### this line is very important!!!!
        #### need to regenerate shock draws for new sigmas
        lc_baseline.prepare_shocks()
        
        ## terminal solution
        m_init,σ_init = lc_baseline.terminal_solution()
        
        ## solve backward
        ms_star, σs_star = solve_model_backward_iter(lc_baseline,
                                                     m_init,
                                                     σ_init)
        ms_stars.append(ms_star)
        σs_stars.append(σs_star)


    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))

# + code_folding=[]
# compare solutions

sub_minus_obj = compare_2solutions(ms_stars,
                                  σs_stars)

plt.hist(sub_minus_obj.flatten(),
         bins=50)
plt.title('Consumption in low PR model minus in high PR')
print('should be positive')

# + code_folding=[]
if __name__ == "__main__":

    m_grid = np.linspace(0.0,10.0,200)
    ## plot c func at different age /asset grid
    years_left = [0,20,21,40]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_baseline.L-year
        i = lc_baseline.L-age
        model_names = ['low PR','high PR']
        for k,model_name in enumerate(model_names):
            m_plt,c_plt = ms_stars[k][i,:,0,0],σs_stars[k][i,:,0,0]
            #c_func = lambda m: interp(m_plt,c_plt,m)
            axes[x].plot(m_plt,
                         c_plt,
                         label = model_name,
                         lw=3
                        )
        axes[x].legend()
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))
# -

# ## transitory UE risk as a special case of persistent UE
#
#
#
#

# + code_folding=[]
if __name__ == "__main__":
    
    U_prb = 0.2

    lc_trans_ue =  LifeCycle(sigma_psi = sigma_psi,
                       sigma_eps = sigma_eps,
                       U= U_prb,
                       ρ=ρ,
                       R=R,
                       T=T,
                       L=L,
                       G=G,
                       β=β,
                       x=x,
                       borrowing_cstr = borrowing_cstr,
                       b_y= b_y,
                       unemp_insurance = unemp_insurance
                       )

    lc_trans_mkv0 =  LifeCycle(sigma_psi = sigma_psi,
                       sigma_eps = sigma_eps,
                       U=U0,
                       ue_markov=True,
                       P= np.array([[U_prb,1-U_prb],[U_prb,1-U_prb]]),
                       ρ=ρ,
                       R=R,
                       T=T,
                       L=L,
                       G=G,
                       β=β,
                       x=x,
                       borrowing_cstr = borrowing_cstr,
                       b_y= b_y,
                       unemp_insurance = unemp_insurance
                       )


    models = [lc_trans_ue,lc_trans_mkv0] 
    model_names = ['transitory UE',
                  'markov UE:special case']

    t_start = time()

    ms_stars =[]
    σs_stars = []
    for i,model in enumerate(models):
        ## terminal solution
        m_init,σ_init = model.terminal_solution()
        #### need to regenerate shock draws for new sigmas
        ms_star, σs_star = solve_model_backward_iter(model,
                                                     m_init,
                                                     σ_init)
        ms_stars.append(ms_star)
        σs_stars.append(σs_star)


    t_finish = time()

    print("Time taken, in seconds: "+ str(t_finish - t_start))

# +
# compare solutions

trans_mkv_diff = compare_2solutions(ms_stars,
                                  σs_stars)

plt.hist(trans_mkv_diff.flatten(),
         bins=50)
plt.title('Differences in Consumption Policy between two cases')
print('should be positive')

# + code_folding=[] pycharm={"name": "#%%\n"}
if __name__ == "__main__":


    ## plot c func at different age /asset grid
    years_left = [1,20,21,40]

    n_sub = len(years_left)

    fig,axes = plt.subplots(1,n_sub,figsize=(6*n_sub,6))

    for x,year in enumerate(years_left):
        age = lc_baseline.L-year
        i = lc_baseline.L-age
        for k,model_name in enumerate(model_names):
            m_plt,c_plt = ms_stars[k][i,:,0,0],σs_stars[k][i,:,0,0]
            axes[x].plot(m_plt,
                         c_plt,
                         label = model_name,
                         lw=3,
                        )
        axes[x].legend()
        axes[x].set_xlim(0.0,np.max(m_plt))
        axes[x].set_xlabel('asset')
        axes[0].set_ylabel('c')
        axes[x].set_title(r'$age={}$'.format(age))
