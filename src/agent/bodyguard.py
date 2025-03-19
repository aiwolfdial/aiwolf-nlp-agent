"""騎士のエージェントクラスを定義するモジュール."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiwolf_nlp_common.packet import Role

from agent.agent import Agent
from utils.timeout import timeout

if TYPE_CHECKING:
    from configparser import ConfigParser


class Bodyguard(Agent):
    """騎士のエージェントクラス."""

    def __init__(
        self,
        config: ConfigParser,
        name: str,
        game_id: str,
        idx: int,
        role: Role,  # noqa: ARG002
    ) -> None:
        """騎士のエージェントを初期化する."""
        super().__init__(config, name, game_id, idx, Role.BODYGUARD)

    @timeout
    def talk(self) -> str:
        """トークリクエストに対する応答を返す."""
        return super().talk()

    @timeout
    def guard(self) -> str:
        """護衛リクエストに対する応答を返す."""
        return super().guard()

    @timeout
    def vote(self) -> str:
        """投票リクエストに対する応答を返す."""
        return super().vote()
