## 目次
- [自動テスト](#自動テスト) 2分
    - [単体テスト](#単体テスト)
    - [統合テスト](#統合テスト)
    - [E2Eテスト](#e2eテスト)
- [なぜテストコードを書くのか](#なぜテストコードを書くのか) 3分
- [効果的なテストコード](#効果的なテストコード) 2分
- [テスト戦略](#テスト戦略) 3分
- [テストファースト](#テストファースト) 5分
- [ハンズオン](#ハンズオン) 20分
    - [UTを書いてみる](#2-utを書いてみる)
    - [ITを書いてみる](#3-itを書いてみる)
    - [CIでテストが通ることを確認](#4-ciでテストが通ることを確認)
- 質疑応答 10分


## 自動テスト
一般的に自動テストは単体テスト（UT）、統合テスト（IT）、E2Eテスト（E2E）に分類されます。

それぞれの定義には解釈の余地があるので、プロジェクトやチームで各テスト工程の対象を決めておくと良いです。

今回の勉強会では以下のように定義します。

### 単体テスト
  - クラス、関数をテストする
  - DBやファイルシステム、Web APIなどのプロセス外のシステムに依存する処理は対象外
  - 例：サービスクラスやドメインオブジェクトのビジネスロジックをテスト対象とする。

### 統合テスト
  - 複数のコンポーネントや外部システムとの連携を含めてテストする
  - 本勉強会では、単体テストに該当しないテストは全てここに分類する
  - 例：コントローラやサービスクラスなどをテスト対象とし、テスト用のDBとしてDockerコンテナを用いる。

### E2Eテスト
  - デプロイされたアプリケーションでビジネスシナリオをテストする
  - 広義の統合テストの一部と見ることもできる
  - 例：フロントエンド・バックエンドをdev環境にデプロイし、playwrightなどでフロントエンドを操作し実際のシナリオを実行する。

## なぜテストコードを書くのか
- 退行を防ぐ
  - テストコードがない場合、コードの変更やバージョンアップのたびに手動でテストすることを強いられます。これはヒューマンエラーによる見落としや重大なバグを誘発します。チーム開発やコードベースが大きくなるほど顕著に現れます。
  - 上記の問題はテストコードで解決できます。テストコードをCIに組み込めば、コードが変更されるたびに自動でテストが実行されます。

- 仕様がコードベースで表現される
  - テストコードで仕様を検証していれば、「ドキュメントが古くて仕様が分からない」「実装した人しか仕様が分からない」という問題を防ぐことができます。

- 自分が書いたコードに自信を持てる
  - これらの利点は、開発者に自信を与えてくれます。コードを変更してもバグを起こしていないか不安になることがなくなります。仕様を正しく満たし、退行を引き起こさない実装をしたと言えるようになります。
  - 個人的に最も大きい恩恵だと感じています。

## 効果的なテストコード
テストコードでは「ふるまい」を検証することが重要です。

- ふるまいとは
  - テスト対象（クラスや関数）から得られる最終的な結果のこと
  - 関数の戻り値、DBの状態などが該当する
  - 「プライベート変数の状態」「プライベート関数が呼ばれたか」などはふるまいではなく実装の詳細であり、テスト対象にしない

- なぜふるまいを検証するのが良いか
  - テストの信頼性向上
    - 実装の詳細を検証していると、**リファクタリングしただけでテストが壊れる**（ふるまいは変わっていないのに失敗する）問題が起きます。逆に、実装の内部状態だけ見ていると**ふるまいのバグを見逃す**リスクもあります。どちらもテストの信頼性を下げ、テストが嘘をつくようになる状態です。
    - テスト対象のふるまいが変わったときだけ警告してくれることが、テストの信頼性を上げてくれます。
  - テストの可読性向上
    - 例えば、非エンジニアからすれば「プライベート変数の状態」「プライベート関数が呼ばれたか」といった実装の詳細は知らなくて良いことです。一方、ふるまいは仕様に関わるため、非エンジニアが見ても検証内容を把握することができます。
    - エンジニアであっても実装詳細のテストを読むことを強いられるのは認知負荷を不要に高めてしまいます。

## テスト戦略
テストピラミッドという考え方があります。単体テスト > 統合テスト > E2E の割合でテストコードを構成するのが一般的に良いとされています。

```
          /\
         /E2E\        ← 少ない
        /------\
       /   IT   \     ← 中程度
      /----------\
     /     UT     \   ← 多い
    /--------------\
```

ビジネスロジックが少ない単純なCRUDなどの場合は単体テストで検証することが少ないので、単体テスト <= 統合テスト となることもあります。

```
       /\
      /E2E\       ← 少ない
     /------\
    /   IT   \    ← 多い
    \--------/
     \  UT  /     ← 少ない
      \    /
       \/
```

このように、テストの割合はその機能のビジネスロジックの複雑さや重要度によって検討するのが良いと思います。

## テストファースト
実装よりも先にテストコードを書くことをテストファーストと言います。

経験上、実装した後にテストコードを書くと、「今の実装のままテストを通すこと」に集中してしまい、正しい振る舞いかどうかを考えなくなりがちです。テストファーストにすることで、まず仕様（正しい振る舞い）を定義してから実装に入れるようになります。また、自分がそのコードの最初の利用者になるため、使いやすいインターフェース設計が自然とできるようになります。

### テスト駆動開発（TDD）
Kent Beck さんが考案した、テストファーストを取り入れた開発手法です。

1. テストケースをTODOリストとして書き出す
2. その中から1つテストを書く → 失敗を確認する（**RED**）
3. テストが通る最小限の実装をする（**GREEN**）
4. 必要に応じてリファクタリングする（**REFACTOR**）
5. 2に戻る

## ハンズオン
TDDでREST APIを実装してみましょう。

### 仕様
見積もり作成API（`POST /quotes`）を1本実装します。

顧客がプランと契約月数を指定すると、割引を適用した見積もり金額を計算し、DBに保存した上で結果を返すAPIです。

**料金計算ルール:**
- 月額料金はプランによって異なる
  - basic: 980円
  - standard: 1,980円
  - premium: 4,980円
- 長期割引
  - 12ヶ月以上: 8%割引
  - 24ヶ月以上: 14%割引
- 端数は切り捨て

| 項目 | 内容 |
|------|------|
| メソッド | POST |
| パス | `/quotes` |
| リクエストボディ | `{"customer_name": "田中太郎", "plan": "standard", "months": 12}` |
| 正常レスポンス（201） | `{"id": 1, "customer_name": "田中太郎", "plan": "standard", "months": 12, "monthly_price": 1980, "discount_rate": 8, "total_price": 21859}` |
| 異常系（クライアントエラー） | 入力値が不正な場合は `422 Unprocessable Entity` を返す |
| 異常系（システムエラー） | サーバー内部でエラーが発生した場合は `500 Internal Server Error` を返す |

技術スタック: Python / FastAPI / pytest / MySQL

### 開発環境セットアップ
本リポジトリをcloneし、自分のブランチを作成してください。

```bash
git clone <リポジトリURL>
cd testing-workshop
git checkout -b work/<自分の名前>
```

以下のコマンドで開発環境を整えます。依存ライブラリ（pytest, fastapi, httpx）もインストールされます。

```bash
make setup
```

リポジトリには以下のファイルが事前に用意されています。今回のハンズオンではビジネスロジックとテストの実装に集中するため、インフラ周りは準備済みです。

| ファイル | 役割 |
|------|------|
| `docker-compose.yml` | テスト用MySQLコンテナの定義 |
| `sql/schema.sql` | quotesテーブルのDDL |
| `src/database.py` | DB接続の取得・解放（FastAPIの依存性注入用） |
| `src/main.py` | FastAPIアプリとエンドポイントの雛形（中身は未実装） |
| `tests/conftest.py` | IT用フィクスチャ（テーブル作成・クリーンアップ） |
| `.github/workflows/test.yml` | pushトリガーでpytestを自動実行するCI |

### 実装
TDDで見積もり作成APIを実装してみましょう。

#### 1. テストケースをTODOリストに書き出す
仕様から以下のふるまいが想定されるのでTODOリスト（todo.md）に書いておきましょう。

**料金:**
- [ ] プランに応じた月額料金が正しいこと（basic: 980円, standard: 1,980円, premium: 4,980円）

**割引:**
- [ ] 12ヶ月未満は割引なしであること
- [ ] 12ヶ月以上24ヶ月未満は8%割引されること
- [ ] 24ヶ月以上は14%割引されること
- [ ] 割引適用時の端数は切り捨てされること

**エラー:**
- [ ] 不正なプランの場合エラーになること

**API:**
- [ ] POST /quotes で見積もりが作成されDBに保存されること
- [ ] サーバー内部エラー時に500エラーが返ること
- [ ] 不正なリクエストで422エラーが返ること

#### 2. UTを書いてみる
`tests/test_quote.py` にテストコードを書いていきましょう。

TODOリストの「プランに応じた月額料金が正しいこと」から始めます。3プラン分書きましょう。

まずテスト関数と検証したいふるまいのアサーションを書きます。3パターンあるので `pytest.mark.parametrize` でまとめましょう。

```python
import pytest


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [("basic", 980), ("standard", 1980), ("premium", 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        assert quote.monthly_price == expected
```

見積もりを表す `Quote` が必要なので、プランを渡して生成します。この時点ではプランに応じた月額料金だけを検証するので、月数はまだ不要です。

```python
import pytest

from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [("basic", 980), ("standard", 1980), ("premium", 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan)
        assert quote.monthly_price == expected
```

##### RED

テストを実行して失敗することを確認します。まだ何も実装していないので `ModuleNotFoundError` が出るはずです。

```bash
uv run pytest tests/test_quote.py
```

##### GREEN

`src/quote.py` に `Quote` クラスを実装してテストが通るようにしましょう。
テストを通すために必要な最小限だけ実装します。

```python
class Quote:
    def __init__(self, plan: str):
        if plan == "basic":
            self._monthly_price = 980
        elif plan == "standard":
            self._monthly_price = 1980
        elif plan == "premium":
            self._monthly_price = 4980

    @property
    def monthly_price(self) -> int:
        return self._monthly_price
```

テストが通るか確認しましょう。

```bash
uv run pytest tests/test_quote.py
```

GREENになりました。次はTODOリストの「12ヶ月以上24ヶ月未満は8%割引されること」を検証します。standardプラン・20ヶ月のケースでテストを追加しましょう。割引には月数が必要なので、ここで初めて `months` を導入します。`Quote` が `months` を受け取るようになるため、月額料金のテストにも `months=1` を渡します。

```python
import pytest

from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [("basic", 980), ("standard", 1980), ("premium", 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan="standard", months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432
```

##### RED

```bash
uv run pytest tests/test_quote.py
```

REDになりました。`months` 引数も `discount_rate` も `total_price` もまだ実装されていないからです。

##### GREEN

割引の判定と合計金額の計算を `Quote` に追加しましょう。`months` を受け取るようにし、`plan`/`months` もプロパティとして公開します（後のAPI実装で使います）。このテストを通すために必要な最小限の割引ロジックだけ実装します。

```python
class Quote:
    def __init__(self, plan: str, months: int):
        if plan == "basic":
            self._monthly_price = 980
        elif plan == "standard":
            self._monthly_price = 1980
        elif plan == "premium":
            self._monthly_price = 4980

        self._plan = plan
        self._months = months

        if 12 <= months < 24:
            self._discount_rate = 8
        else:
            self._discount_rate = 0

        self._total_price = self._monthly_price * months * (100 - self._discount_rate) // 100

    @property
    def plan(self) -> str:
        return self._plan

    @property
    def months(self) -> int:
        return self._months

    @property
    def monthly_price(self) -> int:
        return self._monthly_price

    @property
    def discount_rate(self) -> int:
        return self._discount_rate

    @property
    def total_price(self) -> int:
        return self._total_price
```

```bash
uv run pytest tests/test_quote.py
```

GREENになりました。`total_price` は `/ 100` で `float` になりますが、このテストケース（1,980 × 20 × 92 / 100 = 36,432.0）では割り切れるため問題ありません。端数が出るケースは後のテストで対処します。

次はTODOリストの「12ヶ月未満は割引なしであること」を検証します。

```python
import pytest

from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [("basic", 980), ("standard", 1980), ("premium", 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan="standard", months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432

    def test_12ヶ月未満は割引なしであること(self):
        quote = Quote(plan="standard", months=1)
        assert quote.discount_rate == 0
        assert quote.total_price == 1980
```

##### GREEN

```bash
uv run pytest tests/test_quote.py
```

現在の実装で12ヶ月未満は `else` 節で割引率0%になるため、追加の実装なしでGREENになります。

次はTODOリストの「24ヶ月以上は14%割引されること」を検証します。

```python
import pytest

from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [("basic", 980), ("standard", 1980), ("premium", 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan="standard", months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432

    def test_12ヶ月未満は割引なしであること(self):
        quote = Quote(plan="standard", months=1)
        assert quote.discount_rate == 0
        assert quote.total_price == 1980

    def test_24ヶ月以上は14パーセント割引されること(self):
        quote = Quote(plan="standard", months=24)
        assert quote.discount_rate == 14
        assert quote.total_price == 40867
```

##### RED

```bash
uv run pytest tests/test_quote.py
```

24ヶ月以上の14%割引がまだ実装されていません。また、`total_price` の計算で `/ 100` が小数を返すため（1,980 × 24 × 86 ÷ 100 = 40,867.2）、整数の期待値と一致しません。

##### GREEN

`src/quote.py` を以下のように書き換えて、24ヶ月以上の割引ロジックを追加しましょう。

```python
class Quote:
    def __init__(self, plan: str, months: int):
        if plan == "basic":
            self._monthly_price = 980
        elif plan == "standard":
            self._monthly_price = 1980
        elif plan == "premium":
            self._monthly_price = 4980

        self._plan = plan
        self._months = months

        if months >= 24:
            self._discount_rate = 14
        elif months >= 12:
            self._discount_rate = 8
        else:
            self._discount_rate = 0

        self._total_price = self._monthly_price * months * (100 - self._discount_rate) // 100

    @property
    def plan(self) -> str:
        return self._plan

    @property
    def months(self) -> int:
        return self._months

    @property
    def monthly_price(self) -> int:
        return self._monthly_price

    @property
    def discount_rate(self) -> int:
        return self._discount_rate

    @property
    def total_price(self) -> int:
        return self._total_price
```

```bash
uv run pytest tests/test_quote.py
```

GREENになりました。

次はTODOリストの「割引適用時の端数は切り捨てされること」を検証します。前のステップで `//` に変更済みですが、端数が発生するケースを明示的にテストしておきましょう。

```python
import pytest

from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [("basic", 980), ("standard", 1980), ("premium", 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan="standard", months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432

    def test_12ヶ月未満は割引なしであること(self):
        quote = Quote(plan="standard", months=1)
        assert quote.discount_rate == 0
        assert quote.total_price == 1980

    def test_24ヶ月以上は14パーセント割引されること(self):
        quote = Quote(plan="standard", months=24)
        assert quote.discount_rate == 14
        assert quote.total_price == 40867

    def test_割引適用時の端数は切り捨てされること(self):
        # 1,980 × 12 × 92 ÷ 100 = 21,859.2 → 切り捨てで 21,859
        quote = Quote(plan="standard", months=12)
        assert quote.discount_rate == 8
        assert quote.total_price == 21859
```

##### GREEN

```bash
uv run pytest tests/test_quote.py
```

前のステップで `//`（切り捨て除算）に変更済みのため、追加の実装なしでGREENになります。

##### REFACTOR

ここで `__init__` を見てみましょう。料金の取得・割引率の判定・合計の計算と、1つのメソッドに3つの責務が混在しています。テストがGREENのうちにリファクタリングしましょう。

**リファクタリング**: 各責務を凝集度の高いクラス・関数に分離します。

- プラン料金 → `Plan` 列挙型（`src/plan.py`）
- 割引率の判定 → `DiscountRate` 値オブジェクト（`src/discount.py`）
- 合計計算 → `Quote._calc_total` メソッド

`src/plan.py`:

```python
from enum import Enum


class Plan(Enum):
    """契約プランを表す列挙型。"""

    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"

    @property
    def monthly_price(self) -> int:
        """プランに対応する月額料金(円)を返す。"""
        prices = {
            "basic": 980,
            "standard": 1980,
            "premium": 4980,
        }
        return prices[self.value]
```

`src/discount.py`:

```python
class DiscountRate:
    """契約月数に応じた割引率(%)を表す値オブジェクト。"""

    _LONG_TERM_MONTHS = 24
    _LONG_TERM_RATE = 14
    _MID_TERM_MONTHS = 12
    _MID_TERM_RATE = 8

    def __init__(self, months: int):
        if months >= self._LONG_TERM_MONTHS:
            self._value = self._LONG_TERM_RATE
        elif months >= self._MID_TERM_MONTHS:
            self._value = self._MID_TERM_RATE
        else:
            self._value = 0

    @property
    def value(self) -> int:
        """割引率(%)を返す。"""
        return self._value
```

`src/quote.py`:

```python
from src.discount import DiscountRate
from src.plan import Plan


class Quote:
    """プランと契約月数から見積もりを算出する値オブジェクト。"""

    def __init__(self, plan: Plan, months: int):
        self._plan = plan
        self._months = months
        self._monthly_price = plan.monthly_price
        self._discount_rate = DiscountRate(months)
        self._total_price = self._calc_total()

    def _calc_total(self) -> int:
        """月額 × 月数 に割引率を適用した合計金額を整数で返す。"""
        return self._monthly_price * self._months * (100 - self._discount_rate.value) // 100

    @property
    def plan(self) -> str:
        return self._plan.value

    @property
    def months(self) -> int:
        return self._months

    @property
    def monthly_price(self) -> int:
        return self._monthly_price

    @property
    def discount_rate(self) -> int:
        return self._discount_rate.value

    @property
    def total_price(self) -> int:
        return self._total_price
```

`Quote` が `Plan` 列挙型を受け取るようになったので、テストコードも更新します。

```python
import pytest

from src.plan import Plan
from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [(Plan.BASIC, 980), (Plan.STANDARD, 1980), (Plan.PREMIUM, 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan=Plan.STANDARD, months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432

    def test_12ヶ月未満は割引なしであること(self):
        quote = Quote(plan=Plan.STANDARD, months=1)
        assert quote.discount_rate == 0
        assert quote.total_price == 1980

    def test_24ヶ月以上は14パーセント割引されること(self):
        quote = Quote(plan=Plan.STANDARD, months=24)
        assert quote.discount_rate == 14
        assert quote.total_price == 40867

    def test_割引適用時の端数は切り捨てされること(self):
        # 1,980 × 12 × 92 ÷ 100 = 21,859.2 → 切り捨てで 21,859
        quote = Quote(plan=Plan.STANDARD, months=12)
        assert quote.discount_rate == 8
        assert quote.total_price == 21859
```

```bash
uv run pytest tests/test_quote.py
```

GREENのままです。リファクタリング成功です。`Quote` は `Plan` と `DiscountRate` に責務を委譲するシンプルな値オブジェクトになりました。各クラスが単一の責務を持ち、凝集度が高まっています。

次はTODOリストの「不正なプランの場合エラーになること」を検証します。`Plan` 列挙型が不正な値を拒否することを確認しましょう。

```python
import pytest

from src.plan import Plan
from src.quote import Quote


class TestQuote:
    @pytest.mark.parametrize("plan, expected", [(Plan.BASIC, 980), (Plan.STANDARD, 1980), (Plan.PREMIUM, 4980)])
    def test_プランに応じた月額料金が正しいこと(self, plan, expected):
        quote = Quote(plan=plan, months=1)
        assert quote.monthly_price == expected

    def test_12ヶ月以上24ヶ月未満は8パーセント割引されること(self):
        quote = Quote(plan=Plan.STANDARD, months=20)
        assert quote.discount_rate == 8
        assert quote.total_price == 36432

    def test_12ヶ月未満は割引なしであること(self):
        quote = Quote(plan=Plan.STANDARD, months=1)
        assert quote.discount_rate == 0
        assert quote.total_price == 1980

    def test_24ヶ月以上は14パーセント割引されること(self):
        quote = Quote(plan=Plan.STANDARD, months=24)
        assert quote.discount_rate == 14
        assert quote.total_price == 40867

    def test_割引適用時の端数は切り捨てされること(self):
        # 1,980 × 12 × 92 ÷ 100 = 21,859.2 → 切り捨てで 21,859
        quote = Quote(plan=Plan.STANDARD, months=12)
        assert quote.discount_rate == 8
        assert quote.total_price == 21859

    @pytest.mark.parametrize("invalid_plan", ["free", "enterprise"])
    def test_不正なプランの場合ValueErrorが発生すること(self, invalid_plan):
        with pytest.raises(ValueError):
            Plan(invalid_plan)
```

##### GREEN

```bash
uv run pytest tests/test_quote.py
```

`Plan` は `Enum` を継承しているため、不正な値が渡されると自動的に `ValueError` を送出します。追加の実装なしでGREENになります。

すべてGREENになればUTは完了です。todo.mdのチェックを更新しておきましょう。

**料金:**
- [x] プランに応じた月額料金が正しいこと（basic: 980円, standard: 1,980円, premium: 4,980円）

**割引:**
- [x] 12ヶ月未満は割引なしであること
- [x] 12ヶ月以上24ヶ月未満は8%割引されること
- [x] 24ヶ月以上は14%割引されること
- [x] 割引適用時の端数は切り捨てされること

**エラー:**
- [x] 不正なプランの場合エラーになること

**API:**
- [ ] POST /quotes で見積もりが作成されDBに保存されること
- [ ] サーバー内部エラー時に500エラーが返ること
- [ ] 不正なリクエストで422エラーが返ること

#### 3. ITを書いてみる
続いて統合テストを書きます。このAPIはDBへの書き込みを伴うため、統合テストではHTTPリクエストのレスポンスだけでなく、DBに正しく保存されているかも検証します。

統合テストでは本番と同じDBエンジン（MySQL）をDockerで用意し、実際のSQL実行や制約を検証します。テスト用のMySQL（`docker-compose.yml`）、テーブル定義（`sql/schema.sql`）、DB接続（`src/database.py`）は事前に用意されています。

MySQLコンテナを起動しておきましょう。

```bash
docker compose up -d --wait
```

TODOリストの「POST /quotes で見積もりが作成されDBに保存されること」から始めます。`tests/test_api.py` にテストコードを書きましょう。

`tests/conftest.py` にはテストごとにテーブルを作成・クリーンアップするフィクスチャが用意されているので、テストコードの実装に集中できます。

```python
from fastapi.testclient import TestClient

from src.database import get_connection
from src.main import app


class TestCreateQuote:
    def test_POST_quotesで見積もりが作成されDBに保存されること(self):
        # Arrange
        client = TestClient(app)

        # Act
        response = client.post(
            "/quotes", json={"customer_name": "田中太郎", "plan": "standard", "months": 12}
        )

        # Assert
        data = response.json()
        assert response.status_code == 201
        assert "id" in data
        assert data["monthly_price"] == 1980
        assert data["discount_rate"] == 8
        assert data["total_price"] == 21859

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM quotes WHERE id = %s", (data["id"],))
                row = cursor.fetchone()
        finally:
            conn.close()
        assert row is not None
        assert row["total_price"] == 21859
```

ポイント:
- Docker上の本物のMySQLに対してテストするため、SQL方言や制約の差異に悩まされない
- フィクスチャの `yield` 前後でテーブルの作成・削除を行い、テスト間でデータが干渉しない
- レスポンスの検証だけでなく、DBの状態（ふるまい）も検証している
- `try/finally` でコネクションを確実にcloseし、例外発生時のリソースリークを防止

##### RED

```bash
uv run pytest tests/test_api.py
```

REDになります。`src/main.py` のエンドポイントがまだ未実装（`pass`）だからです。

##### GREEN

雛形（リクエスト/レスポンスモデル、エンドポイントの定義）は事前に用意されているので、`create_quote` 関数の中身を実装しましょう。まずはDB保存処理も含めてベタ書きで実装します。

`src/main.py` を以下のように書き換えます。

```python
from typing import Literal

import pymysql
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from src.database import get_db
from src.plan import Plan
from src.quote import Quote

app = FastAPI()


class QuoteRequest(BaseModel):
    """見積もり作成リクエストのスキーマ。"""

    customer_name: str
    plan: Literal["basic", "standard", "premium"]
    months: int = Field(gt=0)


class QuoteResponse(BaseModel):
    """見積もり作成レスポンスのスキーマ。"""

    id: int
    customer_name: str
    plan: str
    months: int
    monthly_price: int
    discount_rate: int
    total_price: int


@app.post("/quotes", status_code=201, response_model=QuoteResponse)
def create_quote(
    req: QuoteRequest, conn: pymysql.Connection = Depends(get_db)
) -> QuoteResponse:
    """見積もりを作成してDBに保存し、結果を返す。"""
    quote = Quote(plan=Plan(req.plan), months=req.months)

    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO quotes (customer_name, plan, months, monthly_price, discount_rate, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                req.customer_name,
                quote.plan,
                quote.months,
                quote.monthly_price,
                quote.discount_rate,
                quote.total_price,
            ),
        )
        conn.commit()
        quote_id = cursor.lastrowid

    return QuoteResponse(
        id=quote_id,
        customer_name=req.customer_name,
        plan=quote.plan,
        months=quote.months,
        monthly_price=quote.monthly_price,
        discount_rate=quote.discount_rate,
        total_price=quote.total_price,
    )
```

ポイント:
- 雛形では `QuoteRequest` で `plan` を `Literal` で制限し、`months` を `Field(gt=0)` で正の整数のみに制限している。不正な入力はFastAPIが自動で422エラーを返す
- `QuoteResponse` でレスポンスの型を明示。OpenAPIドキュメントにも反映される
- `Depends(get_db)` でコネクションの取得・解放をFastAPIに任せ、リソースリークを防止

```bash
uv run pytest tests/test_api.py
```

GREENになりました。テストが通る状態を維持したまま、リファクタリングに進みます。

##### REFACTOR

SQLの実行をハンドラから分離し、関心の分離を実現します。DBアクセスを担当する `src/repository.py` を作成しましょう。

```python
import pymysql

from src.quote import Quote


def save_quote(conn: pymysql.Connection, customer_name: str, quote: Quote) -> int:
    """見積もりをDBに保存し、採番されたIDを返す。"""
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO quotes (customer_name, plan, months, monthly_price, discount_rate, total_price) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                customer_name,
                quote.plan,
                quote.months,
                quote.monthly_price,
                quote.discount_rate,
                quote.total_price,
            ),
        )
        conn.commit()
        return cursor.lastrowid
```

`src/main.py` の `create_quote` を `save_quote` を使うように変更します。

`src/main.py` を以下のように書き換えます。

```python
from typing import Literal

import pymysql
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from src.database import get_db
from src.plan import Plan
from src.quote import Quote
from src.repository import save_quote

app = FastAPI()


class QuoteRequest(BaseModel):
    """見積もり作成リクエストのスキーマ。"""

    customer_name: str
    plan: Literal["basic", "standard", "premium"]
    months: int = Field(gt=0)


class QuoteResponse(BaseModel):
    """見積もり作成レスポンスのスキーマ。"""

    id: int
    customer_name: str
    plan: str
    months: int
    monthly_price: int
    discount_rate: int
    total_price: int


@app.post("/quotes", status_code=201, response_model=QuoteResponse)
def create_quote(
    req: QuoteRequest, conn: pymysql.Connection = Depends(get_db)
) -> QuoteResponse:
    """見積もりを作成してDBに保存し、結果を返す。"""
    quote = Quote(plan=Plan(req.plan), months=req.months)
    quote_id = save_quote(conn, req.customer_name, quote)

    return QuoteResponse(
        id=quote_id,
        customer_name=req.customer_name,
        plan=quote.plan,
        months=quote.months,
        monthly_price=quote.monthly_price,
        discount_rate=quote.discount_rate,
        total_price=quote.total_price,
    )
```

```bash
uv run pytest tests/test_api.py
```

リファクタリング後もGREENのままです。ハンドラはビジネスロジックの組み立てに専念し、SQL実行は `repository.save_quote` に委譲する構造になりました。

##### RED

次はTODOリストの「サーバー内部エラー時に500エラーが返ること」を検証します。`tests/test_api.py` を以下のように書き換えましょう。

```python
from fastapi.testclient import TestClient

from src.database import get_connection
from src.main import app


class TestCreateQuote:
    def test_POST_quotesで見積もりが作成されDBに保存されること(self):
        # Arrange
        client = TestClient(app)

        # Act
        response = client.post(
            "/quotes", json={"customer_name": "田中太郎", "plan": "standard", "months": 12}
        )

        # Assert
        data = response.json()
        assert response.status_code == 201
        assert "id" in data
        assert data["monthly_price"] == 1980
        assert data["discount_rate"] == 8
        assert data["total_price"] == 21859

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM quotes WHERE id = %s", (data["id"],))
                row = cursor.fetchone()
        finally:
            conn.close()
        assert row is not None
        assert row["total_price"] == 21859

    def test_サーバー内部エラー時に500エラーが返ること(self):
        # Arrange: テーブルを削除してDBエラーを発生させる
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE quotes")
            conn.commit()
        finally:
            conn.close()

        # Act
        client = TestClient(app)
        response = client.post(
            "/quotes", json={"customer_name": "田中太郎", "plan": "standard", "months": 12}
        )

        # Assert
        assert response.status_code == 500
```

```bash
uv run pytest
```

REDになります。DBエラー（`pymysql.Error`）が未処理のまま送出されるためです。

##### GREEN

`src/main.py` を以下のように書き換えて、DBエラーを500レスポンスに変換するカスタム例外ハンドラを追加しましょう。

```python
from typing import Literal

import pymysql
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.database import get_db
from src.plan import Plan
from src.quote import Quote
from src.repository import save_quote

app = FastAPI()


class QuoteRequest(BaseModel):
    """見積もり作成リクエストのスキーマ。"""

    customer_name: str
    plan: Literal["basic", "standard", "premium"]
    months: int = Field(gt=0)


class QuoteResponse(BaseModel):
    """見積もり作成レスポンスのスキーマ。"""

    id: int
    customer_name: str
    plan: str
    months: int
    monthly_price: int
    discount_rate: int
    total_price: int


@app.exception_handler(pymysql.Error)
async def db_exception_handler(request: Request, exc: pymysql.Error) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.post("/quotes", status_code=201, response_model=QuoteResponse)
def create_quote(
    req: QuoteRequest, conn: pymysql.Connection = Depends(get_db)
) -> QuoteResponse:
    """見積もりを作成してDBに保存し、結果を返す。"""
    quote = Quote(plan=Plan(req.plan), months=req.months)
    quote_id = save_quote(conn, req.customer_name, quote)

    return QuoteResponse(
        id=quote_id,
        customer_name=req.customer_name,
        plan=quote.plan,
        months=quote.months,
        monthly_price=quote.monthly_price,
        discount_rate=quote.discount_rate,
        total_price=quote.total_price,
    )
```

```bash
uv run pytest
```

GREENになりました。500エラーのテストではモックを使わず、テーブルを削除して実際のDBエラーを再現しています。

##### GREEN

次はTODOリストの「不正なリクエストで422エラーが返ること」を検証します。不正なプラン・不正な月数・フィールド欠落の3パターンをテストしましょう。`tests/test_api.py` を以下のように書き換えます。

```python
import pytest
from fastapi.testclient import TestClient

from src.database import get_connection
from src.main import app


class TestCreateQuote:
    def test_POST_quotesで見積もりが作成されDBに保存されること(self):
        # Arrange
        client = TestClient(app)

        # Act
        response = client.post(
            "/quotes", json={"customer_name": "田中太郎", "plan": "standard", "months": 12}
        )

        # Assert
        data = response.json()
        assert response.status_code == 201
        assert "id" in data
        assert data["monthly_price"] == 1980
        assert data["discount_rate"] == 8
        assert data["total_price"] == 21859

        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM quotes WHERE id = %s", (data["id"],))
                row = cursor.fetchone()
        finally:
            conn.close()
        assert row is not None
        assert row["total_price"] == 21859

    def test_サーバー内部エラー時に500エラーが返ること(self):
        # Arrange: テーブルを削除してDBエラーを発生させる
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE quotes")
            conn.commit()
        finally:
            conn.close()

        # Act
        client = TestClient(app)
        response = client.post(
            "/quotes", json={"customer_name": "田中太郎", "plan": "standard", "months": 12}
        )

        # Assert
        assert response.status_code == 500

    @pytest.mark.parametrize(
        "body",
        [
            {"customer_name": "田中太郎", "plan": "free", "months": 12},
            {"customer_name": "田中太郎", "plan": "standard", "months": 0},
            {"customer_name": "田中太郎"},
        ],
    )
    def test_不正なリクエストで422エラーが返ること(self, body):
        client = TestClient(app)
        response = client.post("/quotes", json=body)
        assert response.status_code == 422
```

```bash
uv run pytest
```

雛形の `QuoteRequest` で `plan` を `Literal` で制限し、`months` を `Field(gt=0)` で正の整数のみに制限しているため、追加の実装なしでGREENになります。

すべてGREENになればITも完了です。todo.mdを更新しましょう。

**料金:**
- [x] プランに応じた月額料金が正しいこと（basic: 980円, standard: 1,980円, premium: 4,980円）

**割引:**
- [x] 12ヶ月未満は割引なしであること
- [x] 12ヶ月以上24ヶ月未満は8%割引されること
- [x] 24ヶ月以上は14%割引されること
- [x] 割引適用時の端数は切り捨てされること

**エラー:**
- [x] 不正なプランの場合エラーになること

**API:**
- [x] POST /quotes で見積もりが作成されDBに保存されること
- [x] サーバー内部エラー時に500エラーが返ること
- [x] 不正なリクエストで422エラーが返ること

#### 4. CIでテストが通ることを確認
変更をpushしてGitHub ActionsでCIが通ることを確認しましょう。

```bash
git add .
git commit -m "feat: 見積もり作成API(POST)の実装とテスト"
git push
```

GitHubのActionsタブでテストがGREENになっていることを確認してください。

開発終了です。PRを作成してレビューを待ちましょう。

### まとめ
Claude Codeなどのコーディングエージェントの登場で、自動テストの重要性がさらに増しています。テストコードは、エージェントに仕様を誤解させずに正しく実装させるためのガードレールとしても機能します。

自動テストの文化をチームに根付かせていきましょう。

### 参考文献
- [単体テストの考え方/使い方](https://www.amazon.co.jp/%E5%8D%98%E4%BD%93%E3%83%86%E3%82%B9%E3%83%88%E3%81%AE%E8%80%83%E3%81%88%E6%96%B9-%E4%BD%BF%E3%81%84%E6%96%B9-Vladimir-Khorikov/dp/4839981728)
- [テスト駆動開発](https://www.amazon.co.jp/%E3%83%86%E3%82%B9%E3%83%88%E9%A7%86%E5%8B%95%E9%96%8B%E7%99%BA-Kent-Beck/dp/4274217884/ref=pd_sbs_d_sccl_1_1/356-7703089-6525043?pd_rd_w=NOpq7&content-id=amzn1.sym.d9975236-2c6f-40f8-8a79-8a86a96a4ad2&pf_rd_p=d9975236-2c6f-40f8-8a79-8a86a96a4ad2&pf_rd_r=15J2YJ1C4ZKKCKXRTWYW&pd_rd_wg=4dFJk&pd_rd_r=ef551665-559e-4a9d-a162-320dff6ecad4&pd_rd_i=4274217884&psc=1)
- [【翻訳】テスト駆動開発の定義](https://t-wada.hatenablog.jp/entry/canon-tdd-by-kent-beck)
- [ドメイン駆動設計をはじめよう](https://www.amazon.co.jp/%E3%83%89%E3%83%A1%E3%82%A4%E3%83%B3%E9%A7%86%E5%8B%95%E8%A8%AD%E8%A8%88%E3%82%92%E3%81%AF%E3%81%98%E3%82%81%E3%82%88%E3%81%86-%E2%80%95%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2%E3%81%AE%E5%AE%9F%E8%A3%85%E3%81%A8%E4%BA%8B%E6%A5%AD%E6%88%A6%E7%95%A5%E3%82%92%E7%B5%90%E3%81%B3%E3%81%A4%E3%81%91%E3%82%8B%E5%AE%9F%E8%B7%B5%E6%8A%80%E6%B3%95-Vlad-Khononov/dp/481440073X?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&ref_=fplfs&psc=1&smid=AN1VRQENFRJN5)
