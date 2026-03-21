#!/usr/bin/env python3
import os
import sys
from enum import Enum
from typing import Dict
import inspect

import yaml


class YamlUtil:

    @staticmethod
    def load(path, config: Dict = {}) -> Dict:
        try:
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
                return config
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                for key, value in config.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            pass
        return config

    @staticmethod
    def save(path, config: Dict) -> Dict:
        try:
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        except:
            pass
        return config


class BaseEnum:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        clsModule = cls.__module__
        cls_path = inspect.getfile(cls)
        clsFullName = f"{cls.__module__}.{cls.__name__}"
        cls_dirpath = os.path.dirname(cls_path)  # .../src
        clsModulePath = clsModule.replace(".", "\\")
        current_dir = os.path.dirname(os.path.abspath(__file__))  # .../src
        config_path = os.path.join(cls_dirpath, "config.yaml")
        config = YamlUtil.load(config_path)
        cls.init(config)
        env = config.get("env")
        if env:
            env_config_path = os.path.join(cls_dirpath, f"config-{env}.yaml")
            env_config = YamlUtil.load(env_config_path)
            cls.init(env_config)

    @classmethod
    def init(cls, config=None):
        clsName = cls.__name__
        clsConfig = config and config.get(clsName)
        if clsConfig:
            for config_key, config_value in clsConfig.items():
                new_config_key = config_key = config_key.upper().replace("-", "_")
                if hasattr(cls, new_config_key):
                    setattr(cls, new_config_key, config_value)


class ApiEnum(BaseEnum):
    API_KEY = ""

    DATABASE_URL = ""

    BASE_URL_OPEN_API = ""

    BASE_URL_HEALTH = ""

    OPEN_TOKEN = ""

    TOKEN = ""

    DEFAULT__REQUEST_TIMEOUT = 120

    DEFAULT__PAGE_SIZE = 5

    DEFAULT__PAGE_SIZE_MAX = 65536

    GET_DOWNLOAD_URL__URL = BASE_URL_OPEN_API + "/api/tos/get-download-url"


class ConstantEnum(BaseEnum):
    class SourceEnum(Enum):
        ARK_CLAW = "ARK_CLAW"
        JVS_CLAW = "JVS_CLAW"
        LIGHT_CLAW = "LIGHT_CLAW"
        WUHONG = "WUHONG"
        COZE = "COZE"
        SKILL_HUB = "SKILL_HUB"
        CLAW_HUB = "CLAW_HUB"
        FEISHU = "FEISHU"
        DINGTALK = "DINGTALK"
        WEIXIN = "WEIXIN"
        YUANBAO = "YUANBAO"
        WECOM = "WECOM"
        QQBOT = "QQBOT"

    APP__ID = ""

    APP__SOURCE = SourceEnum.CLAW_HUB.value

    IS_DEBUG = False

    CURRENT__OPEN_ID = ""

    CURRENT__USER_NAME = ""

    CURRENT__TENTANT_CODE = ""

    FEISHU_APP__ID = ""

    FEISHU_APP__SECRET = ""

    FEISHU_APP__RECEIVE_ID = ""

    SUPPORTED_FORMATS = ["mp4", "avi", "mov"]
    MAX_FILE_SIZE_MB = 10
    DEFAULT__OUTPUT_LEVEL = "json"

    @staticmethod
    def is_debug():
        return ConstantEnum.IS_DEBUG

    @classmethod
    def init(cls, config=None):
        super().init(config)
        openclaw_sender_open_id = os.environ.get("OPENCLAW_SENDER_OPEN_ID")
        openclaw_sender_username = os.environ.get("OPENCLAW_SENDER_USERNAME")
        feishu_open_id = os.environ.get("FEISHU_OPEN_ID")
        if openclaw_sender_open_id:
            cls.CURRENT__OPEN_ID = openclaw_sender_open_id
        if openclaw_sender_username:
            cls.CURRENT__USER_NAME = openclaw_sender_username
        if feishu_open_id:
            cls.FEISHU_APP__RECEIVE_ID = feishu_open_id
