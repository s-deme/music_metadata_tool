"""CLI のエントリポイントを公開するモジュール。"""

from music_metadata_lib.interface.cli.main import app, run

__all__ = ["app", "run"]


if __name__ == "__main__":
    run()
