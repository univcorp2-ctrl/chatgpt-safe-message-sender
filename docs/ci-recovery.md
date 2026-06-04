# CI Recovery Notes

## 現状

GitHub automation worker から `.github/workflows/*` を作成しようとしたところ、GitHub API が `404: Not Found` を返しました。

失敗したパス:

- `.github/workflows/ci.yml`
- `.github/workflows/live-smoke.yml`
- `.github/workflows/ci.yaml`

コード、テスト、docs、devcontainer は main ブランチに作成済みです。

## 推定原因

通常ファイルは作成できているため、リポジトリ作成や push 全体の失敗ではありません。`.github/workflows/*` だけが失敗しているため、GitHub token / GitHub App 側で workflow file を作成・更新する権限が不足している、または GitHub API が workflow scope なしの更新を拒否している可能性が高いです。

## 保存済みテンプレート

workflow と同じ内容を通常ファイルとして保存しています。

- `docs/workflows/ci.yml`
- `docs/workflows/live-smoke.yml`

## 復旧後に反映する場所

権限が復旧したら、上記テンプレートを以下に配置します。

- `docs/workflows/ci.yml` → `.github/workflows/ci.yml`
- `docs/workflows/live-smoke.yml` → `.github/workflows/live-smoke.yml`

## ローカル相当チェック

```bash
bash scripts/run_local_ci.sh
```
