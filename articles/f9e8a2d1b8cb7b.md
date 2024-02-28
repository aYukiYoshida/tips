---
title: "mise で Nodejs を管理する環境で Playwright Test for VSCode 使用時にハマったこと"
emoji: "🎭"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["mise", "playwright", "vscode"]
published: true
---

## はじめに

開発環境のパッケージ管理にいままで[pyenv](https://github.com/pyenv/pyenv)と[nodenv](https://github.com/nodenv/nodenv)と[asdf](https://asdf-vm.com/)と、と使用するパッケージに合わせて使い分けていたのですが、最近[mise](https://mise.jdx.dev/)で一元管理するように乗り換えました。

この記事では mise で Nodejs を管理する環境で VSCode の拡張である [Playwright Test for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) が node を呼び出せないとエラーを出した時の対処方法を記述します。

## エラー内容

mise で Nodejs を管理する環境下で Playwright Test for VSCode を使用していると、以下のようなエラーをこの拡張機能が出ました。

``` console
Unable to find 'node' executable. Make sure to have Node.js installed and available in your PATH. Current PATH: '...'.
```

確かに Current PATH には `/Users/username/.local/share/mise/installs/node/18.15.0/bin` のような Nodejs のパスが含まれていませんでした。

## 原因

筆者の環境ではログインシェルに `zsh` を使用していました。この環境下で `mise` をアクティベートするために `$HOME/.zshrc` に以下のように記述していました。

``` shell
if command -v mise 1>/dev/null 2>&1; then
  eval "$(mise activate zsh)"
fi
```

この記述により、対話モードのシェルでは mise 管理下の Nodejs へのパスが `PATH` の環境変数に追加されます。しかし VSCode では、 `$HOME/.zshrc` を読み込まないため、 `PATH` の環境変数にmise 管理下の Nodejs へのパスが追加されません。

## 解決方法

[mise のドキュメント](https://mise.jdx.dev/getting-started.html#_2b-alternative-add-mise-shims-to-path)にあるように `shims` へのパスを `PATH` の環境変数に追加することで解決できます。この処理は対話モードのシェルでは不要のため、`$HOME/.zprofile` に以下のように記述します。

``` shell
if command -v mise 1>/dev/null 2>&1; then
  eval "$(mise activate --shims)"
fi
```

## おわりに

VSCode と Playwright Test for VSCode と具体的な環境によるエラーについて記述しましたが、 mise で管理する環境下で他のパッケージを ほかの IDE で使用する場合にも同様のエラーが発生する可能性があると思います。mise のアクティベートと shims を PATH に追加する処理を profile ファイルと rc ファイルそれぞれに記述することでエラーを回避できるかもしれません。
