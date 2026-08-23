# Higgsfield 生成プロンプト集｜基準キーフレーム＋第1話

台本：台本/ななえママ_ショートドラマ台本_v8_10話30秒版.md
各コードブロックが1回の生成に対応する。そのままコピー＆ペーストで使用可。

## 共通設定

- aspect_ratio: 9:16 を毎回明示する（省略すると横型になるモデルがある）
- 静止画：人物リアリティ重視のモデル
- 動画：image-to-video。直前に作った静止画を start_image に指定する

## 共通ネガティブプロンプト（全生成に付与）

```
low quality, blurry face, distorted hands, extra fingers, duplicate person, inconsistent identity, inconsistent age, changing hairstyle, changing clothes within the same scene, Western-looking environment, unreadable text, fake QR code, broken subtitles, robotic facial expression, exaggerated crying, melodramatic acting, excessive slow motion, overused rain, generic corporate advertising, luxury imagery unrelated to the story, unrealistic success montage, random business meeting, disconnected scenes, timeline inconsistency, watermark, text overlay, anime, 3d render, plastic skin
```

---

# ステップ1：基準キーフレーム 10枚（静止画）

## KF-01｜52歳・現在・正面

```
Character reference, front view. A 52-year-old Japanese woman, soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin, elegant low chignon with a few loose strands, fine laugh lines, calm confident gaze, refined natural makeup, deep-navy silk long-sleeve dress with subtle sheen, small pearl earrings. Standing in a dimly lit Ginza hostess club before opening, warm amber practical lights, mahogany walls softly out of focus behind her. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-02｜52歳・現在・3/4アングル

```
Character reference, three-quarter view, head turned slightly to camera left. A 52-year-old Japanese woman, soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin, elegant low chignon with a few loose strands, fine laugh lines, refined natural makeup, deep-navy silk long-sleeve dress with subtle sheen, small pearl earrings. Dimly lit Ginza hostess club, warm amber key light from the left. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-03｜52歳・現在・横顔

```
Character reference, profile view. A 52-year-old Japanese woman, soft oval face, straight nose, double eyelids, warm dark-brown eyes, small mouth, fair skin, elegant low chignon with a few loose strands, fine laugh lines, refined natural makeup, deep-navy silk long-sleeve dress. Dimly lit Ginza hostess club, warm rim light from behind, dark background. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-04｜8歳（1982年）

```
An 8-year-old Japanese girl, soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin, black bob with straight blunt bangs, thin frame, wearing a faded pink sweatshirt. Sitting at a wooden study desk in a six-tatami room of a privately owned early-1980s Japanese concrete condominium apartment — not public housing, but the modest, decently kept home of a white-collar family — with a sliding paper screen door and an old bookshelf, late afternoon sunlight slanting through the window, dust floating in the air. Photorealistic cinematic film still, shallow depth of field, muted warm color grade, natural film grain, vertical 9:16.
```

## KF-05｜13歳（1987年）

```
A 13-year-old Japanese girl, the same face as the 8-year-old reference: soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin. Black hair in a low ponytail, navy sailor-collar school uniform, slightly harder and more closed-off expression. Sitting at the same wooden study desk in the same six-tatami condominium room, dusk light, the room slightly emptier than before. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-06｜17歳・高校生

```
A 17-year-old Japanese girl, the same face: soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin. Semi-long dark brown hair, plain grey school cardigan over a white blouse, standing in the narrow hallway of a small 1990s Japanese apartment, a half-packed bag at her feet, flat overcast daylight from a frosted window. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-07｜21〜23歳（1996–98年）

```
A Japanese woman in her early twenties, the same face: soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin. Long dark brown hair with soft waves, black long-sleeve hostess dress, careful late-1990s makeup, visibly tired eyes. Sitting in a small club dressing room in front of a bulb-lit mirror, cluttered cosmetics, late-1990s Japan. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-08｜21〜23歳・腫れた頬版

```
A Japanese woman in her early twenties, the same face and the same long dark brown wavy hair and the same black long-sleeve hostess dress as the previous reference. Her right cheekbone and under-eye are visibly swollen with a purple-yellow bruise, partially covered with foundation. She is applying more foundation with a sponge, looking at herself in a bulb-lit dressing room mirror, expression flat and controlled, not crying. Late-1990s Japan. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-09｜24〜28歳（1999–2003年）

```
A Japanese woman in her mid-twenties, the same face: soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin. Elegant upswept hair, black floor-length evening dress, refined makeup, composed posture. Standing in a high-end Ginza hostess club with mahogany walls, low warm lighting, crystal glassware softly out of focus. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

## KF-10｜40歳（2015年）

```
A 40-year-old Japanese woman, the same face: soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin. Shoulder-length dark brown hair with soft curls, deep navy dress, composed but weary expression. Standing alone in a quiet apartment at night, a single warm lamp, city lights out of focus through the window. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

---

# ステップ2：第1話「机の中の遺書」6ショット

## S1-01｜0–3秒｜銀座のビルを見上げる

画像
```
A 52-year-old Japanese woman, soft oval face, straight nose, double eyelids, warm dark-brown eyes, elegant low chignon, deep-navy silk long-sleeve dress, standing on a narrow Ginza back street at night, seen from behind her shoulder, looking up at a slim three-storey building whose small sign has just lit up. Wet asphalt reflecting amber and white signage, closed shutters on both sides, no crowd. Low angle. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

動画（3秒）
```
Slow push-in from behind her shoulder toward the lit sign. She tilts her head up slightly. Subtle handheld float. The signage flickers on. No other movement, no crowd, no camera whip.
```

## S1-02｜3–7秒｜スタッフを送り出す

画像
```
The same 47-year-old Japanese woman, elegant low chignon, deep-navy silk long-sleeve dress, inside a dim Ginza hostess club before opening. She is speaking to a young female staff member, one hand lightly on the young woman's arm. Six staff in black stand along a mahogany bar behind them. Warm amber practical lights, polished glassware. Medium shot. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

動画（4秒）
```
Medium shot, slow lateral dolly to the right past the line of staff. She nods once and smiles briefly. The staff turn toward the door. Natural human pacing, no slow motion, no exaggerated gestures.
```

## S1-03｜7–11秒｜顔にプッシュイン

画像
```
Close-up of the same 52-year-old Japanese woman's face, three-quarter view, soft oval face, double eyelids, warm dark-brown eyes, fine laugh lines, elegant low chignon. Warm amber club light from the left, dark background. Eyes still, a faint smile just beginning to fade. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

動画（4秒）
```
Slow push-in to a medium close-up. Her smile fades. She lowers her eyes once, then holds. Minimal movement, no head turn, no blinking loop.
```

演出メモ：この目を伏せる瞬間の顔のサイズと画角を、次のS1-04の8歳の顔と完全に一致させる。マッチカットの成否はここで決まる。生成後、2枚を並べて頭部サイズを確認すること。

## S1-04｜11–17秒｜8歳へマッチカット

画像
```
An 8-year-old Japanese girl, the same face as the adult reference: soft oval face, straight nose, double eyelids, warm dark-brown eyes with slightly downturned outer corners, small mouth, fair skin. Black bob with straight blunt bangs, faded pink sweatshirt. Sitting at a wooden study desk in a six-tatami room of a privately owned early-1980s Japanese concrete condominium apartment — not public housing, but the modest, decently kept home of a white-collar family — late afternoon sunlight slanting through the window, dust floating in the air. Close-up, three-quarter view, the head occupying the same portion of the frame as the previous adult close-up. Photorealistic cinematic film still, shallow depth of field, muted warm color grade, natural film grain, vertical 9:16.
```

動画（6秒）
```
The girl slowly lifts her eyes toward the camera. The late afternoon light shifts slightly across her face. Dust drifts in the air. The camera holds completely still, no push-in, no pan.
```

## S1-05｜17–24秒｜引き出しの遺書

画像
```
Close-up of a small child's hand pulling open the drawer of a 1982 Japanese wooden study desk. Inside the drawer, a folded sheet of writing paper lies among erasers, a pencil case and a plastic ruler. Warm late-afternoon light from the left. The writing on the paper is not legible. Photorealistic cinematic film still, shallow depth of field, muted warm color grade, natural film grain, vertical 9:16.
```

動画（7秒）
```
The small hand opens the drawer, takes out the folded paper, unfolds it, adds a short line with a pencil, folds it again, places it back and closes the drawer. One continuous action. The camera is locked off. The text on the paper stays out of focus and unreadable.
```

演出メモ：便箋の文字は読めない解像度に留める。文面を創作しないため。

## S1-06｜24–30秒｜ドアの方を見る

画像
```
The same 8-year-old Japanese girl with a black blunt-banged bob and faded pink sweatshirt, in the same six-tatami condominium room at night, turned toward a closed sliding paper screen door, her hand still resting on the just-closed desk drawer. A faint red light sweeps across the paper screen behind her. Single dim ceiling bulb. Photorealistic cinematic film still, shallow depth of field, muted color grade, natural film grain, vertical 9:16.
```

動画（6秒）
```
She turns her head toward the door and holds still. A red light sweeps slowly across the paper screen behind her once, then fades. No other movement. Unsettling stillness, no music-video energy.
```

---

# 生成順の推奨

1. KF-01〜03（現在の顔）を作り、顔を確定する
2. KF-04（8歳）を作り、KF-01と並べて同一人物に見えるか確認する
3. ここで一度止めて、顔の方向性を承認する
4. 残りのKF-05〜10を作る
5. S1-01〜06の画像 → 承認 → 動画化

ご本人の写真がある場合、KF-01〜03は不要。写真を1〜4枚ならReference Element、5枚以上ならSoul Characterとして登録し、全ショットで参照する。そのほうが顔の精度は高い。

# 第1話のナレーションとテロップ（音声生成・編集用）

| 秒 | ナレーション | テロップ |
|---|---|---|
| 0–3 | 銀座で23年。ビルを一棟持ち、七つの事業を経営する女性がいる。 | 銀座28年／一棟のビル、七つの事業 |
| 3–7 | 52歳。彼女を成功者と呼ぶ人は、多い。 | 52歳。成功者と呼ばれる |
| 7–11 | けれど彼女は、そう呼ばれるたびに、あるものを思い出すという。 | けれど、彼女は |
| 11–17 | 昭和のマンションの、六畳の子ども部屋。／小学2年生だった彼女が、学習机の引き出しに入れていたもの。 | 8歳 |
| 17–24 | 自分で書いた、遺書だった。／彼女はときどきそれを書き直しては、また引き出しにしまっていた。 | 遺書 |
| 24–30 | なぜ8歳の子どもが、遺書を書いたのか。／その答えは、彼女の家にあった。 | 次回：警察が来る家 |

ナレーション音声：日本語、女性または中性的な語り、落ち着いた低めのトーン、1.3〜1.4倍速、感情を張らずに読む。
