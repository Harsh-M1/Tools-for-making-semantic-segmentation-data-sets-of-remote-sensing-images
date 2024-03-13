import os
from osgeo import gdal 
from osgeo.gdalconst import GA_ReadOnly
from PIL import Image
from tqdm import tqdm
def tif2jpg(input_folder,output_folder ):
    # 获取输入文件夹中的所有文件
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 循环处理每个文件
    for input_file in tqdm(input_files, desc="Converting"):
        input_path = os.path.join(input_folder, input_file)
        output_file = os.path.splitext(input_file)[0] + ".jpg"
        output_path = os.path.join(output_folder, output_file)

        ds = gdal.Open(input_path, GA_ReadOnly)
        if ds is None:
            print(f"无法打开影像文件: {input_path}")
            continue

        width = ds.RasterXSize
        height = ds.RasterYSize

        red_band = ds.GetRasterBand(1).ReadAsArray()
        green_band = ds.GetRasterBand(2).ReadAsArray()
        blue_band = ds.GetRasterBand(3).ReadAsArray()

        rgb_image = Image.new('RGB', (width, height))
        rgb_data = []

        for y in range(height):
            row = []
            for x in range(width):
                red = red_band[y][x]
                green = green_band[y][x]
                blue = blue_band[y][x]
                row.append((red, green, blue))
            rgb_data.append(row)

        rgb_image.putdata([pixel for row in rgb_data for pixel in row])
        rgb_image.save(output_path, "JPEG")

    print("处理完成")
if __name__ == "__main__":
	# 输入文件夹和输出文件夹路径
	input_folder = r"G:\ocean_yangzhi_data\CNRaft_dataset\Images_tif"
	output_folder = r"G:\ocean_yangzhi_data\CNRaft_dataset\Images"
	tif2jpg(input_folder,output_folder)