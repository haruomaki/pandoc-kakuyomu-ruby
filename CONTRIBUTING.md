# デバッグ方法

```sh
pandoc --to=FORMAT --filter=/path/to/ruby_kenten xxx.md
```
というコマンドは以下のコマンドと等価です。

```sh
pandoc --to=json xxx.md | python /path/to/ruby_kenten.py FORMAT | pandoc --from=json --to=FORMAT
```

これを利用すると、（例えば変換先をhtmlとして）挙動を調べたいときは次のようなコマンドを実行することで、フィルタによる変換後のAST(json表現)を確認することができます。

またpythonからの標準/エラー出力もありますから、printデバッグなども可能です。

```sh
pandoc --to=json xxx.md | python /path/to/ruby_kenten.py html
```

ここで`python /path/to/ruby_kenten.py`のコマンドラインオプションとして`html`を付けるのが肝です。上のコマンドではフィルタがpandocと完全に独立しているため、フィルタに変換先のフォーマットを別途教えてあげているのです。

こうすると、`toJSONFilter`へ渡す関数（このプロジェクトでは`ruby_kenten`関数）の引数`fmt`に「html」が入ってくれます。
