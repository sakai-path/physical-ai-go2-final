# Mutual Pursuit and Evasion with Two Unitree Go2 Robots

**同一の制御構成を持つ2体のロボットは、互いを追跡・回避し続けられるか？**

Physical AI 応用編1の最終課題として、Genesis上に2体のUnitree Go2を配置し、強化学習による歩行・追跡・回避と、距離に応じた役割交代を組み合わせました。

## システム構成

![2体のGo2の階層型PPO制御と役割交代を示す白黒のシステム構成図](docs/system_architecture.svg)

2体は同じ制御構成とモデル群を使用します。ただし、**追跡と回避は別々に学習した方策**で、役割交代は**学習ではなく距離閾値によるルール制御**です。上位PPOの観測を8Dから姿勢・角速度を含む12Dへ拡張し、Genesisで収集した遷移を使って追加学習しました。

## 最終評価

Genesis 1.4.4で、下位歩行PPO（Phase112）と上位12D PPO（Phase50）を使用。近距離初期配置 `close_start`、20 ms刻み、手動yaw指令制限なしで60秒評価しました。

| 指標 | 結果 |
|---|---:|
| 評価時間 | 60.00秒（3,000ステップ） |
| 役割交代 | 8回 |
| 最終2体間距離 | 0.523 m |
| 最大絶対Roll / Pitch | 4.72° / 7.01° |
| 最低機体高さ | 0.197 m |
| 軌跡データ | 6,000行（2体×3,000） |

公開用評価Notebookを用いた**Google Colab / NVIDIA L4**での再実行でも、60秒完走と8回の役割交代を確認しました。役割交代ステップは元の評価記録と一致しました。一方、**T4**での実行では29.1秒（1,455ステップ）で機体高さによる安全停止が発生しました。GPU差が原因と断定するものではありません。

この結果は**1つの初期配置・1つの長時間実行**であり、あらゆる条件での安定性や12D姿勢入力の有効性を証明するものではありません。

## 実行環境

- **実行基盤：** Google Colab（NVIDIA L4 GPU）
- **シミュレータ：** Genesis 1.4.4
- **強化学習：** PyTorch / RSL-RL 5.5.1
- **映像描画：** PyBullet（Genesisの記録データを描画）

最終評価の60秒完走・8回の役割交代はL4環境で確認しました。T4環境では同条件の実行が途中停止しており、GPU差が原因と断定するものではありません。

## 再現・ファイル

- [`notebooks/56_genesis_60s_3d_dot_video.ipynb`](notebooks/56_genesis_60s_3d_dot_video.ipynb) — Genesisで60秒評価した開発版Notebook（公開用整理版は登録準備中）
- [`scripts/verify_phase56_results.py`](scripts/verify_phase56_results.py) — Phase56結果ZIPのCSV構造と60秒・8回の役割交代を検査（物理シミュレーションの再実行ではありません）
- [`docs/reproduction.md`](docs/reproduction.md) — Colabの実行手順、必要ファイル、検証方法
- [`docs/model_manifest.md`](docs/model_manifest.md) — 必要な学習済みモデルと設定
- [`docs/experiment_summary.md`](docs/experiment_summary.md) — 結果と評価上の制約

**注意：** [`models/`](models/) に上位追跡・回避PPOと歩行設定を公開しました。下位歩行PPOを含む4ファイルすべてを公開済みです。評価Notebookは現在Google Drive上の配置を参照するため、実行時にパス調整が必要です。詳細は [`docs/model_manifest.md`](docs/model_manifest.md) を参照してください。

## 公開範囲と再現性の制約

本リポジトリは提出用の最終評価Notebook、技術資料、結果の検証スクリプトをまとめたものです。**下位歩行・上位追跡・上位回避のPPOモデルと設定ファイルは公開済みです。** ただし、Notebookのパス調整や環境構築が必要で、第三者による完全再現は未実施です。

最終結果（60秒、役割交代8回）は特定の初期配置で得たものであり、異なる条件での安定性や12D姿勢観測の効果を保証しません。公開用に整理した評価Notebookは未登録であり、既存のPhase56 Notebookは開発過程を含む記録です。実験の再現性は今後の課題です。

## 動画について

実験の物理計算・制御は**Genesis**で行っています。PyBulletは記録済みの関節姿勢をGo2 URDFで描画するために使用しており、追跡実験の物理計算には使用していません。

## 技術・課題

Python、PyTorch、PPO、Genesis、RSL-RL、Google Colab、PyBulletを使用。機体高さの低下、初期配置への依存、長時間安定性、12D姿勢入力の寄与の検証が今後の課題です。

## AIの活用について

本プロジェクトでは、設計・実装・検証の過程で生成AIを補助的に活用しました。

ロボットの制御には強化学習（PPO）を使用しており、実験の実施、結果の評価、開発方針の決定は制作者が行っています。

## クレジット・謝辞

- **制作・実験・検証：** 本リポジトリの制作者
- **講座：** 東京大学 松尾・岩澤研究室「Physical AI講座2026 応用編1」（最終課題）
- **ロボットモデル：** Unitree Robotics / Unitree Go2
- **シミュレーション：** [Genesis](https://github.com/Genesis-Embodied-AI/Genesis)
- **強化学習・計算基盤：** [RSL-RL](https://github.com/leggedrobotics/rsl_rl)、[PyTorch](https://pytorch.org/)
- **記録データの3D描画：** [PyBullet](https://pybullet.org/)
- **実行環境：** Google Colab
- **開発補助：** 生成AI

各ソフトウェア・モデルの著作権およびライセンスは、それぞれの権利者・配布元に帰属します。本プロジェクトは、上記の組織・企業による公式な共同開発または承認を意味するものではありません。
