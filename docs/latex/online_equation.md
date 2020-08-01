# LaTeX の数式をオンライン上の画像にする

## description
CODECOGSのサービス [Online LaTeX equation editor](https://www.codecogs.com/latex/eqneditor.php) を使う。

入力した数式のオンライン情での画像として生成し、`<img>`タグを取得することができる。

## example

以下の式の`<img>`タグを取得

**LaTeX式**   
```tex
\begin{aligned}
R_{\rm A} = 
3.7\times10^{8}\left(M_{\ast}/M_{\odot}\right)^{1/7} R_{6}^{10/7}B_{12}^{4/7}L_{ 37}^{-2/7}\ {\rm cm},
\label{eq:AlfvenRadius}
\end{aligned}
```

**取得した`<img>`タグ**  
```html
<img src="https://latex.codecogs.com/gif.latex?\begin{aligned}&space;R_{\rm&space;A}&space;&=&&space;3.7\times10^{8}\left(M_{\ast}/M_{\odot}\right)^{1/7}&space;R_{6}^{10/7}B_{12}^{4/7}L_{&space;37}^{-2/7}\&space;{\rm&space;cm},&space;\label{eq:AlfvenRadius}&space;\end{aligned}" title="\begin{aligned} R_{\rm A} &=& 3.7\times10^{8}\left(M_{\ast}/M_{\odot}\right)^{1/7} R_{6}^{10/7}B_{12}^{4/7}L_{ 37}^{-2/7}\ {\rm cm} \end{aligned}" />
```

**実際の画像**
<div align="center">
<img src="https://latex.codecogs.com/gif.latex?\begin{aligned}&space;R_{\rm&space;A}&space;&=&&space;3.7\times10^{8}\left(M_{\ast}/M_{\odot}\right)^{1/7}&space;R_{6}^{10/7}B_{12}^{4/7}L_{&space;37}^{-2/7}\&space;{\rm&space;cm},&space;\label{eq:AlfvenRadius}&space;\end{aligned}" title="\begin{aligned} R_{\rm A} &=& 3.7\times10^{8}\left(M_{\ast}/M_{\odot}\right)^{1/7} R_{6}^{10/7}B_{12}^{4/7}L_{ 37}^{-2/7}\ {\rm cm} \end{aligned}" />
</div>
