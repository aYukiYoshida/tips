---
title: AppiumでAndroidのToastを無理やり取得する
tags:
  - Android
  - テスト
  - appium
private: false
updated_at: '2025-08-20T16:29:27+09:00'
id: 94d0ae023eb8d0ec5ced
organization_url_name: null
slide: false
ignorePublish: false
---
## はじめに

Appiumを使用してAndroidアプリのテストを行う際、Toastの要素が表示されているかを確認できないという問題がありました。Appiumのバージョンがv1系ですが、同じ内容の[issue](https://github.com/appium/appium/issues/13119)があります。
例えば、以下のようにToastの要素の表示を確認しようとしても`selenium.common.exceptions.StaleElementReferenceException`が発生します。

```python
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((AppiumBy.XPATH, './/android.widget.Toast[@text="message")))
assert element.get_attribute("displayed") == "true"
```

このとき、Toastの要素は`driver.page_source`には、含まれていることが確認できています。

以下は、[Appiumが提供するデモアプリ](https://github.com/appium/android-apidemos)でToastを表示させたときのスクリーンショットです。

<img src="https://raw.githubusercontent.com/aYukiYoshida/tips/main/images/f761020e739678/toast.png" alt="Toastの要素が表示されていない" width="500">

## Toastの要素の取得方法の提案

`driver.page_source`のxmlを直接解析することで、Toastの要素を取得する方法を提案します。
まず、`WebDriverWait`を使用して、Toastの要素が`page_source`内に出現まで待機し、Toastの要素を`driver.page_source`から抽出します。xmlの解析には[`xml.etree.ElementTree`](https://docs.python.org/ja/3/library/xml.etree.elementtree.html)モジュールを使用します。

```python
from xml.etree import ElementTree as ET

def presence_of_element_in_source(locator: Locator) -> Callable[[WebDriver], ET.Element]:
    def predicate(driver: WebDriver) -> ET.Element:
        element = ET.fromstring(driver.page_source).find(locator.value)
        if element is None:
            raise NoSuchElementException(f"Element with {locator} is not found in the page source.")
        return element

    return predicate

def find_element_from_source(locator: Locator, timeout: float) -> ET.Element:
    """Find an element in the page source."""
    if locator.strategy != AppiumBy.XPATH:
        raise ValueError(f"Locator strategy must be {AppiumBy.XPATH}, but got {locator.strategy}")
    try:
        return WebDriverWait(driver, timeout).until(presence_of_element_in_source(locator), timeout=timeout)
    except TimeoutException:
        raise NoSuchElementException(f"Element with {locator} is not found in the page source.")
```

取得したToast要素は[`ET.Element`](https://docs.python.org/ja/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element)オブジェクトであり、`get()`メソッドを使用して属性を取得できます。

```python
>>> print(element.attrib)
{'index': '1', 'package': 'com.android.settings', 'class': 'android.widget.Toast', 'text': 'message', 'displayed': 'true'}
>>> element.get("displayed")
'true'
```

`displayed`属性を確認することで、Toastの要素が表示されているかどうかを確認できます。ただし、実際に画面に表示されていることを保証するものではありません。

```python
toast: ET.Element = find_element_from_source((AppiumBy.XPATH, './/android.widget.Toast[@text="This is a long notification. See, you might need a second more to read it."]'), timeout=10)
assert element.get("displayed") == "true"
```

## まとめ

この方法により、Appiumを使用してAndroidアプリのToast要素を無理やり取得し、表示されているかどうかを確認することが可能になります。

<!-- zenn article id: f761020e739678 -->
