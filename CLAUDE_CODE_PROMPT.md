# FileAgent 実装指示

SPEC.mdを読んで以下を全て実装してください：

1. venv作成・依存インストール（fastapi・uvicorn・paramiko・httpx・gitpython）
2. config.pyにSSH設定・許可パス・Ollama URL定義
3. services/ssh_client.py：paramikoでSSH接続管理・ファイル読み書き・コマンド実行
4. services/ollama_client.py：Qwen連携・コード生成
5. routers/mac_files.py：Macファイル操作（許可パスチェック必須）
6. routers/win_files.py：SSH経由Windowsファイル操作
7. routers/git_ops.py：git操作
8. routers/build.py：xcodebuild・launchctl
9. routers/codegen.py：Qwenコード生成
10. main.py：全ルーター登録・FastAPI起動

## 検証（必須・全て実行）
1. curl http://localhost:8006/health
2. curl 'http://localhost:8006/mac/list?path=~/jarvis_server'
3. curl -X POST http://localhost:8006/mac/write -H 'Content-Type: application/json' -d '{"path": "~/Desktop/fileagent/test.txt", "content": "テスト"}'
4. curl 'http://localhost:8006/mac/read?path=~/Desktop/fileagent/test.txt'
5. curl 'http://localhost:8006/win/list?path=F:\Jarvis'
6. curl -X POST http://localhost:8006/codegen/generate -H 'Content-Type: application/json' -d '{"prompt": "Hello Worldを出力するPython関数", "language": "python"}'

## launchd登録
~/Library/LaunchAgents/com.fileagent.server.plistを作成してlaunchctl loadで登録

## サーバー再起動（必須）
launchctl stop com.fileagent.server 2>/dev/null
sleep 2
launchctl start com.fileagent.server
sleep 5
curl http://localhost:8006/health

## GitHub
gh repo create pitbull24karats-cmd/fileagent --public --source=~/Desktop/fileagent --push
