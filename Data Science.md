# Classification
## Boosting
### AdaBoost.M1
A classifier $G(X)$ produces a prediction taking value from $\{1,-1\}$
Error Rate : $$\overline{err}=\frac{1}{N}\sum \limits_{ i =1 }^{N}I(y_{i}\ne G(x_{i})) $$
#### Steps
1. Creat modified versions of data
2. Produce a sequence of weak classifiers $G_{m}(x),m=1,2,\dots,M$\
3. Combine them to get final classifier: $G(x)=sign\Big(\sum\limits_{ m=1}^{M} \alpha_{m}G_{m}(x)\Big)$
#### AdaBoost.M1 Algorithm
1. Initialize the observation weights $w_{i}=\frac{1}{N},i=1,\dots,N$
2. For $i=1,...,M$:
		1. (a)Fit $G_{m}(x)$ to the traning data using weights $w_{i}$.
		2. (b)Compute $$\overline{err}_{m}=\frac{\sum \limits_{ i =1 }^{N}w_{i}I(y_{i}\ne G_{m}(x_{i}))}{\sum \limits_{ i =1 }^{N}w_{i} }$$
		3. (c)Compute $$\alpha_{m}=\log\left( \frac{1-err_{m}}{err_{m}} \right)$$
		4. (d)Set $w_{i}\cdot\exp\{\alpha_{m}I(y_{i}\ne G_{m} (x_{i}))\},i=1,\dots,N$ to $w_{i}$
		5. (e)$G(x)=sign\{ \sum \limits_{m=1}^{M}{\alpha_{m}G_{m}(x)}\}$
$$\frac{\sum \limits_{ i =1 }^{N}w_{i}I(y_{i}\ne G(x_{i}))}{\sum \limits_{ i =1 }^{N}w_{i} }\cdot\frac{\sum \limits_{ i =1 }^{N}w_{i}\exp\{\alpha_{m}I(y_{i}\ne G_{m} (x_{i}))\}}{\sum \limits_{ i =1 }^{N}w_{i} I(y_{i}\ne G(x_{i}))\exp\{\alpha_{m}I(y_{i}\ne G_{m} (x_{i}))\}}$$
## Gradient Boosting
Loss function $L(x)=\sum \limits_{i=1}^{N}L(y_{i},f(x_{i}))$
Minimizing from getting $$\mathbf{\hat{f}}= \mathop{\mathrm{argmin}}\limits_{\mathbf{f}} \ L(\mathbf{f})$$

## Comp
Kaggle，天池
京东智汇平台，DataFountain，DataCastle，科赛网，创新工场AIChallenger等  
腾讯，滴滴出行，第四范式，中国平安，融360，中国农业银行等  
SIGKDD，ICDM，CIKM，IJCAI等

- LLM发挥实力的阈值时2kw



