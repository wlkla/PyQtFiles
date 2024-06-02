from PyQt5.QtGui import QPainter

from packages import *


class RotatedLabel(QLabel):
    def __init__(self, angle, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.angle = angle

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        painter.drawText(int(-self.width() * 2.8), int(-self.height() / 2), self.width() * 6, self.height(),
                         Qt.AlignCenter, self.text())


class MyLabel(QWidget):
    def __init__(self, pic):
        super().__init__()
        self.pic = pic
        self.old_pic = pic
        self.new_pic = pic
        self.resize(520, 520)
        self.setMinimumSize(QSize(520, 520))
        self.setMaximumSize(QSize(520, 520))
        self.label = QLabel(self)
        self.label.setGeometry(QRect(4, 4, 512, 512))
        self.label.setMinimumSize(QSize(512, 512))
        self.label.setMaximumSize(QSize(512, 512))
        self.label.setObjectName("label")
        self.label.setPixmap(QPixmap(self.old_pic))
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(200, 20, 93, 28))
        self.pushButton.setStyleSheet("border: 1px solid white;\n"
                                      "color:white;\n"
                                      "background-color: black;\n"
                                      "font: 10pt \"华文新魏\";\n"
                                      "border-radius:5px;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("计算面积")
        self.pushButton.clicked.connect(self.calculate_area)  # type: ignore
        self.label_2 = RotatedLabel(270, self)
        self.label_2.setGeometry(QRect(40, 140, 31, 241))
        self.label_2.setStyleSheet("border: 1px solid white;\n"
                                   "color:white;\n"
                                   "background-color: black;\n"
                                   "font: 10pt \"华文新魏\";\n"
                                   "border-radius:5px;")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Lung area: ")

        self.pushButton.hide()
        self.label_2.hide()

    def enterEvent(self, event):
        if self.old_pic == self.new_pic:
            self.pushButton.show()
        self.label.setPixmap(QPixmap(self.new_pic))

    def leaveEvent(self, event):
        if self.old_pic == self.new_pic:
            self.pushButton.hide()
            self.label_2.hide()
            self.label.setPixmap(QPixmap(self.old_pic))

    def calculate_area(self):
        self.pushButton.hide()
        mask = plt.imread(self.pic)
        contours = find_contours(mask, 0.5)
        fig, ax = plt.subplots()
        ax.imshow(mask, interpolation='nearest', cmap=plt.cm.gray)  # type: ignore
        for contour in contours:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
        lung_area = np.sum(mask)
        self.label_2.setText(f"Lung area: {lung_area}")
        self.label_2.show()
        self.new_pic = fig2img(fig)
        self.label.setPixmap(QPixmap(self.new_pic))
        plt.close(fig)


def save_segmentation(binary_mask, file_name):
    np.save(file_name, binary_mask)


def extract_main(binary_mask, cover=0.95):
    for i in range(binary_mask.shape[0]):
        slice_binary = binary_mask[i]
        _label = measure.label(slice_binary)
        properties = measure.regionprops(_label)
        properties.sort(key=lambda x: x.area, reverse=True)
        areas = [prop.area for prop in properties]
        count = 0
        area_sum = 0
        area_cover = np.sum(areas) * cover
        while area_sum < area_cover:
            area_sum += areas[count]
            count += 1
        slice_filter = np.zeros(slice_binary.shape, dtype=bool)
        for j in range(count):
            min_row, min_col, max_row, max_col = properties[j].bbox
            slice_filter[min_row:max_row, min_col:max_col] |= \
                properties[j].convex_image
        binary_mask[i] = binary_mask[i] & slice_filter
    _label = measure.label(binary_mask)
    properties = measure.regionprops(_label)
    properties.sort(key=lambda x: x.area, reverse=True)
    binary_mask = (_label == properties[0].label)

    return binary_mask


def fill_2d_hole(binary_mask):
    for i in range(binary_mask.shape[0]):
        slice_binary = binary_mask[i]
        _label = measure.label(slice_binary)
        properties = measure.regionprops(_label)
        for prop in properties:
            min_row, min_col, max_row, max_col = prop.bbox
            slice_binary[min_row:max_row, min_col:max_col] |= \
                prop.filled_image
        binary_mask[i] = slice_binary

    return binary_mask


def separate_two_lung(binary_mask, spacing, max_iter=22, max_ratio=4.8):
    found = False
    iter_count = 0
    eroded1 = None
    eroded2 = None
    binary_mask_full = np.copy(binary_mask)
    while not found and iter_count < max_iter:
        _label = measure.label(binary_mask, connectivity=2)
        properties = measure.regionprops(_label)
        properties.sort(key=lambda x: x.area, reverse=True)
        if len(properties) > 1 and \
                properties[0].area / properties[1].area < max_ratio:
            found = True
            eroded1 = (_label == properties[0].label)
            eroded2 = (_label == properties[1].label)
        else:
            binary_mask = scipy.ndimage.binary_erosion(binary_mask)  # type: ignore
            iter_count += 1
    if found:
        distance1 = scipy.ndimage.distance_transform_edt(~eroded1, sampling=spacing)  # type: ignore
        distance2 = scipy.ndimage.distance_transform_edt(~eroded2, sampling=spacing)  # type: ignore

        binary_mask1 = binary_mask_full & (distance1 < distance2)
        binary_mask2 = binary_mask_full & (distance1 > distance2)

        binary_mask1 = extract_main(binary_mask1)
        binary_mask2 = extract_main(binary_mask2)
    else:
        binary_mask1 = binary_mask_full
        binary_mask2 = np.zeros(binary_mask.shape).astype('bool')
    binary_mask1 = fill_2d_hole(binary_mask1)
    binary_mask2 = fill_2d_hole(binary_mask2)

    return binary_mask1, binary_mask2


def binarize(image, spacing, intensity_thread=-600, sigma=1.0, area_thread=30.0,
             even_thread=0.99, corner_side=10):
    binary_mask = np.zeros(image.shape, dtype=bool)
    side_len = image.shape[1]
    grid_axis = np.linspace(-side_len / 2 + 0.5, side_len / 2 - 0.5, side_len)
    x, y = np.meshgrid(grid_axis, grid_axis)
    distance = np.sqrt(np.square(x) + np.square(y))
    nan_mask = (distance < side_len / 2).astype(float)
    nan_mask[nan_mask == 0] = np.nan
    for i in range(image.shape[0]):
        slice_raw = np.array(image[i]).astype('float32')
        num_uniq = len(np.unique(slice_raw[0:corner_side, 0:corner_side]))
        if num_uniq == 1:
            slice_raw *= nan_mask
        slice_smoothed = scipy.ndimage.gaussian_filter(slice_raw, sigma, truncate=2.0)  # type: ignore
        slice_binary = slice_smoothed < intensity_thread
        _label = measure.label(slice_binary)
        properties = measure.regionprops(_label)
        label_valid = set()
        for prop in properties:
            area_mm = prop.area * spacing[1] * spacing[2]
            if area_mm > area_thread and prop.eccentricity < even_thread:
                label_valid.add(prop.label)
        slice_binary = np.in1d(_label, list(label_valid)).reshape(_label.shape)
        binary_mask[i] = slice_binary

    return binary_mask


def corner_label_tool(_label):
    return {_label[0, 0, 0], _label[0, 0, -1], _label[0, -1, 0], _label[0, -1, -1], _label[-1, 0, 0],
            _label[-1, 0, -1], _label[-1, -1, 0], _label[-1, -1, -1]}


def exclude_corner_middle(_label):
    mid = int(_label.shape[2] / 2)
    corner_label = corner_label_tool(_label)
    middle_label = {_label[0, 0, mid], _label[0, -1, mid], _label[-1, 0, mid], _label[-1, -1, mid]}
    for temp in corner_label:
        _label[_label == temp] = 0
    for temp in middle_label:
        _label[_label == temp] = 0

    return _label


def volume_filter(_label, spacing, vol_min=0.2, vol_max=8.2):
    properties = measure.regionprops(_label)
    for prop in properties:
        if prop.area * spacing.prod() < vol_min * 1e6 or \
                prop.area * spacing.prod() > vol_max * 1e6:
            _label[_label == prop.label] = 0

    return _label


def exclude_air(_label, spacing, area_thread=3e3, dist_thread=62):
    y_axis = np.linspace(-_label.shape[1] / 2 + 0.5, _label.shape[1] / 2 - 0.5,
                         _label.shape[1]) * spacing[1]
    x_axis = np.linspace(-_label.shape[2] / 2 + 0.5, _label.shape[2] / 2 - 0.5,
                         _label.shape[2]) * spacing[2]
    y, x = np.meshgrid(y_axis, x_axis)
    distance = np.sqrt(np.square(y) + np.square(x))
    distance_max = np.max(distance)
    vols = measure.regionprops(_label)
    label_valid = set()
    for vol in vols:
        single_vol = (_label == vol.label)
        slice_area = np.zeros(_label.shape[0])
        min_distance = np.zeros(_label.shape[0])
        for i in range(_label.shape[0]):
            slice_area[i] = np.sum(single_vol[i]) * np.prod(spacing[1:3])  # type: ignore
            min_distance[i] = np.min(single_vol[i] * distance + (1 - single_vol[i]) * distance_max)  # type: ignore
            if np.average([min_distance[i] for i in range(_label.shape[0])
                           if slice_area[i] > area_thread]) < dist_thread:
                label_valid.add(vol.label)
    binary_mask = np.in1d(_label, list(label_valid)).reshape(_label.shape)
    has_lung = len(label_valid) > 0

    return binary_mask, has_lung


def fill_hole(binary_mask):
    _label = measure.label(~binary_mask)
    corner_label = corner_label_tool(_label)
    binary_mask = ~np.in1d(_label, list(corner_label)).reshape(_label.shape)

    return binary_mask


def extract_lung(image, spacing):
    binary_mask = binarize(image, spacing)
    _label = measure.label(binary_mask, connectivity=1)
    _label = exclude_corner_middle(_label)
    _label = volume_filter(_label, spacing)
    binary_mask, has_lung = exclude_air(_label, spacing)
    binary_mask = fill_hole(binary_mask)
    binary_mask1, binary_mask2 = separate_two_lung(binary_mask, spacing)

    return binary_mask1, binary_mask2, has_lung


def load_itk_image(filename):
    itk_image = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itk_image)
    numpyOrigin = np.array(list(reversed(itk_image.GetOrigin())))
    numpySpacing = np.array(list(reversed(itk_image.GetSpacing())))

    return numpyImage, numpyOrigin, numpySpacing


def resample(image, spacing, new_spacing=None, order=1):
    if new_spacing is None:
        new_spacing = [1.0, 1.0, 1.0]
    new_shape = np.round(image.shape * spacing / new_spacing)
    resample_spacing = spacing * image.shape / new_shape
    resize_factor = new_shape / image.shape
    image_new = scipy.ndimage.zoom(image, resize_factor, mode='nearest', order=order)  # type: ignore

    return image_new, resample_spacing


def get_CT_info(src_dir):
    Slices = []
    for file in os.listdir(src_dir):
        if file.endswith('.dcm'):
            _slice = pydicom.read_file(src_dir + '/' + file)
            Slices.append(_slice)
    Slices.sort(key=lambda x: int(x.InstanceNumber))

    return Slices


def get_pixels_hu(slices):
    images = np.stack([s.pixel_array for s in slices])
    images_temp = images
    images_temp = images_temp.astype("int32")
    for slice_number in range(len(slices)):
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope
        images_temp[slice_number] = slope * images_temp[slice_number] + intercept

    return images_temp


def fig2img(fig):
    fig.canvas.draw()

    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)  # type: ignore
    buf.shape = (w, h, 4)
    buf = np.roll(buf, 3, axis=2)
    image = QImage(buf, w, h, QImage.Format_ARGB32)

    return QPixmap.fromImage(image)


def save_pic(maskRL, length):
    for i in range(length):
        arr = maskRL[i, :, :]
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plt.imsave(os.path.join(save_path, "mask_{}.png".format(i + 1)), arr, cmap='gray')
        img = Image.open(os.path.join(save_path, "mask_{}.png".format(i + 1)))
        img = img.convert('1')
        img.save(os.path.join(save_path, "mask_{}.png".format(i + 1)))
