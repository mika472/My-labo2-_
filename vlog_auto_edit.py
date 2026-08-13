#!/usr/bin/env python3
"""
Vlog自動編集パイプライン
- ジャンプカット（無音検出）
- 字幕自動生成（Whisper）
- BGM・効果音挿入
- 製品ファクトチェック＋テロップ化（Claude API）
- 誤字・内容検証（Claude API）
"""

import os
import sys
import json
import subprocess
import re
import argparse
from pathlib import Path
import anthropic

# ---------- 設定 ----------
SILENCE_THRESHOLD_DB = "-35dB"   # 無音判定の閾値
SILENCE_MIN_DURATION = 0.4        # 秒：これ以下の無音は残す
BGM_VOLUME = 0.08                  # BGMの音量（0.0〜1.0）
SFX_VOLUME = 0.4
OUTPUT_SUBTITLE_STYLE = (
    "FontName=Noto Sans CJK JP,FontSize=20,PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,Outline=2,Shadow=0,"
    "Alignment=2,MarginV=30"
)


def run(cmd: list[str], check=True) -> subprocess.CompletedProcess:
    print(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


# ─── Step 1: 音声抽出 ────────────────────────────────────────────────────────
def extract_audio(video_path: Path, work_dir: Path) -> Path:
    audio_path = work_dir / "audio.wav"
    run(["ffmpeg", "-y", "-i", str(video_path),
         "-vn", "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le",
         str(audio_path)])
    print(f"[1] 音声抽出完了: {audio_path}")
    return audio_path


# ─── Step 2: 無音区間を検出してジャンプカットリストを作成 ──────────────────
def detect_jump_cuts(audio_path: Path) -> list[tuple[float, float]]:
    """無音区間を検出し、(start, end) のリストを返す（残す区間）"""
    result = run([
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={SILENCE_THRESHOLD_DB}:d={SILENCE_MIN_DURATION}",
        "-f", "null", "-"
    ], check=False)

    silence_starts, silence_ends = [], []
    for line in (result.stderr or "").splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            silence_starts.append(float(m.group(1)))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m:
            silence_ends.append(float(m.group(1)))

    # 無音区間を除いた「残す区間」に変換
    keep_segments = []
    cursor = 0.0
    for s, e in zip(silence_starts, silence_ends):
        if cursor < s:
            keep_segments.append((cursor, s))
        cursor = e
    # 最後まで残す（動画の総長はffprobeで取得）
    keep_segments.append((cursor, None))

    cut_count = len(keep_segments) - 1
    print(f"[2] ジャンプカット検出完了: {cut_count} カット（{len(keep_segments)} セグメント保持）")
    return keep_segments


def get_duration(video_path: Path) -> float:
    result = run(["ffprobe", "-v", "quiet", "-print_format", "json",
                  "-show_format", str(video_path)])
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def apply_jump_cuts(video_path: Path, segments: list[tuple[float, float]],
                    work_dir: Path, total_duration: float) -> Path:
    """ffmpegのtrimフィルターで無音区間を除去して結合"""
    filter_parts = []
    concat_v, concat_a = [], []

    for i, (s, e) in enumerate(segments):
        end = e if e is not None else total_duration
        filter_parts.append(
            f"[0:v]trim=start={s}:end={end},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={s}:end={end},asetpts=PTS-STARTPTS[a{i}]"
        )
        concat_v.append(f"[v{i}]")
        concat_a.append(f"[a{i}]")

    n = len(segments)
    filter_complex = ";".join(filter_parts)
    filter_complex += f";{''.join(concat_v)}{''.join(concat_a)}concat=n={n}:v=1:a=1[outv][outa]"

    cut_path = work_dir / "cut.mp4"
    run(["ffmpeg", "-y", "-i", str(video_path),
         "-filter_complex", filter_complex,
         "-map", "[outv]", "-map", "[outa]",
         "-c:v", "libx264", "-crf", "18", "-preset", "fast",
         "-c:a", "aac", "-b:a", "192k",
         str(cut_path)])
    print(f"[2b] カット動画生成完了: {cut_path}")
    return cut_path


# ─── Step 3: Whisperで文字起こし → SRT字幕生成 ────────────────────────────
def transcribe_to_srt(audio_path: Path, work_dir: Path,
                      language: str = "ja") -> tuple[Path, str]:
    """whisper CLIを使用（pip install openai-whisper でインストール可能）"""
    run(["whisper", str(audio_path),
         "--model", "large-v3",
         "--language", language,
         "--output_format", "srt",
         "--output_dir", str(work_dir)])

    srt_path = work_dir / "audio.srt"
    full_text = srt_path.read_text(encoding="utf-8") if srt_path.exists() else ""

    # 字幕数をカウント
    subtitle_count = len(re.findall(r"^\d+$", full_text, re.MULTILINE))
    print(f"[3] 文字起こし完了: {subtitle_count} 本の字幕生成")
    return srt_path, full_text


def burn_subtitles(video_path: Path, srt_path: Path, work_dir: Path) -> Path:
    """字幕を動画に焼き込む"""
    sub_path = work_dir / "subtitled.mp4"
    run(["ffmpeg", "-y", "-i", str(video_path),
         "-vf", f"subtitles={srt_path}:force_style='{OUTPUT_SUBTITLE_STYLE}'",
         "-c:a", "copy",
         str(sub_path)])
    print(f"[3b] 字幕焼き込み完了: {sub_path}")
    return sub_path


# ─── Step 4: BGM・効果音を挿入 ────────────────────────────────────────────
def insert_bgm(video_path: Path, bgm_path: Path, work_dir: Path) -> Path:
    """BGMをループ再生しながらミックス"""
    bgm_out = work_dir / "with_bgm.mp4"
    run(["ffmpeg", "-y",
         "-i", str(video_path),
         "-stream_loop", "-1", "-i", str(bgm_path),
         "-filter_complex",
         f"[0:a]volume=1.0[voice];[1:a]volume={BGM_VOLUME}[bgm];"
         "[voice][bgm]amix=inputs=2:duration=first[aout]",
         "-map", "0:v", "-map", "[aout]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest",
         str(bgm_out)])
    print(f"[4] BGM挿入完了: {bgm_out}")
    return bgm_out


# ─── Step 5: Claude APIで製品ファクトチェック → テロップ生成 ──────────────
def factcheck_and_create_telops(transcript: str,
                                 client: anthropic.Anthropic) -> list[dict]:
    """
    文字起こしテキストから製品・サービス名を抽出し、
    ファクトチェックした結果をテロップデータとして返す
    """
    prompt = f"""以下はVlog動画の文字起こしです。

<transcript>
{transcript[:6000]}
</transcript>

1. 動画に登場する「製品名・サービス名・ブランド名・場所名・固有名詞」を全て抽出してください。
2. それぞれについて簡潔な補足情報（価格・特徴・公式情報など）を調査・生成してください。
3. 画面に表示するテロップとして最適な短い文章（20文字以内）を作成してください。
4. そのテロップが映像中のどのタイミング（おおよそ何秒ごろ）に表示すべきか推定してください。

JSON形式で返してください:
{{
  "telops": [
    {{
      "name": "製品・場所名",
      "fact": "補足情報（1〜2文）",
      "display_text": "テロップ文字（20文字以内）",
      "estimated_time_sec": 30
    }}
  ]
}}"""

    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text
    # JSONブロックを抽出
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        data = json.loads(m.group())
        telops = data.get("telops", [])
    else:
        telops = []

    print(f"[5] ファクトチェック完了: {len(telops)} 件のテロップを生成")
    return telops


def apply_telops(video_path: Path, telops: list[dict], work_dir: Path) -> Path:
    """drawtext フィルターでテロップを動画に追加"""
    if not telops:
        return video_path

    drawtext_list = []
    for t in telops:
        sec = int(t.get("estimated_time_sec", 0))
        text = t["display_text"].replace("'", "\\'").replace(":", "\\:")
        drawtext_list.append(
            f"drawtext=text='{text}':fontcolor=white:fontsize=18:"
            f"x=(w-text_w)/2:y=h-80:"
            f"enable='between(t,{sec},{sec+4})':"
            f"box=1:boxcolor=black@0.6:boxborderw=6"
        )

    filter_complex = ",".join(drawtext_list)
    telop_path = work_dir / "with_telops.mp4"
    run(["ffmpeg", "-y", "-i", str(video_path),
         "-vf", filter_complex,
         "-c:a", "copy",
         str(telop_path)])
    print(f"[5b] テロップ合成完了: {telop_path}")
    return telop_path


# ─── Step 6: 最終検証（誤字・内容チェック） ───────────────────────────────
def final_verification(transcript: str, telops: list[dict],
                        client: anthropic.Anthropic) -> dict:
    telop_summary = "\n".join(
        f"- {t['name']}: {t['display_text']} / {t['fact']}" for t in telops
    )
    prompt = f"""以下はVlog動画の文字起こしとテロップ情報です。

【文字起こし（一部）】
{transcript[:3000]}

【生成されたテロップ】
{telop_summary}

以下の観点で検証してください:
1. 誤字・脱字・言い間違いが文字起こしに含まれているか
2. テロップの情報に明らかな誤りや不自然な点はあるか
3. 視聴者に誤解を与えかねない表現はあるか
4. 全体的な動画の品質スコア（100点満点）

JSON形式で返してください:
{{
  "typo_issues": ["問題点のリスト"],
  "factual_issues": ["ファクト問題のリスト"],
  "misleading_expressions": ["誤解表現のリスト"],
  "quality_score": 85,
  "overall_comment": "総評コメント"
}}"""

    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    result = json.loads(m.group()) if m else {}
    score = result.get("quality_score", "N/A")
    print(f"[6] 最終検証完了: 品質スコア {score}/100")
    return result


# ─── メインパイプライン ────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Vlog自動編集パイプライン")
    parser.add_argument("video", help="入力動画ファイルのパス")
    parser.add_argument("--bgm", default=None, help="BGM音楽ファイルのパス（省略可）")
    parser.add_argument("--output", default="final_output.mp4", help="出力ファイル名")
    parser.add_argument("--language", default="ja", help="字幕言語コード（デフォルト: ja）")
    parser.add_argument("--skip-cuts", action="store_true", help="ジャンプカットをスキップ")
    parser.add_argument("--skip-bgm", action="store_true", help="BGM挿入をスキップ")
    args = parser.parse_args()

    video_path = Path(args.video).resolve()
    if not video_path.exists():
        print(f"エラー: 動画ファイルが見つかりません: {video_path}")
        sys.exit(1)

    work_dir = video_path.parent / f"{video_path.stem}_work"
    work_dir.mkdir(exist_ok=True)
    print(f"\n=== Vlog自動編集開始: {video_path.name} ===")
    print(f"作業ディレクトリ: {work_dir}\n")

    # Claude APIクライアント
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("警告: ANTHROPIC_API_KEY が未設定です。ファクトチェック・検証をスキップします。")
    client = anthropic.Anthropic(api_key=api_key) if api_key else None

    # Step 1: 音声抽出
    audio_path = extract_audio(video_path, work_dir)

    # Step 2: ジャンプカット
    if not args.skip_cuts:
        total_dur = get_duration(video_path)
        segments = detect_jump_cuts(audio_path)
        current_video = apply_jump_cuts(video_path, segments, work_dir, total_dur)
        # カット後の音声を再抽出（字幕用）
        audio_path = extract_audio(current_video, work_dir)
    else:
        current_video = video_path

    # Step 3: 字幕生成・焼き込み
    srt_path, transcript = transcribe_to_srt(audio_path, work_dir, args.language)
    if srt_path.exists():
        current_video = burn_subtitles(current_video, srt_path, work_dir)

    # Step 4: BGM挿入
    if not args.skip_bgm and args.bgm:
        bgm_path = Path(args.bgm)
        if bgm_path.exists():
            current_video = insert_bgm(current_video, bgm_path, work_dir)
        else:
            print(f"[4] BGMファイルが見つかりません: {bgm_path}（スキップ）")

    # Step 5: ファクトチェック＋テロップ
    telops = []
    if client and transcript:
        telops = factcheck_and_create_telops(transcript, client)
        telop_json = work_dir / "telops.json"
        telop_json.write_text(json.dumps(telops, ensure_ascii=False, indent=2))
        if telops:
            current_video = apply_telops(current_video, telops, work_dir)

    # Step 6: 最終検証
    verification = {}
    if client and transcript:
        verification = final_verification(transcript, telops, client)
        ver_json = work_dir / "verification.json"
        ver_json.write_text(json.dumps(verification, ensure_ascii=False, indent=2))

    # 最終出力ファイルにコピー
    output_path = video_path.parent / args.output
    import shutil
    shutil.copy2(current_video, output_path)

    print(f"\n=== 完成 ===")
    print(f"出力ファイル: {output_path}")
    if verification:
        print(f"品質スコア: {verification.get('quality_score', 'N/A')}/100")
        comment = verification.get('overall_comment', '')
        if comment:
            print(f"総評: {comment}")
    print(f"作業ファイル: {work_dir}/")


if __name__ == "__main__":
    main()
