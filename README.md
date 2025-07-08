# aiwolf-nlp-agent

人狼知能コンテスト（自然言語部門） のサンプルエージェントです。

> [!IMPORTANT]
> 最新情報は[aiwolfdial.github.io](https://aiwolfdial.github.io/aiwolf-nlp/)を参照してください。

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## 目次

- [aiwolf-nlp-agent](#aiwolf-nlp-agent)
  - [目次](#目次)
  - [環境構築](#環境構築)
  - [実行方法](#実行方法)
    - [エージェントの実行](#エージェントの実行)
      - [設定ファイルを指定して起動する方法](#設定ファイルを指定して起動する方法)
    - [ローカル環境での実行](#ローカル環境での実行)
    - [予選の対戦方法](#予選の対戦方法)
    - [本戦の対戦方法](#本戦の対戦方法)
  - [設定 (config/config.yml)](#設定-configconfigyml)
    - [web\_socket](#web_socket)
    - [agent](#agent)
    - [log](#log)
      - [log.requests](#logrequests)
  - [エージェントのカスタマイズ方法](#エージェントのカスタマイズ方法)
    - [全役職共通 (src/agent/agent.py)](#全役職共通-srcagentagentpy)
      - [リクエストに対応するメソッド](#リクエストに対応するメソッド)
    - [人狼 (src/agent/werewolf.py)](#人狼-srcagentwerewolfpy)
    - [狂人 (src/agent/possessed.py)](#狂人-srcagentpossessedpy)
    - [占い師 (src/agent/seer.py)](#占い師-srcagentseerpy)
      - [占い結果の取得方法](#占い結果の取得方法)
    - [騎士 (src/agent/bodyguard.py)](#騎士-srcagentbodyguardpy)
    - [村人 (src/agent/villager.py)](#村人-srcagentvillagerpy)
    - [霊媒師 (src/agent/medium.py)](#霊媒師-srcagentmediumpy)
      - [霊媒結果の取得方法](#霊媒結果の取得方法)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

人狼ゲームの役職や流れなどのルールについては、[logic.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/logic.md)を参照してください。

大会参加者はエージェントを実装したうえで、ご自身の端末でエージェントを実行、大会運営が提供するゲームサーバに接続する必要があります。エージェントの実装については、実装言語を含め、制限はありません。\
自己対戦では、5体,13体のエージェントをご自身の端末で実行し、大会運営が提供する自己対戦用のゲームサーバに接続しすることで、エージェント同士の対戦を行うことができます。

ローカル内での動作確認ならびに自己対戦するためのゲームサーバについては、[aiwolfdial/aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server)を参照してください。

## 環境構築

> [!IMPORTANT]
> Python 3.11以上が必要です。

```bash
git clone https://github.com/aiwolfdial/aiwolf-nlp-agent.git
cd aiwolf-nlp-agent
cp config/config.yml.example config/config.yml
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> [!NOTE]
> aiwolf-nlp-commonとは、役職や接続方式に関するプログラムが定義されているPythonパッケージです。\
> 詳細は[aiwolfdial/aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common)を参照してください。

## 実行方法

### エージェントの実行

```bash
python src/main.py
```

#### 設定ファイルを指定して起動する方法

デフォルトでは`config/config.yml`の設定を参照して起動します。\
指定して起動する方法や複数の設定ファイルを同時に実行する方法は以下のとおりです。

```bash
python src/main.py -c config/config_1.yml # config/config_1.ymlを指定する場合
python src/main.py -c config/config_1.yml config/config_2.yml # config/config_1.ymlとconfig/config_2.ymlを指定する場合
python src/main.py -c config/config_*.yml # config/config_*.ymlを指定する場合
```

### ローカル環境での実行

事前にゲームサーバを立ち上げる必要があります。\
[aiwolfdial/aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server)を参照してください。

### 予選の対戦方法

予選は参加登録後に招待されるSlack上で公開されるアドレスに接続することで、対戦できます。\
[設定](#web_socket)の該当項目を変更したうえで、エージェントを実行してください。

### 本戦の対戦方法

本戦は参加登録後に招待されるSlack上で公開されるアドレスに接続することで、対戦できます。\
本戦では`web_socket.auto_reconnect`を`true`にしてください。\
[設定](#web_socket)の該当項目を変更したうえで、エージェントを実行してください。\
対戦状況によって大会運営サーバを停止している時間帯があるため、接続エラー(`[Errno 61] Connection refused`)が発生し、自動で再接続を繰り返す可能性があります。

## 設定 (config/config.yml)

### web_socket

`url`: ゲームサーバのURLです。ローカル内のゲームサーバに接続する場合はデフォルト値で問題ありません。\
`token`: ゲームサーバに接続するためのトークンです。大会運営から提供されるトークンを設定してください。\
`auto_reconnect`: 対戦終了後に自動で再接続するかどうかの設定です。

### agent

`num`: 起動するエージェントの数です。自己対戦の場合はデフォルト値で問題ありません。\
`team`: エージェントのチーム名です。大会運営から提供されるチーム名を設定してください。\
`kill_on_timeout`: アクションタイムアウト時にリクエストの処理を中断するかどうかの設定です。

### log

`console_output`: コンソールにログを出力するかどうかの設定です。\
`file_output`: ファイルにログを出力するかどうかの設定です。\
`output_dir`: ログを保存するディレクトリのパスです。\
`level`: ログの出力レベルです。`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`のいずれかを設定してください。

#### log.requests

`name`, `initialize`, `daily_initialize`, `whisper`, `talk`, `daily_finish`, `divine`, `guard`, `vote`, `attack`, `finish`: 各リクエストのログを出力するかどうかの設定です。

## エージェントのカスタマイズ方法

### 全役職共通 (src/agent/agent.py)

すべての役職に共通する動作を定義するファイルです。

#### リクエストに対応するメソッド

ゲームサーバから送信されるリクエストに対応するメソッドは下記の通りです。

| メソッド名         | 変更推奨度 | 処理                                         |
| ------------------ | ---------- | -------------------------------------------- |
| `name`             | **非推奨** | 名前リクエストに対する応答を返す             |
| `initialize`       | **中**     | ゲーム開始リクエストに対する初期化処理を行う |
| `daily_initialize` | **中**     | 昼開始リクエストに対する処理を行う           |
| `talk`             | **高**     | トークリクエストに対する応答を返す           |
| `daily_finish`     | **中**     | 昼終了リクエストに対する処理を行う           |
| `divine`           | **高**     | 占いリクエストに対する応答を返す             |
| `vote`             | **高**     | 投票リクエストに対する応答を返す             |
| `finish`           | **中**     | ゲーム終了リクエストに対する処理を行う       |

### 人狼 (src/agent/werewolf.py)

人狼の動作を定義するファイルです。\
すべての役職に共通する動作とは別に以下のメソッドがあります。

| メソッド名 | 変更推奨度 | 処理                             |
| ---------- | ---------- | -------------------------------- |
| `whisper`  | **高**     | 囁きリクエストに対する応答を返す |
| `attack`   | **高**     | 襲撃リクエストに対する応答を返す |

### 狂人 (src/agent/possessed.py)

狂人の動作を定義するファイルです。

### 占い師 (src/agent/seer.py)

人狼の動作を定義するファイルです。\
すべての役職に共通する動作とは別に以下のメソッドがあります。

| メソッド名 | 変更推奨度 | 処理                             |
| ---------- | ---------- | -------------------------------- |
| `divine`   | **高**     | 占いリクエストに対する応答を返す |

#### 占い結果の取得方法

占いフェーズ以降の昼開始リクエスト内の`info.divine_result`から取得できます。\
詳細は[judge.py](https://github.com/aiwolfdial/aiwolf-nlp-common/blob/main/src/aiwolf_nlp_common/packet/judge.py)を参照してください。

### 騎士 (src/agent/bodyguard.py)

騎士の動作を定義するファイルです。\
すべての役職に共通する動作とは別に以下のメソッドがあります。

| メソッド名 | 変更推奨度 | 処理                             |
| ---------- | ---------- | -------------------------------- |
| `guard`    | **高**     | 護衛リクエストに対する応答を返す |

### 村人 (src/agent/villager.py)

村人の動作を定義するファイルです。

### 霊媒師 (src/agent/medium.py)

霊媒師の動作を定義するファイルです。

#### 霊媒結果の取得方法

追放フェーズ以降の昼開始リクエスト内の`info.medium_result`から取得できます。\
詳細は[judge.py](https://github.com/aiwolfdial/aiwolf-nlp-common/blob/main/src/aiwolf_nlp_common/packet/judge.py)を参照してください。
