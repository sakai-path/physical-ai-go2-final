# 最終評価の再現手順

## 1. 実行環境

- Google Colab / NVIDIA L4 GPU推奨（L4での60秒完走記録あり）
- Genesis 1.4.4、rsl-rl-lib 5.5.1
- Genesis公式リポジトリの固定コミット `105898fc0a5f068f22dffbbfa39f5ea89be42a1e`
- PyTorch / PythonはColabランタイムの環境を使用

T4での試行は29.1秒で機体高さによる安全停止が発生しました。GPU差が原因とは断定できません。

## 2. 必要なモデル・設定

最終評価に必要なファイルはすべて公開リポジトリの [`models/`](../models/) にあります。

| 用途 | ファイル |
|---|---|
| 下位歩行PPO | `models/phase112_final.pt` |
| 下位歩行設定 | `models/planned_cfgs.pkl` |
| 上位追跡12D PPO | `models/upper_pursuit_12d_phase50.pt` |
| 上位回避12D PPO | `models/upper_evasion_12d_phase50.pt` |

公開済みのPhase56 Notebookは、このリポジトリをColabにcloneし、上記4ファイルを直接読み込みます。**Google Driveへの配置は不要**です。

## 3. 最終評価の実行

1. [`notebooks/56_genesis_60s_3d_dot_video.ipynb`](../notebooks/56_genesis_60s_3d_dot_video.ipynb) をGoogle Colabで開きます。
2. GPUランタイム（L4推奨）を選び、セルを上から順に実行します。
3. NotebookがGenesisの固定コミットを取得し、公開済みモデル4ファイルの存在と形式を確認します。
4. `close_start` の初期配置、3,000ステップ、20ms刻み、下位Phase112・上位Phase50、手動yaw制限なしで評価します。
5. 結果ZIPをColabからダウンロードします。

**実行確認状況：** 開発時のL4環境で60秒・8回の役割交代を確認しています。公開済みモデルをGitHubから直接取得するように変更したNotebookについては、GPU上での通し実行をまだ確認していません。

Notebookには開発時のPhase40〜46に由来するrunnerの構築・変更処理が含まれます。これは最終評価に必要なスクリプトを組み立てる工程であり、PPOモデルを追加学習する処理ではありません。

## 4. 結果の確認

結果ZIPには `run.log`、`trajectory.csv`、`tag_events.csv`、`joint_poses.csv`、`joint_name_mapping.csv`、`ppo_training_rollout.csv` などが含まれます。

結果ZIPを取得後、リポジトリのルートで次を実行します。

```bash
python scripts/verify_phase56_results.py path/to/phase56_results.zip
```

この検証は2体×3,000ステップのCSV構造と役割交代8回を確認します。**Genesisの物理シミュレーションを再実行するものではありません。**

元の最終評価・L4再実行での役割交代ステップは 208、614、1043、1332、1701、2017、2303、2662 でした。環境差があるため完全一致は保証しません。

## 5. モデルファイルの検証

リポジトリのルートで次を実行します（PyTorchが必要です）。

```bash
python scripts/verify_model_artifacts.py models
```

モデルの存在、SHA-256、設定の関節数、上位モデルの12D入力構造を確認します。**このコマンドの公開モデル4ファイルに対する実行確認は未実施**です。

`torch.load` と `pickle.load` は任意のコードを実行し得るため、信頼できるファイルに対してのみ使用してください。

## 6. 3D動画

[`notebooks/57_go2_urdf_render_from_phase56.ipynb`](../notebooks/57_go2_urdf_render_from_phase56.ipynb) はPhase56の結果ZIPを読み込み、Go2 URDFによる3D動画を生成します。PyBulletは記録データの描画に使用し、物理シミュレーションの再計算には使用しません。

学習済みモデルの生成・PPO更新は実験用リポジトリで実施しました。公開版は**最終評価と結果確認**を対象としています。
