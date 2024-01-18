import csv
import random

import numpy as np
from Entrance import *
from PyQt5.QtGui import QPixmap
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QMessageBox, QLabel


class Controller:
    def __init__(self):
        super().__init__()
        self.InitUi()
        self.InitParameter()
        self.InitFunction()

    def InitUi(self):
        self.ui = mainwindow()
        self.ui.show()

    def InitParameter(self):
        self.A = None
        self.b = None
        self.x0 = None
        self.round = 0
        self.maxit = 0
        self.labels = []
        self.f_data = None
        self.g_data = None
        self.string = None
        self.lambda_ = None
        self.f_star = [0.31828982358410596, 0.15371877617516788, 0.19483915431128194]
        self.dataSet = ['a9a', 'CINA', 'ijcnn']
        self.stepSet = ['fixed', 'armijo', 'bb', 'wolfe']
        self.opts = {'maxit': 1000, 'alpha0': 0.01, 'gtol': 1e-6}
        self.solutionSet = ['grad', 'newtoon', 'lbfgs', 'trustregion']

    def InitFunction(self):
        self.ui.resized.connect(self.changeSize)
        self.ui.getData.clicked.connect(self.readCSV)
        self.ui.codeGo.clicked.connect(self.optimization)
        self.ui.solutionSet.currentIndexChanged.connect(self.changeUI)

    # 获取数据
    def readCSV(self):
        self.A, self.b = [], []
        dataset = ['./dataset/a9a.csv', './dataset/CINA.csv', './dataset/ijcnn.csv']
        with open(dataset[self.ui.dataSet.currentIndex()], 'r', newline='') as f:
            reader = csv.reader(f, delimiter=",")
            for line in reader:
                self.b.append(float(line[-1]))
                self.A.append([float(n) for n in line[:-1]])
        self.A = np.array(self.A).astype(np.float32)
        self.b = np.array(self.b).astype(np.float32)
        num_samples, num_features = self.A.shape
        self.x0 = np.array([0.0] * num_features).astype(np.float32)
        self.lambda_ = 1 / (100 * num_samples)
        self.string = f"数据获取成功，当前数据集为 {dataset[self.ui.dataSet.currentIndex()]}。\n"
        if self.ui.dataShape.isChecked():
            self.string += f'''
A 形状为的：{self.A.shape}
b 形状为：{self.b.shape}
lambda 长度为： 1
x0 形状为：{self.x0.shape}
'''
        if self.ui.dataType.isChecked():
            self.string += f'''
A 的类型为：{type(self.A)}
b 的类型为：{type(self.b)}
lambda 的类型为： {type(self.lambda_)}
x0 的类型为：{type(self.x0)}
'''
        if self.ui.dataContent.isChecked():
            self.string += f'''
A: 
{str(self.A)}

B: 
{str(self.b)}

lambda:
{str(self.lambda_)}

x0:
[0. 0. 0. ... 0. 0. 0.]
'''
        self.ui.displayData.setText(self.string)

    # 定义计算损失函数值的函数
    def calculate_value(self, x):
        total = 0
        for i in range(len(self.b)):
            total += (np.log(1 + np.exp(-self.b[i] * float(self.A[i].T @ x))) / len(self.b))
        return total

    # 定义计算梯度的函数
    def calculate_gradient(self, x):
        length = len(self.b)
        grad = 2 * self.lambda_ * x
        for i in range(length):
            p = float(1 / (1 + np.exp(-self.b[i] * float(self.A[i].T @ x))))
            grad -= ((1 - p) * self.b[i] * self.A[i]) / length
        return grad

    # 计算海瑟矩阵
    def calculate_hessian(self, x):
        length = len(self.b)
        hessian = 2 * self.lambda_ * np.eye(len(x))
        for i in range(length):
            p = float(1 / (1 + np.exp(-self.b[i] * float(self.A[i].reshape(-1, 1).T @ x))))
            hessian += ((1 - p) * p * self.A[i].reshape(-1, 1) @ self.A[i].reshape(-1, 1).T) / length
        return hessian

    def calculate_direction(self, H_hat, history_s, history_y, gradient):
        q = gradient
        alpha = [0 for _ in range(5)]
        rho = [1 / (history_y[i].T @ history_s[i]) for i in range(5)]
        for i in range(4, -1, -1):
            alpha[i] = rho[i] * history_s[i].T @ q
            q = q - alpha[i] * history_y[i]

        r = H_hat @ q
        for i in range(5):
            beta = rho[i] * history_y[i].T @ r
            r = r + (alpha[i] - beta) * history_s[i]
        return r

    # armijo 线搜索
    def armijo(self, x, grad):
        alpha = 5.0
        f_x = self.calculate_value(x)
        gd = float(grad.T @ (-grad))
        for _ in range(100):
            f_x_new = self.calculate_value(x - alpha * grad)
            if f_x_new <= f_x + 0.1 * alpha * gd:
                return alpha
            else:
                alpha *= 0.5
        return alpha

    # BB 步长
    def bb(self, iteration, y, s, x, grad):
        if iteration == 1:
            return self.opts['alpha0']
        else:
            alpha = float(abs((s.T @ s) / (s.T @ y))) if random.choice([True, False]) else float(
                abs((s.T @ y) / (y.T @ y)))
            f_x = self.calculate_value(x)
            gd = float(grad.T @ (-grad))
            for _ in range(100):
                f_x_new = self.calculate_value(x - alpha * grad)
                if f_x_new <= f_x + 0.1 * alpha * gd:
                    return alpha
                else:
                    alpha *= 0.5
            return alpha

    # wolfe 线搜索
    def wolfe(self, x, m, grad):
        if self.round < m:
            return self.opts['alpha0']
        alpha = 1.0
        f_x = self.calculate_value(x)
        gd = float(grad.T @ (-grad))
        for _ in range(100):
            new_x = x - alpha * grad
            f_x_new = self.calculate_value(new_x)
            grad_new = self.calculate_gradient(new_x)
            ngd = float(grad_new.T @ (-grad))
            if f_x_new <= f_x + 0.1 * alpha * gd:
                if ngd >= 0.9 * gd:
                    return alpha
                else:
                    alpha *= 1.5
            else:
                alpha *= 0.5
        return alpha

    #  优化
    def optimization(self):
        self.clear()
        index = self.ui.solutionSet.currentIndex()
        if self.A is None and self.b is None and self.ui.trainSet.currentIndex() == 0:
            QMessageBox.warning(self.ui, '警告', '请先获取数据！')
        else:
            if index == 0:
                if self.ui.trainSet.currentIndex() == 0:
                    self.gradSolution()
                    self.draw()
                else:
                    try:
                        self.showImage()
                    except:
                        QMessageBox.warning(self.ui, '警告', '没有相关图像！')
            elif index == 1:
                if self.ui.trainSet.currentIndex() == 0:
                    self.newtoonSolution()
                    self.draw()
                else:
                    try:
                        self.showImage()
                    except:
                        QMessageBox.warning(self.ui, '警告', '没有相关图像！')
            elif index == 2:
                if self.ui.trainSet.currentIndex() == 0:
                    self.L_BFGSolution(5)
                    self.draw()
                else:
                    try:
                        self.showImage()
                    except:
                        QMessageBox.warning(self.ui, '警告', '没有相关图像！')
            elif index == 3:
                if self.ui.trainSet.currentIndex() == 0:
                    self.trustregionSolution()
                    self.draw()
                else:
                    try:
                        self.showImage()
                    except:
                        QMessageBox.warning(self.ui, '警告', '没有相关图像！')

    # 梯度算法
    def gradSolution(self):
        self.ui.progressBar.show()
        alpha, x, self.round, self.maxit = 0, self.x0, 0, self.opts['maxit']  # 初始化参数
        grad = self.calculate_gradient(x)
        grad_norm = np.linalg.norm(grad)
        self.g_data = [grad_norm]  # 计算并存储梯度范数
        history_s, history_y = self.x0, grad  # 记录history_s和history_y，用于计算bb步长
        f_x = self.calculate_value(self.x0)
        self.f_data = [f_x]  # 计算并存储每一个迭代点的函数值
        while self.round < self.maxit and grad_norm > self.opts['gtol']:
            self.round += 1
            print(f"alpha_{self.round} = {alpha}, grad_norm_{self.round} = {grad_norm}, f_value_{self.round} = {f_x}")
            index = self.ui.stepSet.currentIndex()
            self.ui.progressBar.setValue(int(self.round * 100 / self.maxit))
            if index == 0:
                alpha = self.opts['alpha0']
            elif index == 1:
                alpha = self.armijo(x, grad)
            elif index == 2:
                alpha = self.bb(self.round, history_s, history_y, x, grad)
            elif index == 3:
                alpha = self.wolfe(x, 2, grad)
            new_x = x - alpha * grad  # 计算新的x值
            new_grad = self.calculate_gradient(new_x)  # 计算新的梯度值
            history_s, history_y = new_x - x, new_grad - grad  # 更新history_s和history_y，用于计算bb步长
            x, grad = new_x, new_grad  # 更新x和grad
            f_x = self.calculate_value(x)
            grad_norm = np.linalg.norm(grad)
            self.g_data.append(grad_norm)  # 存储每一个迭代点的梯度范数
            self.f_data.append(f_x)  # 存储每一个迭代点的函数值
        self.ui.progressBar.setValue(100)

    # 牛顿法
    def newtoonSolution(self):
        self.ui.progressBar.hide()
        alpha, x, self.round, self.maxit, grad = 0, self.x0, 0, self.opts['maxit'], self.calculate_gradient(
            self.x0)  # 初始化参数
        grad_norm, f_x = np.linalg.norm(grad), self.calculate_value(x)
        self.g_data, self.f_data = [grad_norm], [f_x]  # 计算并存储梯度范数和函数值

        while grad_norm > 0.01:  # 首先用梯度算法将迭代点更新到牛顿法收敛范围内
            self.round += 1
            print(f"alpha_{self.round} = {alpha}, grad_norm_{self.round} = {grad_norm}, f_value_{self.round} = {f_x}")
            alpha = self.wolfe(x, 2, grad)
            new_x = x - alpha * grad
            new_grad = self.calculate_gradient(new_x)
            x, grad = new_x, new_grad
            f_x = self.calculate_value(x)
            grad_norm = np.linalg.norm(grad)
            self.g_data.append(grad_norm)
            self.f_data.append(f_x)

        while self.round < self.maxit and grad_norm > self.opts['gtol']:
            self.round += 1
            print(f"alpha_{self.round} = {alpha}, grad_norm_{self.round} = {grad_norm}, f_value_{self.round} = {f_x}")
            H = self.calculate_hessian(x)  # 计算Hessian矩阵
            x = x - np.linalg.inv(H) @ grad  # 计算新的x值
            f_x = self.calculate_value(x)
            grad = self.calculate_gradient(x)
            grad_norm = np.linalg.norm(grad)
            self.g_data.append(grad_norm)  # 存储每一个迭代点的梯度范数
            self.f_data.append(f_x)  # 存储每一个迭代点的函数值

    # L-BFGS 算法
    def L_BFGSolution(self, m):
        x, self.round = self.x0, 0  # 初始化参数
        self.f_data, self.g_data, s, y = [], [], [], []
        for i in range(m):  # 前m步用固定步长的梯度算法填充列表
            self.round += 1
            f_x = self.calculate_value(x)
            grad = self.calculate_gradient(x)
            grad_norm = np.linalg.norm(grad)
            self.f_data.append(f_x)
            self.g_data.append(grad_norm)
            new_x = x - self.opts['alpha0'] * grad
            new_grad = self.calculate_gradient(new_x)
            s.append(new_x - x)
            y.append(new_grad - grad)
            x, grad = new_x, new_grad
            print(
                f"alpha_{self.round} = {self.opts['alpha0']}, grad_norm_{self.round} = {grad_norm}, f_value_{self.round} = {f_x}")

        length = len(self.x0)
        while self.round < self.opts['maxit'] and np.linalg.norm(grad) > self.opts['gtol']:
            self.round += 1
            H_hat = (s[-1].T @ y[-1]) / (y[-1].T @ y[-1]) * np.eye(length)  # 初始化Hessian矩阵的基础更新矩阵
            direction = -self.calculate_direction(H_hat, s, y, grad)  # 计算方向向量
            step = self.wolfe(x, m, grad)  # 使用wolfe准则计算步长
            new_x = x + step * direction  # 计算新的x值
            new_grad = self.calculate_gradient(new_x)  # 计算新的梯度值
            s.pop(0)
            s.append(new_x - x)
            y.pop(0)
            y.append(new_grad - grad)  # 更新存储列表
            x, grad = new_x, new_grad  # 更新x和grad
            f_x = self.calculate_value(x)
            grad_norm = np.linalg.norm(grad)
            self.f_data.append(f_x)
            self.g_data.append(grad_norm)  # 计算并存储每一个迭代点的函数值与梯度范数
            print(
                f"alpha_{self.round} = {step}, grad_norm_{self.round} = {grad_norm}, f_value_{self.round} = {f_x}")

    # 信赖域算法
    def trustregionSolution(self):
        x, self.round = self.x0, 0
        f_x = self.calculate_value(x)
        grad = self.calculate_gradient(x)
        grad_norm = np.linalg.norm(grad)
        self.g_data, self.f_data = [grad_norm], [self.calculate_value(x)]  # 计算并存储梯度范数和函数值
        gamma_1, gamma_2, eta, rho_1, rho_2, radius, radius_max = 0.25, 2, 0.2, 0.25, 0.75, 0.5, 20
        while self.round < 35 and grad_norm > self.opts['gtol']:
            self.round += 1
            print(f"radius_{self.round} = {radius}, grad_norm_{self.round} = {grad_norm}, f_value_{self.round} = {f_x}")
            hessian = self.calculate_hessian(x)
            direction = self.solve_direction(x, grad, hessian, radius)
            denominator = (self.calculate_value(x + direction) - self.calculate_value(x))
            numerator = self.m_function(grad, hessian, direction)
            rho = abs(denominator / numerator)
            if rho < rho_1:
                radius = gamma_1 * radius
            elif rho > rho_2 and np.linalg.norm(direction) == radius:
                radius = min(gamma_2 * radius, radius_max)
            if rho > eta:
                x = x + direction
                f_x = self.calculate_value(x)
                grad = self.calculate_gradient(x)
                grad_norm = np.linalg.norm(grad)
                self.g_data.append(grad_norm)
                self.f_data.append(self.calculate_value(x))

    def m_function(self, grad, hessian, d):
        part1 = grad.T @ d
        part2 = 0.5 * d.T @ hessian @ d
        return part1 + part2

    def solve_direction(self, x, grad, hessian, radius):
        s, r, p = self.x0, grad, -grad
        while True:
            temp1 = hessian @ p.reshape(-1, 1)
            temp2 = p.reshape(-1, 1).T @ temp1
            if float(p.reshape(-1, 1).T @ hessian @ p.reshape(-1, 1)) <= 0:
                tao = (radius - np.linalg.norm(s)) / (np.linalg.norm(p))
                s = s + tao * p
                return s
            alpha = np.linalg.norm(r) ** 2 / temp2
            s = s + float(alpha) * p
            if np.linalg.norm(s) >= radius:
                tao = (radius - np.linalg.norm(s)) / (np.linalg.norm(p))
                s = s + tao * p
                return s
            new_r = r + float(alpha) * np.squeeze(temp1)
            if np.linalg.norm(new_r) < 1e-2 * np.linalg.norm(r):
                return s
            beta = np.linalg.norm(new_r) ** 2 / np.linalg.norm(r) ** 2
            r = new_r
            p = -r + beta * p

    def draw(self):
        self.saveImage()
        self.showImage()

    def saveImage(self):
        dataIndex = self.ui.dataSet.currentIndex()
        data = [self.f_data, self.g_data,
                [(self.f_data[i] - self.f_star[dataIndex]) / self.f_star[dataIndex] for i in range(len(self.f_data))]]
        seed = ['value', 'grad', 'decline']
        title = ['$f(x_k)$', '$||g(x_k)||$', '$(f(x_k)-f(x^*))/f(x^*)$']
        for i in range(len(data)):
            plt.figure(figsize=(15, 5))
            plt.plot(data[i])
            solutionIndex = self.ui.solutionSet.currentIndex()
            stepIndex = (self.ui.stepSet.currentIndex() if solutionIndex == 0 else 0)
            plt.yscale('log')
            plt.xlabel('iteration')
            plt.title(title[i])
            plt.savefig(
                f'./picture/{self.dataSet[dataIndex]}_{self.solutionSet[solutionIndex]}_{self.stepSet[stepIndex]}_{seed[i]}.png')
            plt.close()
            file = open(
                f'./data/{self.dataSet[dataIndex]}_{self.solutionSet[solutionIndex]}_{self.stepSet[stepIndex]}_{seed[i]}.txt',
                'w')
            for line in data[i]:
                file.write(f'{line}\n')
            file.close()

    def showImage(self):
        dataIndex = self.ui.dataSet.currentIndex()
        solutionIndex = self.ui.solutionSet.currentIndex()
        stepIndex = self.ui.stepSet.currentIndex()
        if solutionIndex != 0:
            stepIndex = 0
        if self.ui.valueImage.isChecked():
            self.displayImage(
                f'./picture/{self.dataSet[dataIndex]}_{self.solutionSet[solutionIndex]}_{self.stepSet[stepIndex]}_value.png')
        if self.ui.gradImage.isChecked():
            self.displayImage(
                f'./picture/{self.dataSet[dataIndex]}_{self.solutionSet[solutionIndex]}_{self.stepSet[stepIndex]}_grad.png')
        if self.ui.declineImage.isChecked():
            self.displayImage(
                f'./picture/{self.dataSet[dataIndex]}_{self.solutionSet[solutionIndex]}_{self.stepSet[stepIndex]}_decline.png')

    def displayImage(self, image):
        width = self.ui.scrollArea.width() - 50
        label = QLabel()
        label.setScaledContents(True)
        picture = QPixmap(image)
        label.setPixmap(picture)
        label.setFixedSize(width, int(picture.height() * width / picture.width()))
        self.ui.verticalLayout_4.addWidget(label)
        self.labels.append(label)

    def clear(self):
        for label in self.labels:
            self.ui.verticalLayout_4.removeWidget(label)
            label.deleteLater()
        self.labels.clear()

    def changeUI(self):
        index = self.ui.solutionSet.currentIndex()
        if index == 0:
            self.ui.stepSet.show()
            self.ui.progressBar.show()
        else:
            self.ui.stepSet.hide()
            self.ui.progressBar.hide()

    def changeSize(self):
        width = self.ui.scrollArea.width() - 50
        for label in self.labels:
            picture = label.pixmap()
            label.setFixedSize(width, int(picture.height() * width / picture.width()))
