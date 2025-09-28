---
layout: single
title: Mincraft の代替環境について
description: "オープンソースのボクセルゲームエンジン"
lang: ja_JP
header:
  overlay_image: /assets/images/x.png
  overlay_filter: 0.4
  caption: ""
tagline: "オープンソースのボクセルゲームエンジンの環境を整備する。"
categories: 
- チャンピオン記録帳
tags:
- DojoPaas
- Luanti
toc: false
draft: true
last_modified_at: 2025-09-28
---

今月の頭から教育版マインクラフトのライセンス料が3倍となり、年間¥5,000-超級となったことを受け、CoderDojo 小田原としてはあまり積極的に推奨はできないよなぁ、ということで代替環境の導入を検討することに。  
  
調査した結果、Luantiというゲームエンジンが具合良さそう、ということで当Dojoではこちらを推奨することに決定した。  
[Luanti | Open source voxel game engine](https://www.luanti.org)   
  
試してみたところ、動作は軽快、寄せようと思えばMincraftっぽくもできる、MODも豊富で、あれ?全然こっちでよくね?ということで今月のDojoで紹介したところ新規でMineCraftをやりたくて参加してくれたニンジャが試してくれてこれで良い!と継続決定。  


別のニンジャも使ってくれそうで結構手応えを感じたのである程度ユーザーが増えてきたらMOD作成のハンズオンでオリジナルブロックを作ってみよう、とかやってみようかな。  

あとタイミング的にそろそろ良かろうとCoderDojo Japanとさくらインターネットさんが連携して提供して下さっているCoderDojoでサーバーを一台お借りしたのでそちらにLuantiのサーバーを建ててみた。
Minecraftサーバーだと到底動かないけどもLuanti サーバーであれば少なくとも数人規模であれば全然マルチできそうなのでしばらく運用して様子見かな。

以下サーバー構築の備忘録。

## 使用ポートの開放
DojoPaasは初期状態でLuantiサーバーで使用するUDP 30000が塞がれているのでポート解放をする必要がある。  

```shell
sudo iptables -A INPUT -p udp --dport 30000 -j ACCEPT
```
このままではサーバーが再起動されると設定がリセットされてしまうので永続化する。

```shell
sudo netfilter-persistent save
sudo netfilter-persistent reload
```
## 依存パッケージの準備
flatpak版をインストールしたりDockerのコンテナを入れても良いのだけど今回はソースからビルドすることとした。  
ということで必要な環境を準備する。

依存パッケージの導入
```shell
sudo apt install g++ ninja-build cmake libsqlite3-dev libcurl4-openssl-dev zlib1g-dev libgmp-dev libjsoncpp-dev libzstd-dev libncurses-dev
```
LuaJITのビルド
```shell
git clone https://github.com/LuaJIT/LuaJIT luajit
cd luajit
make amalg
```

## Luantiの環境構築
下準備が終わったのでLuantiの環境を構築する。
```
cd ~
git clone -b stable-5 --depth 1 https://github.com/luanti-org/luanti.git
cd luanti
```
```
mkdir build; cd build
cmake .. -G Ninja -DBUILD_CLIENT=0 -DBUILD_SERVER=1 -DRUN_IN_PLACE=1 -DBUILD_UNITTESTS=0 \
  -DLUA_INCLUDE_DIR=../../luajit/src/ -DLUA_LIBRARY=../../luajit/src/libluajit.a
ninja
```

ゲーム、MODは個別にzipを落としていくのが王道だろうけども手元の端末に使いたいworldとModが揃っていたので今回はSFTPでローカルの端末からコピーした。

luanti ディレクトリ内のmintest.conf.exampleをいい感じに修正してluanti.confとして保存する。default privesを修正してteleportとかflyとかを追加すると良いかも。

  
  
サーバーの起動はマニュアルでやりたいけどいちいち面倒な操作はしたくないので`~/`にサーバー起動用のshファイルを作成 
  
***startluanti.sh***
```shell
#!/bin/bash
cd luanti
screen -S luanti ./bin/luantiserver --gameid {Loadするゲーム名} --world worlds/{world名} --config ./luanti.conf
```
実行権限を付与
```shell
sudo chmod +x ./startluanti.sh
```

以降startluanti.shを実行することで　luanti screen 内でluanti serverが起動する。そのままだとLuantiスクリーンに入ったままなので`Ctrl + A -> Ctrl + D` でscreenから抜けたらsshを切ってもOK。

serverを終了させたい場合は
```shell
screen -r luanti
```
でluanti screenに切り替えて`Ctrl + C`　で終了し、`Ctrl + A ->Ctrl + D` でscreenから抜ける。

一旦worldを作ると関連ファイル群が作成され、その中のworld.mtを編集してloadするMODを設定する。今回はlwscratchを追加するので

```
# lwscratchを有効化
load_mod_lwscratch = true
```
と追加してserverを再度起動し、MODが適用されていることを確認。

## おまけ
生成されたworldsのディレクトリ内のauth.sqliteに登録したユーザーの権限情報が記録されている。serverのゲームマスターのIDにprivs権限を追記しておくとゲーム内でコントロールができるようになるのでおすすめ。
