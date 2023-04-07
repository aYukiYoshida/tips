# TIPS

## Link to deployed page

<!-- markdownlint-disable MD033 -->
<kbd><a href="https://ayukiyoshida.github.io/tips/">Click to me !!</a></kbd>

## Requirements

- [Poetry](https://python-poetry.org)

## Environments

- Install python packages

  ```shell
  poetry install
  ```

- Install node packages

  ```shell
  npm install
  ```

- setup pre-commit

  ```shell
  poetry run pre-commit install
  ```

## Commands

### For mkdocs

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

### For zenn

- Create a new project

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

## Project layout

```text
mkdocs.yml    # The configuration file.
docs/         # Articles for MkDocs
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
articles      # Articles for Zenn
books         # Books for Zenn
```

## Reference

- [MkDocsによるドキュメント作成 - Qiita](https://qiita.com/mebiusbox2/items/a61d42878266af969e3c)
- [GitHubリポジトリでZennのコンテンツを管理する](https://zenn.dev/zenn/articles/connect-to-github)
