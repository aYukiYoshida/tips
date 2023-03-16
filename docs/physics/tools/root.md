# ROOT

(2019年10月24日時点での情報です)

CERNによって開発が行われている, データ解析環境および関連するライブラリ群.
グラフ作成のみならず、ヒストグラムの操作, 4元ベクトルの扱い, 実験データの可視化など, 高エネルギー物理学の研究に不可欠な要素が組み込まれている.
開発当初は素粒子実験のデータ解析用ソフトウェアとして構築されたが, 近年では高エネルギー宇宙物理学や天文学といった分野でも使用されている.

公式HPは[こちら](https://root.cern.ch/)

## インストール方法

### インストール環境

以下はmacOSでのインストール方法。
執筆者の環境は以下の通りです。

```txt
MacBook Pro (15-inch, 2018)
macOS 10.14.6
```

### 手順

1. インストールに必要なものの準備 (2020/02/24追記)
CERNの[Build Prerequisites](https://root.cern.ch/build-prerequisites#macosx)に記載されているものをインストールする。

1. cmakeのインストール
  ```shell
  % brew install cmake
  ```

1. gitでソースコードを取得
  ```shell
  % mkdir ~/tool/cern/
  % cd ~/tool/cern/
  % git clone https://github.com/root-project/root.git
  % git checkout -b v6-18-04 v6-18-04 #versionは最新を選択すること
  ```

1. build
`/usr/local/xray/root` というディレクトリにインストールする
  ```shell
  % mkdir cmake-build
  % cd cmake-build
  % cmake -DCMAKE_INSTALL_PREFIX=/usr/local/xray/root \\\\
    -DPYTHON_EXECUTABLE=/usr/local/bin/python3 \\\\
    -DPYTHON_INCLUDE_DIR=/usr/local/Cellar/python/3.7.4_1/Frameworks/Python.framework/Versions/3.7/Headers \\\\
    -DPYTHON_LIBRARY=/usr/local/Cellar/python/3.7.4_1/Frameworks/Python.framework/Versions/3.7/lib/libpython3.7.dylib ../../root \\\\
    ../../root
  % cmake --build .
  ```

1. install

    ```shell
    % cmake -DCMAKE_INSTALL_PREFIX=/usr/local/xray/root -P cmake_install.cmake
    ```

1. set environment

    ```shell
    % export ROOTSYS=/usr/local/xray/root
    % export PATH=$ROOTSYS/bin:$PATH
    % export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH
    % export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH
    ```

以上
