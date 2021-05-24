import numpy as np
from sklearn.gaussian_process.kernels import RBF


def initGP(leng_scale, sigma_kernel, simple_equation=True):
    ker = RBF(length_scale=leng_scale)
    # else:
    #     ker = sigma_kernel * RBF(length_scale=leng_scale)

    # j = 0
    #
    # x_grid = []
    # y_grid = []
    # i_data = []
    # j_data = []
    #
    # x = abs(grid_min) + abs(grid_max_x)
    # y = abs(grid_min) + abs(grid_max_y)
    #
    # while j < y:
    #     i = 0
    #     while i < x:
    #         x_grid.append(i - abs(grid_min))
    #         y_grid.append(j - abs(grid_min))
    #         # if grid[i, j] != 0:
    #         #     x_grid.append(i - abs(grid_min))
    #         #     y_grid.append(j - abs(grid_min))
    #         #     i_data.append(i)
    #         #     j_data.append(j)
    #         i += 1
    #     j += 1
    #
    # X_grid = np.array(x_grid).reshape(-1, 1)
    # Y_grid = np.array(y_grid).reshape(-1, 1)
    #
    # X_test = np.concatenate([X_grid, Y_grid], axis=1).reshape(-1, 2)

    return ker


def data(x_p, y_p, y_data):
    x_a = np.array(x_p).reshape(-1, 1)
    y_a = np.array(y_p).reshape(-1, 1)
    x_train = np.concatenate([x_a, y_a], axis=1).reshape(-1, 2)
    y_train = np.array(y_data).reshape(-1, 1)

    return x_a, y_a, x_train, y_train


def gp_regression(n_data, x_p, y_p, y_data, X_test, gpr, post_array):

    x_a, y_a, x_train, y_train = data(x_p, y_p, y_data)
    gpr.fit(x_train, y_train)
    gpr.get_params()

    mu, sigma = gpr.predict(X_test, return_std=True)
    post_ls = np.min(np.exp(gpr.kernel_.theta[0]))
    post_array[n_data - 1] = post_ls

    # Z_var = sigma.reshape(x, y)
    # Z_mean = mu.reshape(x, y)

    return sigma, mu, x_a, y_a, post_array


def gpr_value(g, x_bench, y_bench, X_test, sigma, mu, sigma_data, mu_data):
    for i in range(len(X_test)):
        di = X_test[i]
        dix = di[0]
        diy = di[1]
        if dix == x_bench and diy == y_bench:
            mu_data.append(mu[i])
            sigma_data.append(sigma[i])
            # if g % 5 == 0:
            #     mu_d.append(mu[i])
    # sigma_data.append(sigma_value)
    # mu_data.append(float(mu_value))
    # for i in range(len(mu_data)):
    #     mu_data[i] = float(mu_data[i])
    return sigma_data, mu_data