---
layout: single
title: "DojoPaaS用のLuantiサーバー構築スクリプトを作ってました。"
description: "LuantiをほかのDojoでも試しやすいように"
lang: ja_JP
header:
  overlay_image: /assets/images/x.png
  overlay_filter: 0.4
  caption: ""
tagline: ""
categories:
- チャンピオン記録帳
tags:
- DojoPaaS
- Luanti
toc: false
last_modified_at: 2026-06-01
---

以前、DojoPaaSにLuantiサーバーを建てた話を書きました。ニンジャたちが同じワールドで遊べるようになったのはよかったのですが、構築するときはパッケージを入れたり、Luantiをビルドしたり、ポートを開けたりと、そこそこ手順があります。

自分でまた最初から建てるときにも困りそうです。せっかくなので作業をスクリプトにまとめ、GitHubで公開したのですがこちらで記事にすることを忘れてたので今更ながらご紹介です。

[DojoPaaS_Luanti_Server](https://github.com/CoderDojo-Odawara/DojoPaaS_Luanti_Server)

さくらのクラウド上で動くDojoPaaSを想定したものです。準備用の`doitatonce.sh`では2GBのスワップ領域を作り、Luantiで使うUDP 30000番ポートを開けます。`setup_luanti_server.sh`ではLuantiのビルドからゲーム、MOD、ワールドの準備まで進めます。サーバーの起動には`startluanti.sh`を使います。

ゲームにはMinecloniaを選びました。MODには、Luanti上でプログラミングを試せるLWScratchや、文字を表示するためのUnicode Signsなどを入れています。ワールドはクリエイティブモードで、ダメージや時間経過を気にせず遊べる設定にしました。

使い方はリポジトリの[README](https://github.com/CoderDojo-Odawara/DojoPaaS_Luanti_Server#readme)に載せています。

同じようにDojoPaaSでLuantiを動かしてみたい方の参考になればうれしいです。
