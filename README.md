### PC版少前2, 一键长草, 兵棋推演, 活动体力扫荡, 竞技场, 尘烟, 要务

1. 直接使用PC版少前2, 可原生后台运行
2. 游戏帧率越高越好, 推荐120, 支持所有16:9分辨率, windows自动HDR必须关闭, 可以使用RTX HDR
3. 仅支持游戏语言为简体中文/或英文(但是可能有不少问题)
4. 主页背景需要使用暗色, 不能用白色背景, 不然识别不到文字.
5. QQ群1033950808 进群答案: 老王同学OK
6. 部分参数说明：

下图左侧为小活动,物资关卡显示则为**物资模式**,显示为**物资模式**则不用管,右侧为大活动,物资关卡显示为**铸碑者的黎明·上篇**,则需要填图中物资关卡名为**铸碑者的黎明**(不正确填写可能会影响活动代理逻辑)
<img width="5001" height="2066" alt="1765122815802" src="https://github.com/user-attachments/assets/ed261840-449a-46d4-8a07-f58382f3a779" />

![image](https://github.com/user-attachments/assets/6bd2ac34-fd40-4c74-9e8e-a0343818876d)

![image](https://github.com/user-attachments/assets/ae1ecd07-6608-478d-9226-40d4f8000a60)

### 绿色免安装版, 解压后双击ok-gf2.exe, 下载后可应用内更新

* [GitHub下载](https://github.com/ok-oldking/ok-gf2/releases), 免费网页直链, 不要点击下载Source Code,
  点击下载7z压缩包
* [Mirror酱下载渠道](https://mirrorchyan.com/zh/projects?rid=okgf2&source=okgf2readme), 国内网页直链, 下载需要购买CD-KEY,
  已有Mirror酱CD-KEY可免费下载
* [夸克网盘](https://pan.quark.cn/s/a1052cec4d13), 免费, 但需要注册并下载夸克网盘客户端


### Python 源码运行

```
#CPU版本, 使用openvino
pip install -r requirements.txt --upgrade #install python dependencies, 更新代码后可能需要重新运行
python main.py # run the release version
python main_debug.py # run the debug version
```

```
#CUDA版本, 使用paddle-gpu加速, 推荐N卡30系以上使用, 速度飞快, 但是将会增加1GB硬盘占用空间
pip install -r requirements-direct-ml.txt --upgrade #install python dependencies, 更新代码后可能需要重新运行
python main_direct_ml.py # run the release version
```
