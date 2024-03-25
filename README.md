# Tools-for-making-semantic-segmentation-data-sets-of-remote-sensing-images
The warehouse is used for making related tools for semantic segmentation data of remote sensing images, including: 1-.tif format remote sensing image and label image cropping (sliding cropping) Images and labels in 2-.tif format are converted to. jpg and. png formats. 3-label(.png format) is changed from 0-255 to gray values of 0, 1 and 2. ......

# 该仓库用于遥感影像语义分割数据制作相关工具
包括：

1-.tif格式遥感影像及label图片裁剪（滑动裁剪）

2-.tif格式影像和标签转为.jpg和.png格式

3-label（.png格式）由0-255转为灰度值0、1、2......

# 工具介绍

image_split -- 影像裁剪
tif2jpg/tif2png -- 将.tif格式影像转换为jpg或png格式
label2grey -- 将png格式的label标签转换为网络训练所使用的灰度图片
