# aiwolf-nlp-agent
人狼知能コンテスト（自然言語部門） のサンプルエージェントです。

<!-- START doctoc -->
<!-- END doctoc -->

## 次回大会について
最新情報は[aiwolfdial.github.io](https://aiwolfdial.github.io/aiwolf-nlp/)をご確認ください。

また、2025年度人工知能学会全国大会に向けた大会では下記が予定されています。

> [!IMPORTANT]
> - トークリクエストならびに囁きリクエストにおける発言の文字数制限の追加
> - 13人ゲームの追加
> - カスタムプレイヤー名とカスタムプロフィールの追加

### 13人-人狼
13人人狼で現在想定している役職は下記の通りです。
| 役職 | 陣営 | 人数 | 特殊能力 |
| ---- | ---- | ---- | ---- |
| 村人 | 村人 | 6 | なし |
| 占い師 | 村人 | 1 | 夜のターンに1名選択し、そのプレイヤーの陣営を知ることができる |
| 霊媒師 | 村人 | 1 | 投票によって追放されたプレイヤーの陣営を知ることができる |
| 騎士 | 村人 | 1 | 夜のターンに1名選択し、そのプレイヤーを人狼の襲撃から守ることができる |
| 人狼 | 人狼 | 3 | 夜のターンに1名選択し、そのプレイヤーを襲撃することでゲームから除外することができる |
| 狂人 | 人狼 | 1 | 人狼陣営の勝利が自身の勝利になる |

### 5人-人狼
| 役職 | 陣営 | 人数 | 特殊能力 |
| ---- | ---- | ---- | ---- |
| 村人 | 村人 | 2 | なし |
| 占い師 | 村人 | 1 | 夜のターンに1名選択し、そのプレイヤーの陣営を知ることができる |
| 人狼 | 人狼 | 1 | 夜のターンに1名選択し、そのプレイヤーを襲撃することでゲームから除外することができる |
| 狂人 | 人狼 | 1 | 人狼陣営の勝利が自身の勝利になる |

### 大会の予選の実行方法
> [!IMPORTANT]
> 最新情報は[aiwolfdial.github.io](https://aiwolfdial.github.io/aiwolf-nlp/)をご確認ください。

大会参加者はエージェントを実装したうえで、ご自身の端末でエージェントを実行、大会運営が提供するゲームサーバに接続する必要があります。エージェントの実装については、実装言語を含め、制限はありません。  
自己対戦では、5体,13体のエージェントをご自身の端末で実行し、大会運営が提供する自己対戦用のゲームサーバに接続しすることで、エージェント同士の対戦を行うことができます。

ローカル内での動作確認ならびに自己対戦するためのゲームサーバについては、[aiwolfdial/aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server) を参考にしてください。

次回大会の詳細についてはしばらくお待ちください。

## 環境構築

> [!IMPORTANT]
> Python 3.11以上が必要です。

```bash
git clone https://github.com/aiwolfdial/aiwolf-nlp-agent.git
cd aiwolf-nlp-agent
python -m venv .venv
source .venv/bin/activate
pip install .
```

> [!NOTE]
> aiwolf-nlp-commonとは、役職や接続方式に関するプログラムが定義されているPythonパッケージです。  
> 詳細については、[aiwolfdial/aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common) をご覧ください。

## 実行方法

### 自己対戦

事前に、ローカル内にゲームサーバを立ち上げる必要があります。  
[aiwolfdial/aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server) を参考にしてください。

```bash
cp config/config.yml.example config/config.yml
python src/main.py
```

## 設定 (config.yml)

### web_socket

`url`: ゲームサーバのURLです。ローカル内のゲームサーバに接続する場合はデフォルト値で問題ありません。
`token`: ゲームサーバに接続するためのトークンです。大会運営から提供されるトークンを設定してください。
`auto_reconnect`: 対戦終了後に自動で再接続するかどうかの設定です。

### agent

`num`: 起動するエージェントの数です。自己対戦の場合はデフォルト値で問題ありません。  
`team`: エージェントのチーム名です。大会運営から提供されるチーム名を設定してください。

### log

`console_output`: コンソールにログを出力するかどうかの設定です。  
`file_output`: ファイルにログを出力するかどうかの設定です。  
`output_dir`: ログを保存するディレクトリのパスです。  
`level`: ログの出力レベルです。`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`のいずれかを設定してください。

#### log.requests

`name`, `initialize`, `daily_initialize`, `whisper`, `talk`, `daily_finish`, `divine`, `guard`, `vote`, `attack`, `finish`: 各リクエストのログを出力するかどうかの設定です。

## カスタマイズ方法

### 全役職共通
`src/agent/agent.py`: このファイルは全ての役職に共通する動作を記述するファイルです。

#### 要求される動作に関するメソッド
| メソッド名 | 変更推奨度 | 働き |
| ---- | ---- | ---- |
| `name` | 🔴 **非推奨** | `NAME`リクエスト時にチーム名を返却するメソッド |
| `initialize` | 🟡 **推奨度: 中** | `INITIALIZE`リクエスト時に送信されたゲームの設定を受け取る処理を行うメソッド |
| `daily_initialize` | 🟡 **推奨度: 中** | `DAILY_INITIALIZE`リクエスト時の処理を行うメソッド |
| `talk` | 🟢 **推奨度: 高** | `TALK`リクエスト時に他のプレイヤーと会話を行うための発言を生成するメソッド |
| `daily_finish` | 🟡 **推奨度: 中** | `DAILY_FINISH`リクエスト時の処理を行うメソッド |
| `vote` | 🟢 **推奨度: 高** | `VOTE`リクエスト時に投票先を決定するメソッド |
| `finish` | 🟡 **推奨度: 中** | `FINISH`リクエスト時の処理を行うメソッド|

### 村人
path: `src/agent/villager.py`

このファイルは村人専用の動作を記述するファイルです。\
`talk`や`vote`を変更することで村人専用の行動を設定することができます。

### 占い師
path: `src/agent/seer.py`

このファイルは占い師専用の動作を記述するファイルです。\
`talk`や`vote`,`divine`を変更することで占い師専用の行動を設定することができます。

#### 占いのメソッド
| メソッド名 | 変更推奨度 | 働き |
| ---- | ---- | ---- |
| `divine` | 🟢 **推奨度: 高** | `DIVINE`リクエスト時に占い先を決定するメソッド |


#### 占い結果の取得方法について
agentの`info.divine_result`から取得できます。\
詳細は[aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common/blob/main/src/aiwolf_nlp_common/packet/judge.py)をご確認ください。


### 霊媒師
path: `src/agent/medium.py`

このファイルは霊媒師専用の動作を記述するファイルです。\
`talk`や`vote`を変更することで霊媒師専用の行動を設定することができます。

#### 霊媒師の結果の取得方法について
agentの`info.medium_result`から取得できます。\
詳細は[aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common/blob/main/src/aiwolf_nlp_common/packet/judge.py)をご確認ください。

### 騎士
path: `src/agent/bodyguard.py`

このファイルは騎士専用の動作を記述するファイルです。\
`talk`や`vote`,`guard`を変更することで騎士専用の行動を設定することができます。

#### 護衛のメソッド
| メソッド名 | 変更推奨度 | 働き |
| ---- | ---- | ---- |
| `guard` | 🟢 **推奨度: 高** | `GUARD`リクエスト時に護衛先を決定するメソッド |

### 人狼
path: `src/agent/werewolf.py`

このファイルは人狼専用の動作を記述するファイルです。\
`talk`や`vote`,`attack`,`whisper`を変更することで人狼専用の行動を設定することができます。

#### 襲撃のメソッド
| メソッド名 | 変更推奨度 | 働き |
| ---- | ---- | ---- |
| `attack` | 🟢 **推奨度: 高** | `ATTACK`リクエスト時に護衛先を決定するメソッド |
| `whisper` | 🟢 **推奨度: 高** | 13人-人狼の`WHISPER`リクエスト時に人狼同士の囁きを行うメソッド |

### 狂人
path: `src/agent/possessed.py`

このファイルは狂人専用の動作を記述するファイルです。\
`talk`や`vote`を変更することで狂人専用の行動を設定することができます。