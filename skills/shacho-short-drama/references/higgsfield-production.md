# Higgsfield制作リファレンス

実案件で映像を生成し、事故を潰した結果の知見。フェーズ2に入る前に読む。

## 目次

1. NO TEXT RULE（最重要）
2. 共通設定ブロック（毎回コピペする4種）
3. 年代の可読性ルール
4. ネガティブプロンプト
5. プロンプトの書き方

---

## 1. NO TEXT RULE（最重要）

映像生成モデルは日本語文字を正しく描けない。看板・ラベル・書類の文字を捏造し、
必ず文字化けする。実案件で「謎の文字」「誤字」が量産され、作り直しになった。

**テロップは一切Higgsfieldに描かせない。編集アプリで焼き込む。**
そのうえで全ショットのプロンプトに次を入れる。

```
Absolutely no readable text, letters, characters, numbers, signage, logos, labels, book titles, posters or captions anywhere in the frame. Any sign, label or document must be either outside the frame, fully defocused, or blank.
```

文字が出やすい被写体は、設計段階で避けるか処理する。ここを絵コンテの時点で潰しておくと、
生成のやり直しがほぼゼロになる。

| 被写体 | 処理 |
|---|---|
| 店の看板 | 画面外に出し、光だけを入れる |
| ボトルのラベル | 完全にピンボケ、または無地 |
| 売上ボード・指名札 | 数字と名前を出さず、位置と手の動きだけで見せる |
| 通帳・借用書・契約書 | 紙の質感と手の動きのみ。文面は写さない |
| 教科書・ノート・本の背 | 無地か画面外 |
| 携帯の画面 | 光だけ。UIを写さない |
| 振込画面 | 指の動きと光だけ |
| QRコード | Higgsfieldで生成しない。編集で正式データを合成する |

---

## 2. 共通設定ブロック（毎回コピペする4種）

案件ごとに一度作り、全ショットのプロンプトに展開する。
ショットごとに独立生成されるため、参照ではなく毎回インラインで書き下ろすこと。

### SERIES STYLE

```
SERIES STYLE (apply to every shot):
Premium Japanese cinematic biography, photorealistic, vertical 9:16.
Shot on a full-frame cinema camera with prime lenses, shallow depth of field, subtle natural film grain, muted desaturated color grade with warm practical light sources against cool ambient shadow.
Performances are emotionally restrained at all times. Nobody in this series cries loudly, gestures broadly, or looks at the camera unless explicitly instructed.
Camera movement is minimal and motivated: a slow push-in, a slow lateral dolly, or a locked-off frame. Never use whip pans, orbits, drone moves, speed ramps or slow motion.
Every environment must read as authentically Japanese for its stated decade.
This is one person's life, not an advertisement.
```

### CHARACTER LOCK

顔の記述を1本作り、全年代で一字一句同じものを使う。年代ごとに髪型・服・体格だけ差し替える。

```
FACE (identical across all ages):
<例> soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin.
```

年代コード（CHAR-08 / CHAR-13 / CHAR-19 / CHAR-23 / CHAR-40 / CHAR-54 など）を決め、
各コードに「髪型・服装・表情の傾向・西暦」を1行ずつ定義した表を作る。
負傷や加齢のバリエーションは別コードにする（CHAR-23B など）。

### LOCATION LOCK

同じ場所は同じ記述で。アングルの本数まで決めると破綻しない。

```
LOC-<名前> (使う話数):
<場所の構成要素、家具、光の質、時間帯>。Only these N angles.
```

### THIRD PARTY RULE

許諾は主人公本人のものであり、家族・元配偶者・加害者は同意していない第三者。
匿名化しつつ物語を成立させるための定型。

```
THIRD PARTY RULE:
These are real living people who have not consented to appear. They must never be shown with a visible face.
Represent them only through: a back, hands, a mouth in profile behind a glass, footsteps, a voice, or an object they have just left.
Identify them by clothing colour instead of by face.
Never state their names, employers, districts or affiliations.
Violence is never shown. Show only the moment before and the moment after.
```

服の色で人物を識別させるのが要点。顔を出さないと誰が誰か分からなくなるが、
色を固定すれば視聴者は追える。匿名化と可読性が両立する。

---

## 3. 年代の可読性ルール

ショットごとに独立生成されるため、モノのカットだけで構成すると場所・光・服が毎回変わり、
「誰の、いつの話か」が繋がらない。実案件で幼少期が理解不能になった。

1. 過去のショットには必ず主人公の顔を入れる。小道具だけのショットを作らない
2. 1つの年代は1ロケに固定する。アングルは3本まで
3. 顔を映さない第三者は服の色で識別させる
4. 現在→過去はマッチカットで繋ぐ。現在の顔にプッシュイン → 同じ構図・同じ頭部サイズで過去の顔
5. 年齢テロップを画面隅に小さく常時表示する
6. 過去パートのショットは5〜6秒確保する。2〜3秒では何が起きたか読み取れない
7. 1話の中で主人公の衣装を変えない

マッチカットは、直前と直後の頭部サイズを一致させないと成立しない。
両方のキーフレームを生成したら、必ず並べて確認してから動画化に進む。

---

## 4. ネガティブプロンプト

日本語文字対策を先頭に置く。

```
japanese text, kanji, hiragana, katakana, chinese characters, letters, numbers, signage, shop sign, neon sign with characters, logo, brand name, caption, subtitle, watermark, ui overlay, gibberish text, garbled characters, fake writing, book titles, labels, posters, low quality, blurry face, distorted hands, extra fingers, duplicate person, inconsistent identity, inconsistent age, changing hairstyle, changing clothes within the same scene, Western-looking environment, robotic facial expression, exaggerated crying, melodramatic acting, excessive slow motion, overused rain, generic corporate advertising, luxury imagery unrelated to the story, unrealistic success montage, random business meeting, disconnected scenes, timeline inconsistency, anime, 3d render, plastic skin
```

---

## 5. プロンプトの書き方

**1ショット＝1プロンプト。**画像用と動画用を分けて2本書くより、
1本の散文プロンプトに「場面・人物・動き・カメラ・光・禁止事項・感情の意味」をすべて入れたほうが、
発注側が扱いやすく破綻も少ない。

散文で書く。カンマ区切りのタグ列にしない。次の順で組む。

1. 場所と時代
2. 人物（FACE＋年代コードの中身を展開して書く）
3. 何をしているか（1ショット1アクション）
4. 画面内の他の要素と、そこに文字を出さない指示
5. カメラの動き
6. やってはいけないこと（Do not ...）
7. **その場面の感情的な意味を1文で**（The emotional meaning is ...）
8. 画質・グレーディング・アスペクト比

7を書くとモデルの演技が安定する。「悲しい顔」と指示するより、
「この人はこれを何度も経験してきた」と意味を伝えたほうが、抑制の効いた演技になる。

aspect_ratio: 9:16 は毎回明示する。省略すると横型になるモデルがある。
