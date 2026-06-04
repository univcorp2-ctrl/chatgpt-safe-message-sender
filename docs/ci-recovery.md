# CI Recovery Notes

## 現状

GitHub automation worker から `.github/workflows/*` を作成しようとしたところ、GitHub API が `404: Not Found` を返しました。

失敗したパス:

- `.github/workflows/ci.yml`
- `.github/workflows/live-smoke.yml`
- `.github/workflows/ci.yaml`

main ブランチ、専用ブランチ `add-ci-workflows` の両方で試しましたが、同じく `.github/workflows/*` だけ失敗しました。

## 推定原因

通常ファイルは作成できているため、リポジトリ作成や push 全体の失敗ではありません。`.github/workflows/*` だけが失敗しているため、GitHub token / GitHub App 側で workflow file を作成・更新する権限が不足している可能性が高いです。

GitHub REST API の repository contents ドキュメントでも、`.github/workflows` ディレクトリのファイル変更には `workflow` scope が必要とされています。

## 保存済みテンプレート

workflow と同じ内容を通常ファイルとして保存しています。

- `docs/workflows/ci.yml`
- `docs/workflows/live-smoke.yml`

## 復旧後に反映する場所

権限が復旧したら、上記テンプレートを以下に配置します。

- `docs/workflows/ci.yml` → `.github/workflows/ci.yml`
- `docs/workflows/live-smoke.yml` → `.github/workflows/live-smoke.yml`

## Actions に依存しない検証ルート

GitHub Actions workflow がまだ有効化できない場合でも、以下の検証ルートを用意しています。

```bash
make verify
bash scripts/run_local_ci.sh
bash scripts/run_until_green.sh
docker build -t chatgpt-safe-message-sender:local .
```

`docker build` は build 中に lint、format check、pytest、dry-run を実行するため、途中で失敗すると image が完成しません。
