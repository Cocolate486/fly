## 用vscode請按ctrl+shift+V預覽

先在windows上安裝：

[Qground_V_4.4.2](https://github.com/mavlink/qgroundcontrol/releases?page=1),

[WSL](https://learn.microsoft.com/zh-tw/windows/wsl/install),
```powershell
wsl --install
wsl --install -d Ubuntu-20.04
#安裝wsl，並安裝Ubuntu
```

[VScode](https://code.visualstudio.com/)

再按照line上的第一個ppt來做[跳到基本準備與PX4環境安裝](#基本準備與px4環境安裝)


安裝玩ROS系統後，要在WSL中下載vscode，，後續在WSL中開啟vscode也是用這個指令，
```bash
code .
```
也需要在WSL中安裝Qground
```bash
wget https://github.com/mavlink/qgroundcontrol/releases/download/v4.4.2/QGroundControl.AppImage 
#從網上下載連結的檔案
chmod +x QGroundControl.AppImage
#將檔案當成程式來執行
./QGroundControl.AppImage
#啟動Qground，後續啟動也是用這個
```

調試參考[PX4官網連結](https://docs.px4.io/main/en/config_mc/)，但基本上只需要先調試遙控和電池

## 無人機韌體重刷步驟


PX4韌體重刷版本要選1.13.3的[px4_fmu-v6c_default](https://github.com/PX4/PX4-Autopilot/releases?page=3)


1.參考[官網步驟](https://docs.px4.io/main/zh/config/firmware.html)

2.選PX4的那個選項，但我們要自定義安裝，所以下面那個選單選Custom Firmware file後點OK

3.選擇我們下載的那個PX4版本(px4_fmu-v6c_default)後點確認


## 遙控的調試(未完成)

1.將無人機用type-c的線連接到電腦，並打開Qground

2.確認連接後，用尖物去點無人機上遙控的reset鍵兩次，並開啟控制器

3.參考[官網步驟](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/setup_view/radio.html)

4.點下[圖中](https://docs.qgroundcontrol.com/master/assets/radio_start_setup.ojXs6A5h.jpg)的Colibrate和next後，按照[圖中](https://docs.qgroundcontrol.com/master/assets/radio_sticks_throttle.CURqTjK4.jpg)右邊兩個搖桿的指示去做



## 電池的調試


1.將無人機用type-c的線連接到電腦，並打開Qground，且電池黃色接頭已連上無人機

2.確認連接後，將電池選項輸入4(我們的電池上有4S指的是4顆合一)


## 數控的連接

1.先去安裝[usbip](https://github.com/dorssel/usbipd-win/releases?ref=geekbits)

```bash
usbipd
#確認是否安裝成功，可列出所有可用指令
usbipd list
#列出usb port，確認無人機的序列號(名稱為USB Serial Converter的)，例：2-1 USB Serial Converter，就為2-1
usbipd bind -b 2-1
#綁定2-1連接的USB裝置，無輸出正常
usbipd attach -b 2-1 -w Ubuntu-20.04
#將綁定的2-1使用在Ubuntu-20.04中，要先關閉Qground的連接否則會報錯
#無紅字為成功
```

2.另開一個cmd並開啟Ubuntu
```bash
wsl --install -d Ubuntu-20.04
```

## 基本準備與PX4環境安裝

```bash
cd ~
#切換到使用者的主目錄，確保後續操作在熟悉且可寫的環境中。
sudo apt update
#更新套件清單，確保安裝的是最新版本。
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
#下載 PX4 自動駕駛程式碼，--recursive 表示也會下載子模組（如 MAVLink、Firmware 等）。
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh --no-sim-tools --no-nuttx
#執行 PX4 的 Ubuntu 安裝腳本，跳過模擬器與 NuttX（嵌入式 RTOS）相關工具，表示你可能只需要 ROS 與 MAVROS 的部分。
sudo apt-get install protobuf-compiler libeigen3-dev libopencv-dev -y
#安裝 PX4 所需的函式庫：
#protobuf-compiler: 用於訊息序列化
#libeigen3-dev: 線性代數庫
#libopencv-dev: 電腦視覺函式庫
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
#加入 ROS 軟體源，$(lsb_release -sc) 會自動填入你的 Ubuntu 版本（如 focal）。
sudo apt install curl
#安裝 curl，用來下載 ROS 的 GPG 金鑰。
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
#加入 ROS 軟體源的驗證金鑰，確保來源安全。
sudo apt update
sudo apt install ros-noetic-desktop-full
#更新套件清單並安裝完整的 ROS Noetic 桌面版（含 RViz、Gazebo、常用工具）。
echo "alias ros1='source /opt/ros/noetic/setup.bash'" >> ~/.bashrc
source ~/.bashrc
ros1
#建立 ros1 別名，快速載入 ROS 環境變數。
```

## 安裝 ROS 工具與初始化 rosdep

```bash
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
sudo apt install python3-rosdep
#安裝 ROS 開發工具與依賴管理工具。
sudo rosdep init
rosdep update
#初始化 rosdep，用來自動安裝 ROS 套件依賴。
roscore
Ctrl + C
#啟動 ROS 核心，確認 ROS 安裝成功。按 Ctrl + C 結束。
sudo apt-get install ros-${ROS_DISTRO}-mavros ros-${ROS_DISTRO}-mavros-extras ros-${ROS_DISTRO}-mavros-msgs
#安裝 MAVROS 套件（PX4 與 ROS 的橋接器），${ROS_DISTRO} 通常是 noetic。
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
sudo bash ./install_geographiclib_datasets.sh
#安裝地理資料集（如地球模型），MAVROS 需要用來處理 GPS 與地理座標。
```

## 要先安裝catkin套件

```bash
sudo apt update
sudo apt install python3-catkin-tools
#安裝catkin套件
```

## 建立 catkin 工作區並編譯 MAVROS 原始碼

```bash
sudo apt-get install python3-catkin-tools python3-rosinstall-generator -y
sudo apt install ros-noetic-unique-id
#安裝 ROS 編譯工具與 unique-id 套件（MAVROS 依賴）。
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin init 
wstool init src
#建立並初始化 catkin 工作區與 wstool（管理多個 ROS 套件）。
rosinstall_generator --rosdistro kinetic mavlink | tee /tmp/mavros.rosinstall 
rosinstall_generator --upstream mavros --deps | tee -a /tmp/mavros.rosinstall
#產生 MAVROS 與 MAVLink 的安裝清單，雖然指定 kinetic，但後續會切換到 noetic 分支。
wstool merge -t src /tmp/mavros.rosinstall
wstool update -t src -j4
#將清單合併並下載原始碼（使用 4 執行緒加速）。
cd ~/catkin_ws/src/mavlink
git fetch origin
git checkout -b noetic_patch origin/patches/release/noetic/mavlink
#切換到 MAVLink 的 noetic 修補分支，確保相容性。
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -y
catkin build
source devel/setup.bash
#安裝所有依賴並編譯工作區，最後載入環境變數。
```

## 開機後啟動環境並測試

```bash
ros1
source ~/catkin_ws/devel/setup.bash
#載入 ROS Noetic 的環境
echo $ROS_DISTRO
#如果輸出是 noetic，代表你已經載入 ROS Noetic 的環境。
#如果是空的或沒有輸出，表示你還沒執行 ros1 或 source /opt/ros/noetic/setup.bash。
```