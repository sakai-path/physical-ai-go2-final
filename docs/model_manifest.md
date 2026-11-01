# 最終評価で使用するモデル・設定

| 用途 | ファイル | GitHubへのモデル本体登録 |
|---|---|---|
| 下位歩行PPO（Phase112） | `phase112_final.pt` | 未登録（転送制限により保留） |
| 歩行環境設定 | `planned_cfgs.pkl` | 公開済み |
| 上位追跡12D PPO（Phase50） | `upper_pursuit_12d_phase50.pt` | 公開済み |
| 上位回避12D PPO（Phase50） | `upper_evasion_12d_phase50.pt` | 公開済み |

Google Drive上の正確な配置は [`reproduction.md`](reproduction.md) に記載しています。

Phase50の追跡・回避モデルおよび歩行設定は [`models/`](../models/) に公開しました。下位歩行モデルは現在未登録のため、このリポジトリだけでは最終評価を再実行できません。

既存の古い追跡・回避8Dモデルのハッシュ値を、Phase50の12Dモデルのハッシュ値として流用しません。公開したモデルのSHA-256は、GitHubから取得したファイルを使って確認してください。

## Google Drive実体確認（2026-11-01）

Google Driveのプロジェクトフォルダ内で、最終評価に使用する4ファイルの**ファイル名・サイズ・保存先**を確認しました。

| ファイル | サイズ | 状態 |
|---|---:|---|
| `phase112_final.pt` | 4,547,869 bytes | Driveに存在・非共有 |
| `planned_cfgs.pkl` | 1,879 bytes | Driveに存在・非共有 |
| `upper_pursuit_12d_phase50.pt` | 153,426 bytes | Driveに存在・非共有 |
| `upper_evasion_12d_phase50.pt` | 153,426 bytes | Driveに存在・非共有 |

**公開状況：** 上位2モデルと設定ファイルをGitHubへ登録済み。下位歩行モデルは未登録です。第三者による再実行は未実施です。Driveの共有設定は変更していません。

## ローカル検証

Google ColabでGoogle Driveをマウントした後、信頼できる自分のチェックポイントに対して以下を実行します。

```bash
python scripts/verify_model_artifacts.py /content/drive/MyDrive/PhysicalAI_Go2_Pursuit
```

このスクリプトはファイル存在・SHA-256・設定の12関節・上位モデルの12D入力などを確認します。**スクリプトの登録は完了しましたが、4ファイルに対する実行結果はまだ未取得です。** `torch.load` と `pickle.load` は信頼できるファイルに限って実行してください。
