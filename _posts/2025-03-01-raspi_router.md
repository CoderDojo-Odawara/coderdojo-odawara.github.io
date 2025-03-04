---
layout: single
title: CoderDojo 擬似無線LANルーターの構築
description: "raspberry pi 4 で無線LANアクセスポイントを構築した"
lang: ja_JP
header:
  overlay_image: /assets/images/x.png
  overlay_filter: 0.4
  caption: ""
tagline: "Bookwormの仕様に悪戦苦闘"
categories: 
- チャンピオン記録帳
tags:
- Raspberry Pi
- bookworm 
toc: false
last_modified_at: 2025-03-01
---


先日道場の開催場所候補をお借りした時に無線LANの環境が特殊でVLANを構築しないとかも、という感じだったので対策を考えてみた。  

丁度手元に使っていないRaspberry Pi 4Bが転がっていたのでこれを使って無線LANルーターを構築することに。

## 仮想デバイスの作成

```
sudo iw phy phy0 interface add ap0 type __ap
sudo ip link set ap0 address [wlan0と同じMACアドレス]
```
ここで `iw dev`をして仮想デバイスの `ap0` が作成されていることを確認。  
その後設定の永続化をするために

```
sudo vim /etc/udev/rules.d/99-ap0.rules
```

で新規ファイルを作成して

```
    SUBSYSTEM=="ieee80211", ACTION=="add|change", ATTR{macaddress}=="[wlan0と同じMACアドレス]", KERNEL=="phy0", \
    RUN+="/sbin/iw phy phy0 interface add ap0 type __ap", \
    RUN+="/bin/ip link set ap0 address [wlan0と同じMACアドレス]"
```

とし、リブートしてみたところ再起動後数秒はうまくいくのだけどもその後`ap0`が消えてしまうので  
別の方法を模索。(ここが一番時間かかった。。。)

最終的には  HOME ディレクトリに内容を記載したap.shを配置して

```
vim ~/.config/labwc/autostart
```
として自動起動用のファイルを作成、

```
 $HOME/ap.sh
```

とすることで解決。

## 仮想デバイスにアクセスポイント設定

```
 nmcli con add con-name hotspot ifname ap0 type wifi ssid "[決めたSSID]"
 nmcli con modify hotspot wifi-sec.key-mgmt wpa-psk
 nmcli con modify hotspot wifi-sec.proto rsn
 nmcli con modify hotspot wifi-sec.pairwise ccmp
 nmcli con modify hotspot wifi-sec.psk "[決めたパスワード]"
 nmcli con modify hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
 nmcli con modify hotspot ipv4.address 192.168.50.1/24
```

とルーター化をするために各種設定をして  

```
 nmcli connection up hotspot
```

とした。最後に  

```
sudo vim /etc/sysctl.conf
```

内容は  
/etc/sysctl.conf
{: .btn .btn--primary}
```
net.ipv4.ip_forward=1 //コメントを外す
```

とコメントを外して最後に  

```
sudo systemctl reboot --now
```

で無事機能していることを確認した。

###### 参考文献
1. [Raspberry Pi 5B(bookworm) アクセスポイント化＆ルータ化メモ](https://qiita.com/d-ebi/items/2b8e6113690f24487c3e)  
2. [Raspberry Pi OS BookwormでGUIアプリを自動起動させる3つの方法](https://qiita.com/mao172/items/4014ae9d8e1252ddde86)
