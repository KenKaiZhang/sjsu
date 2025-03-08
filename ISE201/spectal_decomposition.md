# [Spectral Decomposition](https://www.youtube.com/watch?v=mhy-ZKSARxI)

**diagonal matrix** : stretches

**orthogonal matrix** : rotates

**symmetric matrix** : a matrix with some form of symmetry along the diagonal

**rectangle matrix** : not symmetric

**transpose** : convert matrix $A$ to $A^T$ by turning the rows into columns

- symmetric matrix : $S = S^T$
- orthogonal matrix : $Q^T = Q^{-1}$
    - the transpose of an orthogonal matrix means rotation in the reverse direction

**matrix decomposition** : discovering the matrices that multiply together to form a matrix

formal definition of eigen

$$A \overrightarrow{v} = \lambda \overrightarrow{v}$$

... says that when the eigenvector $\overrightarrow{v}$ receives a linear transformation $A$, it is the same as the eigenvector $\overrightarrow{v}$ being scaled by an eigenvalue $\lambda$

**THEOREM**

Whenever you have a symmetric matrix you can always unconditionally decompose it into a sequence of three simple matrices

$$S = Q \Lambda Q^T$$

... where

- $S$ : symmetric matrix
- $Q$ : orthogonal matrix
- $\Lambda$ : diagonal matrix

... where the 

- columns of matrix $Q$ are the normalized eigenvectors of $S$
- diagonal values of matrix $\Lambda$ is the eigenvalues of the eigenvectors from left to right

$$
\begin{bmatrix} S \end{bmatrix} = 
\begin{bmatrix} | && | && | && | \\ e_1 && e_2 && ... && e_n \\ | && | && | && | \end{bmatrix}
\begin{bmatrix} \lambda_1 \\ && \lambda_2 \\ && && ... \\ && && && \lambda_n \\ \end{bmatrix}
\begin{bmatrix} | && | && | && | \\ e_1 && e_2 && ... && e_n \\ | && | && | && | \end{bmatrix}^T
$$