"""エージェントを起動するためのモジュール."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from utils.agent_utils import init_agent_from_packet

if TYPE_CHECKING:
    from configparser import ConfigParser

    from agent.agent import Agent

from time import sleep

from aiwolf_nlp_common.client import Client
from aiwolf_nlp_common.packet import Request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def create_client(config: ConfigParser) -> Client:
    """クライアントの作成."""
    return Client(
        url=config.get("websocket", "url"),
        token=(
            config.get("websocket", "token")
            if config.has_option("websocket", "token")
            else None
        ),
    )


def connect_to_server(client: Client, name: str) -> None:
    """サーバーへの接続処理."""
    while True:
        try:
            client.connect()
            logger.info("エージェント %s がゲームサーバに接続しました", name)
            break
        except Exception as ex:  # noqa: BLE001
            logger.warning(
                "エージェント %s がゲームサーバに接続できませんでした",
                name,
            )
            logger.warning(ex)
            logger.info("再接続を試みます")
            sleep(15)


def handle_game_session(
    client: Client,
    config: ConfigParser,
    name: str,
) -> None:
    """ゲームセッションの処理."""
    agent: Agent | None = None
    while True:
        packet = client.receive()
        if packet.request == Request.NAME:
            client.send(name)
            continue
        if packet.request == Request.INITIALIZE:
            agent = init_agent_from_packet(config, name, packet)
        if agent is None:
            raise ValueError(agent, "エージェントが初期化されていません")
        agent.set_packet(packet)
        req = agent.action()
        agent.agent_logger.packet(agent.request, req)
        if req is not None:
            client.send(req)
        if packet.request == Request.FINISH:
            break


def connect(config: ConfigParser, idx: int = 1) -> None:
    """エージェントを起動する."""
    name = config.get("agent", "team") + str(idx)
    while True:
        try:
            client = create_client(config)
            connect_to_server(client, name)
            try:
                handle_game_session(client, config, name)
            finally:
                client.close()
                logger.info("エージェント %s とゲームサーバの接続を切断しました", name)
        except Exception as ex:  # noqa: BLE001
            logger.warning(
                "エージェント %s がエラーで終了しました",
                name,
            )
            logger.warning(ex)
            logger.info("再接続を試みます")
            sleep(15)

        if not config.getboolean("websocket", "auto_reconnect"):
            break
