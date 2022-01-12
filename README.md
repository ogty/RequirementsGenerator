<h1 align="center">Requirements.txt Generator</h1>

<div align="center">

 [![Download Now](https://img.shields.io/badge/-Download%20Now!-%2322A6F2)](https://github.com/ogty/RequirementsGenerator/releases/download/v1.0.5/RequirementsGenerator.zip)
 ![release](https://img.shields.io/github/v/release/ogty/RequirementsGenerator?style=social)
 ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ogty/RequirementsGenerator?style=social)
 
</div>

![sample](./static/demo.gif)

***

### 対応言語

 - Python
 - Python-ipynb
 - Julia
 - Julia-ipynb
 - Go

***

### 機能

 - [x] Windows・Mac・Linux対応
 - [x] 言語選択
 - [x] フォルダ検索
 - [x] 詳細表示
 - [x] ライブラリ選択 
 - [ ] コマンド実行

***

### `config.json`

`static/config.json`ファイルの`ignores`に非表示にしたいディレクトリ名を追記すると、
そのディレクトリ名を含むパスが表示されなくなります。
また、パスを格納している`tree.json`の容量が小さくなります。

### 注意

デスクトップに大量のフォルダがある場合は正常に動作しない場合があります。