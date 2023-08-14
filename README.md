# segaut
使用opencv完成的图像分割和目标检测数据增强工具

完成的功能
1. 根据json标记文件解析为yolo的txt格式，并将其中的类别保存为yaml格式
2. 根据yolo格式的标记文件将图片中的标记部分剪切下来并保存为png格式图片
3. 将一张png格式图片粘贴到新的背景图片上，并同时输出分割和检测的yolo格式标记文件
4. 可视化分割和检测的标记文件
5. streamlit 的网页端

Segmentation and Object Detection's Data Augmentation Tool using OpenCV

Current Functionality
Transfer JSON's label to YOLO's label (txt), and generate a yaml file with all categories.
Cut the original image with YOLO's label and save it as a PNG image.
Paste the PNG image into a new background image and generate two new txt files for segmentation's label and object detection's label.
Visualize the segmentation's label and object detection's label.
Segaut's web using Streamlit.
