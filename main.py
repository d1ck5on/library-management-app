from app.subcommands import (
    Add,
    Delete,
    Search,
    UpdateStatus,
    Show,
    ToJson,
)
import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(required=True)
Add.InitParser(subparsers)
Delete.InitParser(subparsers)
Search.InitParser(subparsers)
UpdateStatus.InitParser(subparsers)
Show.InitParser(subparsers)
ToJson.InitParser(subparsers)
args = parser.parse_args()
args.func(args)
