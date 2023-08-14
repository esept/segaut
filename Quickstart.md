segaut 是一个使用 opencv 完成的针对分割和目标识别的数据增强工具

# 快速使用
### 方法1
```python
import segaut as sa
sal = sa.Saline(output_path)
self.clean_output() # 清空之前的文件夹
self.load_dataset(
    label_path, #json文件路径 
    image_path # 原图片路径
)
self.cut_labeled(
    img_path = None, # 原图片路径
    label_path = None # txt 格式 label 路径
)
self.merge_cut_to_new(
    new_imgs,# 新图片保存路径
    background_img, # 新背景图片路径
    nbs = 10 # 新图片数量
)
```
### 方法2
```python
sas = sa.Saline()
sas.run(
    dataset_path,  #json文件路径 
    image_path,# 原图片路径
    new_img_path,# 新背景图片路径
    nbs = 10 # 新图片数量
)
sas.see() # 可视化分割 label
sas.see(task="det") # 可视化目标识别 label
```
### 方法 3
```python
stviz = sa.Stviz() 
stviz.run_saline()
# 保存在 stmain.py 中
# 命令行中 : python -m streamlit run stmain.py
```


# segaut 的理论方法:
1. 使用 opencv 将图片的被分割区域剪切下来,保存为四通道的 png 图片,非被分割区域为透明
2. 将剪切下的图片二值化处理,二值化图片与新背景图片的二值化图片做粘贴,原图与新背景图片做粘贴
3. 将两张二值化粘贴的图片使用 opencv 的边缘处理,将图片的白色部分的坐标提取出来,并保存为新分割数据集的标记文件

# 类的功能
```python
import segaut as sa
```
## Dataset 
将 json 文件解析成 txt 文件,并将 json 中的不同类别组合成 yaml 文件
```python
sad = sa.Dataset(output_path) # 输出的总文件夹
sad.load_json(
    json_path, # json 的路径
    store_folder, # 保存 txt 文件的文件夹
    stviz # 是否使用了 streamlit 的网页端
)
# yaml 文件在 output_path 中
```

## Augmentator 
使用 txt 格式的标记数据剪切图片
```python
saa = sa.Augmentator(output_path)
saa.cut(img_path, # 被剪切的图片的文件夹
        label_path, # 被剪切的图片的标记数据的文件夹
        stviz = None # 是否使用了 streamlit 的网页端
)
# 剪切完成的图片保存在 output_path/cutted/ 文件夹中
```
将被减下的图片和新背景图片粘贴
```python
saa = sa.Augmentator(output_path)
saa.merge(
    cutted_path, # 新图片路径
    paste_path, # 被减下的图片的路径(png 图片路径)
    nbs = 100, # 生成的图片的数量
    stviz = None # 是否使用了 streamlit 的网页端
)
# 粘贴完成的图片保存在merged_imgs,标签保存在merged_det(识别),merged_seg(分割)
```

## Stviz 
segaut 的 web 端(使用 streamlit)
```python
stviz = sa.Stviz() 
stviz.run_saline()
```

## Visualizer
可视化标签
```python
sav = sa.Visualizer(output_path)
sav.show_label(
    label_path, # 标签路径
    img_path, # 图片路径
    Task # = [seg,det]
)
```

## Tool
工具类,每个方法有具体注释