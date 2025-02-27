# Definition
**随机森林**是由多个决策树组成的模型。
- Essential idea in bagging is to **average many noisy but approximately unbiased models**, hence reduce the variance.

- Trees are ideal candidates for bagging, since they can capture complex interaction.

>**Algorithm:Random Forest for Regression or Classification**
>1. For $n=1,...,N$:
(a)Draw a bootstrap sample $\mathbf{Z^*}$of size $N$ from the training set $\mathbb{T}$.
(b)Grow a random-forest tree $T_n$ to the bootstrapped data, for each terminal node of the tree, repeat the following steps until the minimum node size $n_{min}$ is reached.
>+ i.Select $m$ variables randomly from the $p$ variables.
>+ ii. Pick the best variable/split-point among them.
>+ iii. Split the node into two daughter nodes.
>2. Output the ensemble of trees $\{T_n(x)\},n\in [1,N]$
To make a prediction at a new point $x$:
Regression:
$$
\hat{f}_{N}(x) = \frac{1}{N}\sum\limits_{n=1}^{N}T_n(x)
$$
Classification:
Let $\hat{C}_n(x)$ be the class prediction of the $b$-th random-forest tree. Then $\hat{C}_{N}(x)=majority\ vote{\{\hat{C}_n(x)\},n=1,...,N}$

# Exercise
## Exercise 1
> Let $\{X_n\}$ be $N$ identically distributed r.v. with
$$
\mathbf{Var}[X_i]=\sigma^2,\quad i\in [1,N]\\
$$
and $\rho = \mathbf{Corr}[X_i,X_j]>0,\quad i\ne j$
Prove that $\mathbf{Var}[\bar{X}]=\rho\sigma^2+\frac{1-\rho}{N}\sigma^2$.

Proof:
$$
\begin{align}
\mathbf{Var}\left[\frac{1}{N}\sum\limits_{k=1}^{N}X_i\right]
&=\frac{1}{N^2}\left(\sum\limits_{k=1}^{N}\mathbf{Var}\left[X_i\right]+\sum\limits_{i\ne j}\mathbf{Cov}[X_i,X_j]\right)\\
&=\frac{\sigma^2}{N}+\frac{1}{N^2}\sum\limits_{i\ne j}\rho\sigma^2\\
&=\frac{\sigma^2}{N}+\frac{(N-1)\rho\sigma^2}{N}\\
&=\sigma^2\left(\frac{1}{N}+\frac{(N-1)\rho}{N}\right)\\
&=\sigma^2\left(\rho+\frac{1-\rho}{N}\right)
\end{align}
$$


- Q:Why will the formula be failed if $\rho<0$?
- A:.
---
- The size of the correlation of pairs of bagged trees limits the benefits of averaging.
$\mathbf{Var}[\bar{X}]\to \sigma^2\rho\quad (N\to \infty)$
**随机森林算法**通过在不改变$\sigma^2$的情况下减小 $|\rho|$以达到$\mathbf{Var}[\bar{X}]$减小的效果。
---
随机森林不仅对样本进行**有放回抽样**，还在每个节点分裂时随机选择一部分predictors（通常为$\sqrt{p}$）,这种随机性使得每棵树在训练过程中使用不同的特征子集，从而减少了树之间的相似性。

# Propositions
- Tree可以捕捉数据中复杂的交互结构
- Tree非常noisy，所以平均很好
- Bagging过程中生成的Tree是identically distributed，
- 
- 通过对数据进行多次随机采样和特征选择，生成多个决策树，并通过投票或平均的方式来做出最终预测。
- **易于实现和理解**：由于其基础是决策树，随机森林的原理相对简单。
- **抗过拟合能力强**：通过集成多个树，随机森林能有效地降低过拟合的风险。
- **鲁棒性好**：对数据中的噪声和异常值不敏感。
- **可并行化**：各个决策树可以并行训练，计算效率较高。
# 主要步骤
1. 从原始数据集中有放回地抽样，生成多个子样本集（Bootstrap）。
2. 对每个子样本集训练一棵决策树。在决策树的每个节点分裂时，随机选择部分特征进行最佳分裂（这与传统决策树不同，传统决策树会使用所有特征进行最佳分裂）。
3. 集成所有树的预测结果，对于分类任务，使用多数投票法；对于回归任务，取平均值。
