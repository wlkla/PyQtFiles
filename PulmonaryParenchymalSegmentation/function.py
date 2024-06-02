from main import *
from common import *
from packages import *


class Controller:
    def __init__(self):
        self.ui = MainWindow()
        self.ui.show()
        self.ui.pushButton.clicked.connect(self.pulmonary_parenchymal_segmentation)

    def pulmonary_parenchymal_segmentation(self):
        lstFilesDCM = os.listdir(dcm_dir)
        lstFilesDCM.sort(key=lambda x: int(x.split('-')[-1].split('.')[0]))
        RefDs = pydicom.read_file(os.path.join(dcm_dir, lstFilesDCM[0]))
        (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
        ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
        spacing = np.array(ConstPixelSpacing, dtype=float)[::-1]
        Slices_info = get_CT_info(dcm_dir)
        img_org = get_pixels_hu(Slices_info)
        binary_mask1, binary_mask2, has_lung = extract_lung(img_org, spacing)
        maskL = np.where(binary_mask1[:] == 1., 255, 0)
        maskR = np.where(binary_mask2[:] == 1., 255, 0)
        maskRL = maskL + maskR
        length = maskRL.shape[0]

        save_pic(maskRL, length)
        self.display_pic(length)
        self.load3DModel()

    def display_pic(self, length):
        for i in range(length):
            _label = MyLabel(os.path.join(save_path, "mask_{}.png".format(i + 1)))
            self.ui.verticalLayout_3.addWidget(_label)

    def load3DModel(self):
        vtkWidget = QVTKRenderWindowInteractor()
        vtkWidget.Initialize()
        self.ui.horizontalLayout_6.addWidget(vtkWidget)
        PNG_Reader = vtk.vtkPNGReader()
        PNG_Reader.SetNumberOfScalarComponents(1)
        PNG_Reader.SetFileDimensionality(2)
        PNG_Reader.SetDataExtent(0, 511, 0, 511, 1, 89)
        PNG_Reader.SetFilePrefix(name_prefix[0])
        PNG_Reader.SetFilePattern("%s%d.png")
        PNG_Reader.Update()  # type: ignore
        PNG_Reader.SetDataByteOrderToLittleEndian()
        spacing = [1.0, 1.0, 2.5]
        PNG_Reader.GetOutput().SetSpacing(spacing)
        gauss = vtk.vtkImageGaussianSmooth()
        gauss.SetInputConnection(PNG_Reader.GetOutputPort())  # type: ignore
        gauss.SetStandardDeviations(1.0, 1.0, 1.0)
        gauss.SetRadiusFactors(1.0, 1.0, 1.0)
        gauss.Update()

        contour = vtk.vtkMarchingCubes()
        gauss.GetOutput().SetSpacing(spacing)
        contour.SetInputConnection(gauss.GetOutputPort())  # type: ignore
        contour.ComputeNormalsOn()
        contour.SetValue(0, 100)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(contour.GetOutputPort())  # type: ignore
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 1, 1)

        renderer = vtk.vtkRenderer()
        renderer.SetBackground([1.0, 1.0, 1.0])  # type: ignore
        renderer.AddActor(actor)

        vtkWidget.GetRenderWindow().AddRenderer(renderer)
        vtkWidget.Start()
