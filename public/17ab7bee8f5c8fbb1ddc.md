---
title: Playwright で Page Object Model を使用するときのちょっとした工夫
tags:
  - テスト
  - Web
  - TypeScript
  - testing
  - Playwright
private: true
updated_at: '2023-12-16T23:30:38+09:00'
id: 17ab7bee8f5c8fbb1ddc
organization_url_name: null
slide: false
ignorePublish: false
---
## はじめに

本記事は、[株式会社ACCESS Advent Calendar 2023](https://qiita.com/advent-calendar/2023/access) の22日目の記事です。
Playwright における Page Object Model を使用方法が公式ドキュメントに[ガイド](https://playwright.dev/docs/pom)として、紹介されている。
本記事ではさらに Playwright で Page Object Model を使用するときのちょっとした工夫について紹介する。

## コード

### 対象の HTML

対象の HTML は以下のものとする。一般的なログインフォームを想定している。

```HTML
<form action="/login" method="POST" enctype="application/json">
  <div>
    <label for="username-field">username</label>
    <input type="text" id="username-field" required/>
  </div>
  <div>
    <label for="password-field">password</label>
    <input type="password" id="password-field" required/>
  </div>
  <button id="login">Login</button>
</form>
```

### Page Object Model

上記の対象の HTML に対して、以下のような Page Object Model を作成する。

```typescript
import { expect, type Locator, type Page } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly usernameTextBox: Locator;
  readonly passwordTextBox: Locator;
  readonly loginButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameTextBox = page.getByRole(
      "textarea",
      {
        name: "username"
      }
    );
    this.passwordTextBox = page.getByRole(
      "textarea",
      {
        name: "password"
      }
    );
    this.loginButton = page.getByRole(
      "button",
      {
        name: "Login"
      }
    );
  }

  async login(username: string, password: string) {
    await this.usernameTextBox.fill(username);
    await this.passwordTextBox.fill(password);
    await this.loginButton.click();
  }
}
```

## ちょっとした工夫

冒頭でも参照した[ガイド](https://playwright.dev/docs/pom)では Page Object を定義したクラスのインスタンスを [`test`](https://playwright.dev/docs/api/class-test#test-call) のコールバック関数内で生成している。

```typescript
test('should be able to login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user', 'pass');
});
```

しかし、この方法では、テストケースを定義するたびに、インスタンスを生成するコードを各必要がある。たった一行だけれど、毎回記述するのは個人的には鬱陶しい。そこで、ちょっとした工夫として紹介するのが [Fixture](https://playwright.dev/docs/test-fixtures) のなかでインスタンスを生成するものである。

```typescript
import { test as base, Page } from "@playwright/test";

type TestFixtures = {
  loginPage: LoginPage;
};

const test = base.extend<TestFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage: = new LoginPage(page);
    await use(loginPage);
  },
});

test('should be able to login', async ({ loginPage }) => {
  await loginPage.login('user', 'pass');
});
```

Fixture を使用することで Fixture を呼び出すたびに Page Object のクラスのインスタンスの生成が実行される。

## さいごに

Playwright で Page Object Model を使用する際のちょっとした工夫について紹介した。結局のところ、この記事の味噌は Fixture の使用方法についての紹介となったが、テストケースの前後の処理などにも使用できるため、ぜひ活用してみてほしい。
明日は @Momijinn さんの記事です。お楽しみに！

<!-- zenn article id: 70698527ec7bf0 -->
