import os
from osgeo import gdal 
from osgeo.gdalconst import GA_ReadOnly
from PIL import Image
from tqdm import tqdm
## 单波段tif格式转为8bit.png格式（用于标签转换）
def tif2png(input_folder,output_folder ):
    # 获取输入文件夹中的所有文件
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 循环处理每个文件
    for input_file in tqdm(input_files, desc="Converting"):
        input_path = os.path.join(input_folder, input_file)
        output_file = os.path.splitext(input_file)[0] + ".png"
        output_path = os.path.join(output_folder, output_file)

        ds = gdal.Open(input_path, GA_ReadOnly)
        if ds is None:
            print(f"无法打开影像文件: {input_path}")
            continue

        width = ds.RasterXSize
        height = ds.RasterYSize

        single_band = ds.GetRasterBand(1).ReadAsArray()

        # 将数据缩放到8位深度（0-255）
        min_value = single_band.min()
        max_value = single_band.max()
        scaled_data = ((single_band - min_value) / (max_value - min_value) * 255).astype('uint8')

        png_image = Image.fromarray(scaled_data)
        png_image.save(output_path, "PNG")

    print("处理完成")
    
if __name__ == "__main__":
    # 输入文件夹和输出文件夹路径
    input_folder = r"G:\mutilmode_data\ori_image_label\changhai\muldataset\labels_tif"
    output_folder = r"G:\mutilmode_data\ori_image_label\changhai\muldataset\labels_ori"
    tif2png(input_folder,output_folder )
