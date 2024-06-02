import os
import sys
import vtk
import pydicom
import numpy as np
import scipy.ndimage
from PIL import Image
import SimpleITK as sitk
from window import Ui_Form
from skimage import measure
from scipy.ndimage import label
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QSize, QRect, Qt
from skimage.measure import find_contours
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QApplication
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

dcm_dir = r'./lungCT'
save_path = r'./mask'
name_prefix = ['mask/mask_']
