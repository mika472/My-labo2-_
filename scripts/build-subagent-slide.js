const pptxgen = require('pptxgenjs');

const C = {
  bg:      '13294C',
  zone:    '17305A',
  zoneLn:  '2B4C82',
  cardMain:'24365C',
  cardSub: '1B395A',
  orange:  'F26430',
  orangeS: 'FFB27A',
  cyan:    '5FC6D8',
  paper:   'EEF4FA',
  muted:   'B9C7DA',
  faint:   '5E7BA8',
};
const JP = 'Yu Gothic';
const UI = 'Arial';

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';           // 13.333 x 7.5 in
pres.author = 'AI実践講座';
pres.title = 'サブエージェントの仕組み';

const s = pres.addSlide();
s.background = { color: C.bg };

/* ---------------------------------------------------------------- header */
s.addText('HOW IT WORKS', {
  x: 0.55, y: 0.36, w: 4, h: 0.22, margin: 0,
  fontFace: UI, fontSize: 10, bold: true, charSpacing: 3, color: C.orangeS,
});
s.addText([
  { text: 'サブエージェント', options: { color: C.paper } },
  { text: 'の仕組み',        options: { color: C.orange } },
], {
  x: 0.55, y: 0.60, w: 6.7, h: 0.72, margin: 0,
  fontFace: JP, fontSize: 36, bold: true, valign: 'middle',
});

s.addText('ひとことで言うと', {
  x: 7.35, y: 0.50, w: 5.43, h: 0.24, margin: 0,
  fontFace: JP, fontSize: 10, bold: true, color: C.orangeS,
});
s.addText([
  { text: '本体のAIが、' },
  { text: '目的別の“部下AI”', options: { bold: true, color: C.orangeS } },
  { text: 'に仕事を切り出して同時に働かせ、' },
  { text: '結論だけ', options: { bold: true, color: C.orangeS } },
  { text: 'を受け取る仕組み。' },
], {
  x: 7.35, y: 0.76, w: 5.43, h: 0.60, margin: 0,
  fontFace: JP, fontSize: 12, color: C.paper, lineSpacingMultiple: 1.35,
});

/* ------------------------------------------------------------ three zones */
const ZY = 1.58, ZH = 3.45;
const zones = [
  { x: 0.55, w: 3.55, n: '01', t: '相談を受ける' },
  { x: 4.30, w: 4.75, n: '02', t: '仕事を分けて、同時に走らせる' },
  { x: 9.25, w: 3.53, n: '03', t: '要約だけ受け取る' },
];
zones.forEach(z => {
  s.addShape(pres.ShapeType.roundRect, {
    x: z.x, y: ZY, w: z.w, h: ZH, rectRadius: 0.08,
    fill: { color: C.zone }, line: { color: C.zoneLn, width: 1 },
  });
  s.addText([
    { text: z.n, options: { fontFace: UI, color: C.orange, bold: true } },
    { text: '   ' + z.t, options: { fontFace: JP, color: C.paper, bold: true } },
  ], { x: z.x + 0.22, y: 1.72, w: z.w - 0.4, h: 0.26, margin: 0, fontSize: 12, valign: 'middle' });
});

const CY = 3.345;                         // shared centre line for every node

/* ------------------------------------------------ 01 : you -> the main AI */
s.addShape(pres.ShapeType.roundRect, {
  x: 0.80, y: CY - 0.40, w: 1.10, h: 0.80, rectRadius: 0.06,
  fill: { color: '1D3563' }, line: { color: '7E9BC4', width: 1 },
});
s.addText('あなた', {
  x: 0.80, y: CY - 0.40, w: 1.10, h: 0.80, margin: 0,
  fontFace: JP, fontSize: 12, bold: true, color: C.paper, align: 'center', valign: 'middle',
});
s.addShape(pres.ShapeType.line, {
  x: 1.98, y: CY, w: 0.28, h: 0,
  line: { color: C.paper, width: 1.5, endArrowType: 'triangle' },
});

s.addShape(pres.ShapeType.roundRect, {
  x: 2.30, y: CY - 0.625, w: 1.75, h: 1.25, rectRadius: 0.08,
  fill: { color: C.cardMain }, line: { color: C.orange, width: 1.5 },
});
s.addText('メインAI', {
  x: 2.30, y: CY - 0.55, w: 1.75, h: 0.30, margin: 0,
  fontFace: JP, fontSize: 16, bold: true, color: C.paper, align: 'center',
});
s.addText('＝ 司令塔', {
  x: 2.30, y: CY - 0.23, w: 1.75, h: 0.22, margin: 0,
  fontFace: JP, fontSize: 10, color: C.orangeS, align: 'center',
});
s.addText('あなたが話しているのは\nいつもこの1体だけ', {
  x: 2.30, y: CY + 0.04, w: 1.75, h: 0.50, margin: 0,
  fontFace: JP, fontSize: 9, color: C.muted, align: 'center', lineSpacingMultiple: 1.25,
});
s.addText('頼み方はいつもどおりでいい', {
  x: 0.55, y: 4.66, w: 3.55, h: 0.25, margin: 0,
  fontFace: JP, fontSize: 10, color: C.muted, align: 'center', valign: 'middle',
});

/* ------------------------------- 02 : split the job, run the subagents */
const CARD_X = 5.75, CARD_W = 3.10, CARD_H = 0.71;
const subs = [
  { cy: 2.475, badge: '調', name: '調べ役',  sub: '資料や過去ログを大量に読む' },
  { cy: 3.345, badge: '作', name: '作る役',  sub: '実際に書く・直す・組み立てる' },
  { cy: 4.215, badge: '点', name: '見直し役', sub: '抜けや間違いがないか点検する' },
];

// hand-off arrows: main AI -> each subagent
subs.forEach(a => {
  const dy = a.cy - CY;
  s.addShape(pres.ShapeType.line, {
    x: 4.05, y: Math.min(CY, a.cy), w: CARD_X - 4.05, h: Math.abs(dy),
    flipV: dy < 0,
    line: { color: C.orange, width: 2, endArrowType: 'triangle' },
  });
});

subs.forEach(a => {
  s.addShape(pres.ShapeType.roundRect, {
    x: CARD_X, y: a.cy - CARD_H / 2, w: CARD_W, h: CARD_H, rectRadius: 0.06,
    fill: { color: C.cardSub }, line: { color: C.cyan, width: 1.25 },
  });
  s.addShape(pres.ShapeType.ellipse, {
    x: CARD_X + 0.12, y: a.cy - 0.21, w: 0.42, h: 0.42,
    fill: { color: '235071' }, line: { color: C.cyan, width: 1.25 },
  });
  s.addText(a.badge, {
    x: CARD_X + 0.12, y: a.cy - 0.21, w: 0.42, h: 0.42, margin: 0,
    fontFace: JP, fontSize: 12, bold: true, color: C.cyan, align: 'center', valign: 'middle',
  });
  s.addText(a.name, {
    x: CARD_X + 0.67, y: a.cy - 0.32, w: 2.30, h: 0.24, margin: 0,
    fontFace: JP, fontSize: 12, bold: true, color: C.paper, valign: 'middle',
  });
  s.addText(a.sub, {
    x: CARD_X + 0.67, y: a.cy - 0.09, w: 2.30, h: 0.20, margin: 0,
    fontFace: JP, fontSize: 9, color: C.muted, valign: 'middle',
  });
  s.addShape(pres.ShapeType.roundRect, {
    x: CARD_X + 0.67, y: a.cy + 0.12, w: 2.22, h: 0.21, rectRadius: 0.04,
    fill: { type: 'none' }, line: { color: C.cyan, width: 0.75, dashType: 'dash' },
  });
  s.addText('専用の作業机（メモは持ち帰らない）', {
    x: CARD_X + 0.67, y: a.cy + 0.12, w: 2.22, h: 0.21, margin: 0,
    fontFace: JP, fontSize: 8, color: C.cyan, align: 'center', valign: 'middle',
  });
});

s.addText('3体が同時に動く ＝ 待ち時間が短い', {
  x: 4.30, y: 4.66, w: 4.75, h: 0.25, margin: 0,
  fontFace: JP, fontSize: 10, bold: true, color: C.cyan, align: 'center', valign: 'middle',
});

/* ------------------------------------- 03 : only the summaries come back */
const ANS_X = 9.55;
subs.forEach(a => {
  const dy = CY - a.cy;
  s.addShape(pres.ShapeType.line, {
    x: CARD_X + CARD_W, y: Math.min(CY, a.cy), w: ANS_X - (CARD_X + CARD_W), h: Math.abs(dy),
    flipV: dy < 0,
    line: { color: C.cyan, width: 2, endArrowType: 'triangle' },
  });
});

s.addShape(pres.ShapeType.roundRect, {
  x: ANS_X, y: CY - 0.625, w: 2.93, h: 1.25, rectRadius: 0.08,
  fill: { color: C.cardMain }, line: { color: C.orange, width: 1.5 },
});
s.addText('メインAIが1つの答えに', {
  x: ANS_X, y: CY - 0.55, w: 2.93, h: 0.30, margin: 0,
  fontFace: JP, fontSize: 14, bold: true, color: C.paper, align: 'center',
});
s.addText('受け取るのは数行の要約だけ', {
  x: ANS_X, y: CY - 0.20, w: 2.93, h: 0.24, margin: 0,
  fontFace: JP, fontSize: 10, color: C.orangeS, align: 'center',
});
s.addText('読んだ資料そのものは戻らない', {
  x: ANS_X, y: CY + 0.14, w: 2.93, h: 0.24, margin: 0,
  fontFace: JP, fontSize: 9, color: C.muted, align: 'center',
});
s.addText('→ あなたへ返答', {
  x: 9.25, y: 4.66, w: 3.53, h: 0.25, margin: 0,
  fontFace: JP, fontSize: 10, bold: true, color: C.orangeS, align: 'center', valign: 'middle',
});

/* --------------------------------------------------------------- caption */
s.addText('会議で部長が3人の担当に仕事を振り、上がってきた報告だけをまとめる——サブエージェントの動きは、それと同じです。', {
  x: 0.55, y: 5.18, w: 12.23, h: 0.28, margin: 0,
  fontFace: JP, fontSize: 10.5, color: C.muted, valign: 'middle',
});

/* ------------------------------------------------------------- takeaways */
const points = [
  { n: '01', t: '机が分かれる',   b: 'サブが読んだ資料も試行錯誤も、メインAIの記憶には入らない。話が散らからない。' },
  { n: '02', t: '同時に進む',     b: '調べる・作る・点検するが並行して走る。順番待ちが消えて、全体が速くなる。' },
  { n: '03', t: '戻るのは結論だけ', b: '1万字読んでも返すのは数行。だから長い作業でもメインAIが息切れしない。' },
];
points.forEach((p, i) => {
  const x = 0.55 + i * 4.14;
  s.addShape(pres.ShapeType.roundRect, {
    x, y: 5.62, w: 3.95, h: 1.00, rectRadius: 0.06,
    fill: { color: '18325B' }, line: { color: C.zoneLn, width: 1 },
  });
  s.addText([
    { text: p.n, options: { fontFace: UI, fontSize: 10, color: C.orange, bold: true } },
    { text: '   ' + p.t, options: { fontFace: JP, fontSize: 13, color: C.paper, bold: true } },
  ], { x: x + 0.22, y: 5.74, w: 3.55, h: 0.26, margin: 0, valign: 'middle' });
  s.addText(p.b, {
    x: x + 0.22, y: 6.02, w: 3.55, h: 0.48, margin: 0,
    fontFace: JP, fontSize: 9.5, color: C.muted, lineSpacingMultiple: 1.25,
  });
});

/* ---------------------------------------------------------------- footer */
s.addText('AI実践講座 ／ サブエージェント', {
  x: 0.55, y: 6.82, w: 6, h: 0.22, margin: 0,
  fontFace: JP, fontSize: 9, color: C.faint,
});
s.addText('SUB-AGENT · 01', {
  x: 6.78, y: 6.82, w: 6.0, h: 0.22, margin: 0,
  fontFace: UI, fontSize: 9, charSpacing: 2, color: C.faint, align: 'right',
});

s.addNotes([
  'サブエージェント＝本体のAIが、目的別の「部下AI」に仕事を切り出して同時に働かせ、結論だけを受け取る仕組み。',
  '',
  '01 相談を受ける：利用者が話す相手はいつもメインAI（司令塔）1体だけ。頼み方はいつもどおりでよい。',
  '02 仕事を分けて同時に走らせる：メインAIが依頼を分解し、調べ役・作る役・見直し役へ渡す。各サブエージェントは自分専用の作業机（独立した文脈）で作業し、そのメモはメインに持ち込まれない。3体が並行して動くので待ち時間が短い。',
  '03 要約だけ受け取る：戻ってくるのは結論の要約だけ。読んだ資料そのものは戻らないので、メインAIの手元が散らからず、長い作業でも息切れしない。',
].join('\n'));

pres.writeFile({ fileName: process.argv[2] || 'subagent-slide.pptx' })
  .then(f => console.log('written:', f));
