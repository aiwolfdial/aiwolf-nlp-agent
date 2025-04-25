"""エージェントの基底クラスを定義するモジュール."""

from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING

from aiwolf_nlp_common.packet import Info, Packet, Request, Role, Setting, Status, Talk

from utils.agent_logger import AgentLogger
from utils.stoppable_thread import StoppableThread
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if TYPE_CHECKING:
    from collections.abc import Callable


class Agent:
    """エージェントの基底クラス."""

    def __init__(
        self,
        config: dict,
        name: str,
        game_id: str,
        role: Role,
    ) -> None:
        """エージェントの初期化を行う."""
        self.config = config
        self.agent_name = name
        self.agent_logger = AgentLogger(config, name, game_id)
        self.request: Request | None = None
        self.info: Info | None = None
        self.setting: Setting | None = None
        self.talk_history: list[Talk] = []
        self.whisper_history: list[Talk] = []
        self.role = role

        self.comments: list[str] = []
        with Path.open(
            Path(str(self.config["path"]["random_talk"])),
            encoding="utf-8",
        ) as f:
            self.comments = f.read().splitlines()

    @staticmethod
    def timeout(func: Callable) -> Callable:
        """アクションタイムアウトを設定するデコレータ."""

        def _wrapper(self, *args, **kwargs) -> str:  # noqa: ANN001, ANN002, ANN003
            res = ""

            def execute_with_timeout() -> None:
                nonlocal res
                try:
                    res = func(self, *args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    res = e

            thread = StoppableThread(target=execute_with_timeout)
            thread.start()
            timeout_value = (
                self.setting.timeout.action
                if hasattr(self, "setting") and self.setting
                else 0
            ) // 1000
            if timeout_value > 0:
                thread.join(timeout=timeout_value)
                if thread.is_alive():
                    self.agent_logger.logger.warning(
                        "アクションがタイムアウトしました: %s",
                        self.request,
                    )
                    if bool(self.config["agent"]["kill_on_timeout"]):
                        thread.stop()
                        self.agent_logger.logger.warning(
                            "アクションを強制終了しました: %s",
                            self.request,
                        )
            else:
                thread.join()
            if isinstance(res, Exception):
                raise res
            return res

        return _wrapper

    @staticmethod
    def generate_statement(prompt_text: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # gpt-4-turbo
            messages=[
                {"role": "system", "content": "あなたは人狼知能のプレイヤーです。"},
                {"role": "user", "content": prompt_text},
            ],
        )
        return response["choices"][0]["message"]["content"]

    def set_packet(self, packet: Packet) -> None:
        """パケット情報をセットする."""
        self.request = packet.request
        if packet.info:
            self.info = packet.info
        if packet.setting:
            self.setting = packet.setting
        if packet.talk_history:
            self.talk_history.extend(packet.talk_history)
        if packet.whisper_history:
            self.whisper_history.extend(packet.whisper_history)
        if self.request == Request.INITIALIZE:
            self.talk_history: list[Talk] = []
            self.whisper_history: list[Talk] = []
        self.agent_logger.logger.debug(packet)

    def get_alive_agents(self) -> list[str]:
        """生存しているエージェントのリストを取得する."""
        if not self.info:
            return []
        return [k for k, v in self.info.status_map.items() if v == Status.ALIVE]

    def name(self) -> str:
        """名前リクエストに対する応答を返す."""
        return self.agent_name

    def initialize(self) -> None:
        """ゲーム開始リクエストに対する初期化処理を行う."""

    def daily_initialize(self) -> None:
        """昼開始リクエストに対する処理を行う."""

    def whisper(self) -> str:
        """囁きリクエストに対する応答を返す."""
        return random.choice(self.comments)  # noqa: S311

    def talk(self) -> str:
        """トークリクエストに対する応答を返す."""
        return random.choice(self.comments)  # noqa: S311

    def talk(self):
        """トークリクエストに対する応答を返す。"""
        prompt = f"{self.name}です。今日は{self.game_day}日目です。あなたは{self.role}です。次に話すべき内容を1文で答えてください。"
        # OpenAIの関数を呼び出す
        statement = self.generate_statement(prompt)
        return statement

    def daily_finish(self) -> None:
        """昼終了リクエストに対する処理を行う."""

    def divine(self) -> str:
        """占いリクエストに対する応答を返す."""
        return random.choice(self.get_alive_agents())  # noqa: S311

    def guard(self) -> str:
        """護衛リクエストに対する応答を返す."""
        return random.choice(self.get_alive_agents())  # noqa: S311

    def vote(self) -> str:
        """投票リクエストに対する応答を返す."""
        return random.choice(self.get_alive_agents())  # noqa: S311

    def attack(self) -> str:
        """襲撃リクエストに対する応答を返す."""
        return random.choice(self.get_alive_agents())  # noqa: S311

    def finish(self) -> None:
        """ゲーム終了リクエストに対する処理を行う."""

    @timeout
    def action(self) -> str | None:  # noqa: C901, PLR0911
        """リクエストの種類に応じたアクションを実行する."""
        match self.request:
            case Request.NAME:
                return self.name()
            case Request.TALK:
                return self.talk()
            case Request.WHISPER:
                return self.whisper()
            case Request.VOTE:
                return self.vote()
            case Request.DIVINE:
                return self.divine()
            case Request.GUARD:
                return self.guard()
            case Request.ATTACK:
                return self.attack()
            case Request.INITIALIZE:
                self.initialize()
            case Request.DAILY_INITIALIZE:
                self.daily_initialize()
            case Request.DAILY_FINISH:
                self.daily_finish()
            case Request.FINISH:
                self.finish()
        return None
