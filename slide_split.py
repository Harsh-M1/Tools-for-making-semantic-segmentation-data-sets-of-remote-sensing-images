import os
from osgeo import gdal
import numpy as np
from tqdm import tqdm

# 读取数据


def read_image(image_path, num_bands=None, selected_bands=None):
    dataset = gdal.Open(image_path)
    if dataset is None:
        print(f"Could not open image: {image_path}")
        return None
    else:
        if num_bands is None:
            num_bands = dataset.RasterCount
        image_data = []
        for i in range(1, num_bands + 1):
            if selected_bands is not None and i not in selected_bands:
                continue
            band = dataset.GetRasterBand(i)
            band_data = band.ReadAsArray()
            image_data.append(band_data)
        return np.array(image_data)

# 滑动裁剪


def sliding_crop(image, window_size=(512, 512), stride=256):
    height, width = image.shape[1], image.shape[2]

    # 计算需要填充的高度和宽度
    pad_height = 0
    pad_width = 0
    if height % window_size[0] != 0:
        pad_height = window_size[0] - (height % window_size[0])
    if width % window_size[1] != 0:
        pad_width = window_size[1] - (width % window_size[1])

    # 在图像右侧和下侧填充0值
    padded_image = np.pad(image, ((0, 0), (0, pad_height),
                          (0, pad_width)), mode='constant', constant_values=0)

    crops = []
    for y in range(0, height + pad_height - window_size[0] + 1, stride):
        for x in range(0, width + pad_width - window_size[1] + 1, stride):
            crop = padded_image[:, y:y+window_size[0], x:x+window_size[1]]
            crops.append(crop)
    return crops

# 保存数据


def save_crops(crops, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    existing_files = os.listdir(output_dir)
    existing_indices = set()
    for filename in existing_files:
        if filename.startswith("crop_") and filename.endswith(".tif"):
            index_str = filename.split("_")[1].split(".")[0]
            existing_indices.add(int(index_str))

    start_index = max(existing_indices) + 1 if existing_indices else 0

    for i, crop in enumerate(crops):
        output_path = os.path.join(output_dir, f"crop_{start_index + i}.tif")
        save_image(crop, output_path)


def save_image(image_data, output_path):
    num_bands, height, width = image_data.shape
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(output_path, width, height,
                            num_bands, gdal.GDT_Byte)
    for i in range(num_bands):
        dataset.GetRasterBand(i + 1).WriteArray(image_data[i])
    dataset.FlushCache()


if __name__ == "__main__":
    image_path = r"xxxx.tif"
    label_path = r"xxxx.tif"
    images = read_image(image_path)
    labels = read_image(label_path, 1)
    if images.shape[1:] == labels.shape[1:]:
        print("Images have same dimensions. Starting cropping...")
        images_crops = sliding_crop(images)
        labels_crops = sliding_crop(labels)
        # 保存裁剪后的图像
        save_crops(images_crops,
                   r"H:\Images")
        save_crops(labels_crops,
                   r"H:\Labels")
        print("Cropping done and crops saved!")
    else:
        print("Images have different dimensions. Cannot proceed with cropping.")
