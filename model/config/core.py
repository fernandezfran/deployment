import pathlib
import typing as t

import pydantic
import strictyaml

import model

# Project Directories
PACKAGE_ROOT = pathlib.Path(model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"


class AppConfig(pydantic.BaseModel):
    """Application-level config."""

    package_name: str
    raw_data_file: str
    pipeline_save_file: str


class ModelConfig(pydantic.BaseModel):
    """All configuration relevant to model training and feature engineering."""

    target: str
    unused_fields: t.Sequence[str]
    features: t.Sequence[str]
    test_size: float
    random_state: int
    numerical_vars: t.Sequence[str]
    categorical_vars: t.Sequence[str]
    cabin_vars: t.Sequence[str]


class Config(pydantic.BaseModel):
    """Master config object."""

    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> pathlib.Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(
    cfg_path: t.Optional[pathlib.Path] = None,
) -> strictyaml.YAML:
    """Parse YAML containing the package configuration."""
    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = strictyaml.load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: strictyaml.YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
