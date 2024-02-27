# TIPS

## Link to deployed page

<!-- markdownlint-disable MD033 -->
<kbd><a href="https://ayukiyoshida.github.io/tips/">Click to me !!</a></kbd>

## Requirements

- [mise](https://mise.jdx.dev/)

## Setup

1. Derive source code

    ```shell
    git clone git@github.com:aYukiYoshida/tips.git
    ```

2. Install packages

    ```shell
    mise install
    ```

3. Install dependencies

    ```shell
    mise run setup
    ```

## Commands

### for mkdocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

- Create a new project

  ```shell
  poetry run mkdocs new [dir-name]
  ```

- Start the live-reloading docs server

  ```shell
  poetry run mkdocs serve
  ```

- Build the documentation site.

  ```shell
  poetry run mkdocs build
  ```

- Deploy the built documentation site on Github Pages.

  ```shell
  poetry run mkdocs gh-deploy
  ```

- Print help message and exit.

  ```shell
  poetry run mkdocs -h
  ```

### for Zenn

- Create a new project (only at first time; not required)

  ```shell
  npx zenn init
  ```

- Create a new article

  ```shell
  npx zenn new:article
  ```

- Start the live-reloading docs server

  ```shell
  npx zenn preview --port 3000
  ```

### for Qiita

The following commands for Qiita do not need to be executed manually because the articles of Qiita are managed by the GitHub Actions.
These are provided for reference only.

- Create a new project (only at first time; not required)

  ```shell
  npx qiita init
  ```

- Create a new article

  ```shell
  npx qiita new <BASE_NAME>
  ```

- Start the live-reloading docs server

  ```shell
  npx qiita preview
  ```

## Project Layout

```text
mkdocs.yml    # The configuration file.
docs/         # Articles for MkDocs
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
articles      # Articles for Zenn
books         # Books for Zenn
public        # Articles for Qiita
```

## Sync Articles between Zenn and Qiita

### Workflow

1. Zenn の記事を新規に作成する。もしくは、既存の記事を更新する。
2. Zenn の記事の新規作成もしくは、更新についてコミットする。
3. 前述のコミットを main ブランチに push する。
4. main ブランチでの変更が検知され Zennが提供する機能により自動でデプロイされる。
5. main ブランチでの変更が検知され GitHub Actions の [sync-articles-from-zenn-to-qiita](./.github/workflows/zenn_to_qiita.yml) のワークフローにより、Zenn の記事が Qiita に自動で変換される。
   1. 同期する Qiita の記事が存在しない場合は、新規に作成され、その id が Zenn の記事の末尾に追記される。この Zenn の記事の変更については、自動でコミットされる。
   2. 新規作成もしくは、更新によらず Qiita の記事の変更についてのプルリクエストが作成される。
6. Qiita の記事の変更について、プルリクエストをマージする。
7. main ブランチでの変更が検知され GitHub Actions の [publish-qiita-articles](./.github/workflows/publish_qiita_articles.yml) のワークフローにより、Qiita の記事が自動で公開される。
   1. このとき Qiita CLI により front matter が更新される。この Qiita の記事の変更については、自動でコミットされる。

### Convert Article Command

- Convert article of Zenn to that of Qiita

  ```shell
  npm run z2q <ARTICLE_ID>
  ```

## Reference

- [MkDocsによるドキュメント作成 - Qiita](https://qiita.com/mebiusbox2/items/a61d42878266af969e3c)
- [GitHubリポジトリでZennのコンテンツを管理する](https://zenn.dev/zenn/articles/connect-to-github)
- [Qiita CLI](https://github.com/increments/qiita-cli)
