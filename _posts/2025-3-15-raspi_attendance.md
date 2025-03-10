---
layout: single
title: 出席簿の作成
description: "raspberry pi 4 でNode-REDを利用"
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
draft: true
last_modified_at: 2025-03-31
---

CoderDojo 伊勢原で実施しているNFCタグを読み取って出席管理するシステムが欲しい!ということで、  
せっかくなのでNode-REDの勉強がてら作ってみた。

## 全体構想



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

https://qiita.com/nanbuwks/items/348aa1849a12079d75cd
https://note.com/rei_chemistry/n/ne50dad509570
https://ja.stackoverflow.com/questions/99775/%E3%83%A9%E3%82%BA%E3%83%91%E3%82%A4%E3%81%ABnfcpy%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%97%E3%81%9F%E3%81%84
