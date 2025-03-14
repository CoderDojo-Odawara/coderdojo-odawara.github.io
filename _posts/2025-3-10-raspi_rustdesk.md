---
layout: single
title: Raspberry pi のリモートデスクトップ環境の見直し
description: "Raspberry Pi ConnectからRust Deskへ"
lang: ja_JP
header:
  overlay_image: /assets/images/x.png
  overlay_filter: 0.4
  caption: ""
tagline: "WaylandとX11を行ったり来たり"
categories: 
- チャンピオン記録帳
tags:
- Raspberry Pi
- bookworm 
- RustDesk
toc: false
last_modified_at: 2025-03-10
---

現状でRaspberry Piをカジュアルに操作する場合にはRaspberry Pi Connectを経由しているのだけども特にGUIでの操作をする場合にかなり動作が緩慢なので見直すことに。  
  
個人的にはRustDeskを好んで使っているのでこちらを採用することにした。  


```
wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash
```

でPi Appsを導入してRustDeskを選択インストールすることで諸々調整しながらインストールしてくれて便利.
ところがbookwormで標準採用しているwayland環境はまだExperimentalサポートでかなり不安定。  
  
と、いうことでX11環境で動作させる必要がある様子。  
  
困っていたところ、再起動無しで環境を切り替えるshellスクリプトを配布している方がいらっしゃったので有り難く利用させていただくことに。  

[RPI OS Bookworm – X11とwaylandをリブートなしで一発切り替えするコマンド](https://yagiful.com/blog/raspi-bookworm-switch/)

```
bash raspi-disp-switcher.sh x11
```
でうまく切り替え、RustDeskでの遠隔操作が可能になることを確認。  

＄HOME/.config/labwc/autostart
{: .btn .btn--primary}

###### 参考文献
1.[https://pi-apps.io/install-app/install-rustdesk-on-raspberry-pi/](https://pi-apps.io/install-app/install-rustdesk-on-raspberry-pi/)