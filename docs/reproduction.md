# 最終評価の再現手順

## 1. 実行環境

- Google Colab、**NVIDIA L4 GPU推奨**（L4で60秒完走を確認）
- Genesis 1.4.4、rsl-rl-lib 5.5.1
- Genesis公式リポジトリの固定コミット `105898fc0a5f068f22dffbbfa39f5ea89be42a1e`
- PyTorch / PythonはColabランタイムの環境を使用（バージョン差には注意）

T4での試行は29.1秒で安全停止しました。L4必須と断定するものではありません。

## 2. 必要な入力ファイル

Google Driveの `MyDrive/PhysicalAI_Go2_Pursuit/` 以下に配置します。

| 用途 | 相対パス |
|---|---|
| 下位歩行PPO | `training/locomotion/phase112_78e8a86701/phase112_final.pt` |
| 下位歩行設定 | `training/locomotion/locomotion_51ec8dd43f/planned_cfgs.pkl` |
| 上位追跡12D PPO | `training/upper12_genesis/phase50_42b70a6b/upper_pursuit_12d_phase50.pt` |
| 上位回避12D PPO | `training/upper12_genesis/phase50_42b70a6b/upper_evasion_12d_phase50.pt` |

これらは**学習済みモデル本体と設定ファイル**です。学習結果ZIPだけでは代用できません。信頼できるファイルのみをPyTorch/pickleで読み込んでください。公開・配布状況は `model_manifest.md` を参照してください。

## 3. 評価の実行

1. 現在リポジトリにある `notebooks/56_genesis_60s_3d_dot_video.ipynb` は開発版です。L4で再現確認した整理版 `evaluate_mutual_pursuit.ipynb` はGitHubへ未登録のため、同じ手順での再現には整理版Notebookを別途用意する必要があります。
2. 必要に応じてNotebookのDrive基準パスを変更します。
3. 全セルを上から実行します。NotebookがGenesisの指定コミットを取得し、必要モデルを検査します。
4. `close_start` 配置、3,000ステップ、制御周期20 ms、上位Phase50・下位Phase112、手動yaw制限なしで評価します。
5. 結果ZIPを取得します。

## 4. 出力と検証

結果ZIPには `run.log`、`trajectory.csv`、`tag_events.csv`、`joint_poses.csv`、`joint_name_mapping.csv`、`ppo_training_rollout.csv` などが含まれます。

- `trajectory.csv`：2体合計6,000行、最大stepが3,000であること
- `tag_events.csv`：役割交代8行であること
- `run.log`：`TAG_COUNT 8` と `steps 3000` を確認

元の評価・L4再実行では役割交代が **208 / 614 / 1043 / 1332 / 1701 / 2017 / 2303 / 2662 step** で発生しました。完全一致は保証しません。条件が異なる場合は結果を記録し、失敗を成功扱いしないでください。

## 5. 学習と描画の区別

本Notebookは**学習済みモデルの評価**であり、PPOを再学習しません。追跡・回避モデルの学習経路、8D→12D転写、Genesisロールアウト、追加PPO更新は別のNotebook群に記録されています。

PyBulletによるGo2 URDF動画は、Genesisで取得した `joint_poses.csv` 等の**記録済みデータの描画**です。Genesisの評価結果をPyBulletで再シミュレーションしたものではありません。
