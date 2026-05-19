# FileAgent 設計書

## 概要
JARVISの手足となるローカルファイル操作・コード生成エージェント。
Mac + Windows両方のファイルを操作し、Qwenと連携してコード生成も行う。
将来的にMCPサーバー化を見据えた設計。

## ポート
8006

## 技術スタック
- Python + FastAPI
- Paramiko（SSH接続）
- Ollama（Qwen連携・Windows）
- Git（subprocess）

## ディレクトリ構造
~/Desktop/fileagent/
├── main.py
├── requirements.txt
├── venv/
├── routers/
│   ├── mac_files.py（Macファイル操作）
│   ├── win_files.py（Windowsファイル操作・SSH）
│   ├── git_ops.py（git操作）
│   ├── build.py（xcodebuild・launchctl）
│   └── codegen.py（Qwenコード生成）
├── services/
│   ├── ssh_client.py（SSH接続管理）
│   └── ollama_client.py（Ollama連携）
└── config.py

## API仕様

### Mac側ファイル操作
- GET /mac/read?path=～ → ファイル読み取り
- POST /mac/write → ファイル書き込み {path, content}
- POST /mac/move → ファイル移動 {src, dst}
- DELETE /mac/delete → ファイル削除 {path}
- GET /mac/list?path=～ → ファイル一覧

### Windows側ファイル操作（SSH経由）
- GET /win/read?path=～ → ファイル読み取り
- POST /win/write → ファイル書き込み {path, content}
- POST /win/move → ファイル移動 {src, dst}
- DELETE /win/delete → ファイル削除 {path}
- GET /win/list?path=～ → ファイル一覧

### Git操作
- POST /git/add → git add {path, cwd}
- POST /git/commit → git commit {message, cwd}
- POST /git/push → git push {cwd}
- POST /git/full → add+commit+push一括 {message, cwd}
- GET /git/status → git status {cwd}
- GET /git/log → git log {cwd, limit}

### ビルド・サービス管理
- POST /build/xcode → xcodebuild {scheme, destination}
- POST /build/launchctl → launchctl操作 {action, service}
- GET /build/status → ビルド状態確認

### コード生成（Qwen連携）
- POST /codegen/generate → コード生成 {prompt, language, context}
- POST /codegen/modify → 既存コード修正 {path, instruction}
- POST /codegen/review → コードレビュー {path}

### ヘルス
- GET /health → 全接続状態確認

## セキュリティ
### Mac許可パス
- ~/Desktop/Jarvis/
- ~/jarvis_server/
- ~/Desktop/devbrain/
- ~/Desktop/fixai/
- ~/Desktop/fileagent/
- ~/Desktop/Flowpost/
- ~/Desktop/Cryptagent/
- ~/Desktop/Calendar-Yuto/

### Windows許可パス
- F:\Jarvis
- E:\Jarvis

### SSH設定
- ホスト：192.168.243.196
- ユーザー：aTsuYa
- キー：~/.ssh/jarvis_fileagent

## Ollama設定
- URL：http://192.168.243.196:11434
- コード生成モデル：qwen2.5-coder:7b（将来：Qwen3:8b）
- タイムアウト：60秒

## launchd
- com.fileagent.server.plist
- RunAtLoad: true
- KeepAlive: true
