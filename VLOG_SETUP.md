# Vlog自動編集パイプライン — セットアップ手順

Claude Codeで動画編集を完全自動化するための手順書です。

---

## 必要なツールのインストール

### 1. システムツール（ffmpeg）

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows (winget)
winget install ffmpeg
```

### 2. Python環境とライブラリ

```bash
# Python 3.10以上が必要
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

> `openai-whisper` は初回実行時にモデルファイル（large-v3: 約3GB）を自動ダウンロードします。

### 3. Anthropic APIキーの設定

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # macOS/Linux
# または .env ファイルに記載しておく
```

---

## 使い方

### 基本的な実行

```bash
python vlog_auto_edit.py 動画ファイル.mp4
```

### BGMを追加する場合

```bash
python vlog_auto_edit.py ロンドンvlog.mp4 --bgm bgm/lofi_bgm.mp3
```

### オプション一覧

| オプション | 説明 | デフォルト |
|---|---|---|
| `--bgm` | BGMファイルのパス | なし |
| `--output` | 出力ファイル名 | `final_output.mp4` |
| `--language` | 字幕の言語コード | `ja` |
| `--skip-cuts` | ジャンプカットをスキップ | オフ |
| `--skip-bgm` | BGM挿入をスキップ | オフ |

---

## パイプラインの流れ

```
入力動画 (例: london_vlog.mp4)
    │
    ├─ [Step 1] ffmpeg で音声抽出 → audio.wav
    │
    ├─ [Step 2] silencedetect で無音区間を検出
    │              → ジャンプカット適用 (cut.mp4)
    │
    ├─ [Step 3] Whisper large-v3 で文字起こし
    │              → SRT字幕生成 → 動画に焼き込み (subtitled.mp4)
    │
    ├─ [Step 4] ffmpeg amix で BGM をミックス (with_bgm.mp4)
    │
    ├─ [Step 5] Claude API でファクトチェック
    │              → 製品・場所名を抽出 → テロップ追加 (with_telops.mp4)
    │
    └─ [Step 6] Claude API で最終検証
                   → 誤字・内容チェック → 品質スコア出力
                   → final_output.mp4 完成
```

---

## 出力ファイル

実行後、`動画名_work/` ディレクトリに以下が生成されます：

| ファイル | 内容 |
|---|---|
| `audio.wav` | 抽出した音声 |
| `audio.srt` | 生成した字幕ファイル |
| `cut.mp4` | ジャンプカット済み動画 |
| `subtitled.mp4` | 字幕付き動画 |
| `with_bgm.mp4` | BGMミックス済み動画 |
| `with_telops.mp4` | テロップ追加済み動画 |
| `telops.json` | ファクトチェック結果 |
| `verification.json` | 最終検証レポート |
| `../final_output.mp4` | **最終完成動画** |

---

## 各ステップのカスタマイズ

### 無音検出の感度を調整する

`vlog_auto_edit.py` の上部の定数を変更します：

```python
SILENCE_THRESHOLD_DB = "-35dB"   # 数値を大きくすると感度が上がる (例: -30dB)
SILENCE_MIN_DURATION = 0.4        # 秒：これ以下の無音は残す（語間の自然な間を保持）
```

### BGMの音量を変える

```python
BGM_VOLUME = 0.08    # 0.0〜1.0（0.08 = BGMを8%の音量でミックス）
```

### 字幕のデザインを変える

```python
OUTPUT_SUBTITLE_STYLE = (
    "FontName=Noto Sans CJK JP,FontSize=20,..."
)
```

---

## よくある質問

**Q: GPUがない場合は？**  
A: Whisper は CPU でも動作しますが、`large-v3` モデルは時間がかかります。`--model medium` に変更するか、`openai-whisper` の代わりに OpenAI の Whisper API を使用してください。

**Q: 英語動画に対応できますか？**  
A: `--language en` を指定してください。多言語対応しています。

**Q: BGM素材はどこで入手できますか？**  
A: フリー素材サイト（例：Pixabay Music、Free Music Archive）からダウンロードできます。
