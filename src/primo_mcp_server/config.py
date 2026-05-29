"""Configuration for the Primo MCP server."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(ENV_PATH, override=True)

REQUIRED_VARS = [
    'PRIMO_BASE_URL',
    'PRIMO_VID',
    'PRIMO_INSTITUTION_NAME',
    'PRIMO_REQUEST_TIMEOUT',
    'PRIMO_MAX_RESULTS_PER_REQUEST',
    'PRIMO_DEFAULT_RESULTS',
    'PRIMO_TAB_EVERYTHING',
    'PRIMO_TAB_CATALOGUE',
    'PRIMO_SCOPE_COMBINED',
    'PRIMO_SCOPE_LOCAL',
    'PRIMO_LANGUAGE',
]

for var in REQUIRED_VARS:
    if var not in os.environ:
        raise EnvironmentError(f'Missing required environment variable: {var}. Please configure it in .env')

class PrimoConfig:

    model_config = SettingsConfigDict(env_prefix='PRIMO_')

    # Institution-specific
    base_url: str = os.environ['PRIMO_BASE_URL']
    vid: str = os.environ['PRIMO_VID']
    institution_name: str = os.environ['PRIMO_INSTITUTION_NAME']
    tab_everything: str = os.environ['PRIMO_TAB_EVERYTHING']
    tab_catalogue: str = os.environ['PRIMO_TAB_CATALOGUE']
    scope_combined: str = os.environ['PRIMO_SCOPE_COMBINED']
    scope_local: str = os.environ['PRIMO_SCOPE_LOCAL']

    # Operational
    request_timeout: float = float(os.environ['PRIMO_REQUEST_TIMEOUT'])
    max_results_per_request: int = int(os.environ['PRIMO_MAX_RESULTS_PER_REQUEST'])
    default_results: int = int(os.environ['PRIMO_DEFAULT_RESULTS'])
    language: str = os.environ['PRIMO_LANGUAGE']
    user_agent: str = 'primo-mcp-server/0.1.0'
