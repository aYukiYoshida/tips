# F-test

## XspecのF-test
例えば  
モデル1: `phabs*powerlaw`  
モデル2: `phabs*powerlaw+gaussian`  
に対してモデル2中の `gaussian` の有意性のF検定をする。

**`Xspec`のF-testにおける帰無仮説** : 「加えた成分(`gaussian`)の係数が0である。」  
この仮説のためにはモデル1とモデル2が nest の関係になければいけない。
例えばモデル2が`phabs*powerlaw*gabs`だと
`gabs`の係数を0にするには`powerlaw`もいじることになる。これは nest ではないのでダメ。

### Reference

* Orlandini et al., 2012, ApJ, 748, 86
* Iwakiri et al., 2012, ApJ, 751, 35
* Jaisawal et al., 2013, ApJ, 779, 54
* Bevington, P. R. 1969, Data Reduction and Error Analysis for the Physical Sciences (New York: McGraw-Hill)
* Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. 2007, Numerical Recipes: The Art of Scientific Computing (Cambridge: Cambridge Univ. Press) 
https://www.hs.uni-hamburg.de/DE/Ins/Per/Czesla/PyA/PyA/pyaslDoc/aslDoc/statTest.html