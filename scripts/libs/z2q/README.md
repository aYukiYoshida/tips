# Zenn to Qiita

## 変換内容

### Front Matter

```markdown
title: "" -> ダブルクォート削除
emoji: "😊" -> 削除
type: "tech" # tech: 技術記事 / idea: アイデア -> 削除
topics: [] -> tags: - で並べる
published: false -> private: false

title: 8537f5d29c2d36
tags:
  - ''
private: false
updated_at: ''
id: null
organization_url_name: null
slide: false
```

### 画像のパス

```markdown
![Alternative](/images/{article_id}/image.png =500x) -> <img width="500x" src="https://raw.githubusercontent.com/aYukiYoshida/tips/main/images/{article_id}/image.png" alt="Alternative">
```

### メッセージ

```markdown
:::message -> :::note info
:::message alert -> :::note alert
warn は Zenn が未対応
```
