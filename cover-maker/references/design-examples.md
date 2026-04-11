# 封面设计代码示例

## 风格 A：大字冲击（黑白极简）

适用场景：认知类、干货类、观点类内容

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@900&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .cover {
      width: 1242px;
      height: 1660px;
      background: #000;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 80px;
      position: relative;
      overflow: hidden;
    }
    .tag {
      background: #fff;
      color: #000;
      font-family: 'Noto Sans SC', sans-serif;
      font-weight: 900;
      font-size: 36px;
      display: inline-block;
      padding: 8px 24px;
      margin-bottom: 48px;
      width: fit-content;
    }
    .main-title {
      font-family: 'Noto Sans SC', sans-serif;
      font-weight: 900;
      font-size: 160px;
      color: #fff;
      line-height: 1.05;
      letter-spacing: -4px;
    }
    .highlight {
      background: #fff;
      color: #000;
      padding: 0 12px;
    }
    .sub {
      font-family: 'Noto Sans SC', sans-serif;
      font-weight: 900;
      font-size: 48px;
      color: #666;
      margin-top: 60px;
      line-height: 1.4;
    }
    .line {
      position: absolute;
      bottom: 120px;
      left: 80px;
      right: 80px;
      height: 4px;
      background: #fff;
    }
    .footer {
      position: absolute;
      bottom: 60px;
      left: 80px;
      font-family: 'Noto Sans SC', sans-serif;
      font-weight: 900;
      font-size: 32px;
      color: #444;
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="tag">认知</div>
    <div class="main-title">
      涨粉越快<br>
      <span class="highlight">越不赚钱</span>
    </div>
    <div class="sub">流量质量 × 变现路径<br>才是关键</div>
    <div class="line"></div>
    <div class="footer">@你的账号名</div>
  </div>
</body>
</html>
```

---

## 风格 B：杂志感

适用场景：生活方式、职场、深度内容

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .cover {
      width: 1242px;
      height: 1660px;
      background: #F5F0E8;
      display: flex;
      flex-direction: column;
      padding: 100px 90px;
      position: relative;
    }
    .issue {
      font-family: 'Noto Sans SC', sans-serif;
      font-size: 28px;
      color: #999;
      letter-spacing: 8px;
      text-transform: uppercase;
      margin-bottom: 60px;
    }
    .divider {
      width: 100%;
      height: 2px;
      background: #1a1a1a;
      margin-bottom: 60px;
    }
    .main-title {
      font-family: 'Noto Serif SC', serif;
      font-weight: 900;
      font-size: 130px;
      color: #1a1a1a;
      line-height: 1.1;
      margin-bottom: 50px;
    }
    .thin-divider {
      width: 60px;
      height: 2px;
      background: #1a1a1a;
      margin-bottom: 40px;
    }
    .sub {
      font-family: 'Noto Sans SC', sans-serif;
      font-size: 40px;
      color: #444;
      line-height: 1.6;
    }
    .en-sub {
      position: absolute;
      bottom: 120px;
      left: 90px;
      font-family: 'Noto Sans SC', sans-serif;
      font-size: 28px;
      color: #bbb;
      letter-spacing: 4px;
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="issue">Vol. 01 · 2026</div>
    <div class="divider"></div>
    <div class="main-title">写字楼<br>选址的<br>真相</div>
    <div class="thin-divider"></div>
    <div class="sub">地段从来不是<br>最贵的成本</div>
    <div class="en-sub">THE TRUTH ABOUT OFFICE LOCATION</div>
  </div>
</body>
</html>
```

---

## 风格 C：色块撞色

适用场景：活动、课程、产品推广

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@900&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .cover {
      width: 1242px;
      height: 1660px;
      background: #FF3B30;
      position: relative;
      overflow: hidden;
    }
    .black-block {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 55%;
      background: #000;
    }
    .content {
      position: relative;
      z-index: 10;
      padding: 100px 80px;
    }
    .label {
      font-family: 'Noto Sans SC', sans-serif;
      font-weight: 900;
      font-size: 32px;
      color: #000;
      background: #FFD60A;
      display: inline-block;
      padding: 10px 28px;
      margin-bottom: 50px;
    }
    .main-title {
      font-family: 'Noto Sans SC', sans-serif;
      font-weight: 900;
      font-size: 150px;
      color: #fff;
      line-height: 1;
      letter-spacing: -6px;
    }
    .sub {
      position: absolute;
      bottom: 140px;
      left: 80px;
      right: 80px;
      font-family: 'Noto Sans SC', sans-serif;
      font-weight: 900;
      font-size: 52px;
      color: #fff;
      line-height: 1.4;
    }
    .sub span {
      color: #FFD60A;
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="black-block"></div>
    <div class="content">
      <div class="label">干货分享</div>
      <div class="main-title">3个<br>方法</div>
    </div>
    <div class="sub">让客户<span>主动</span>找你<br>而不是你追客户</div>
  </div>
</body>
</html>
```
