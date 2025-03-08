# Linear Algebra

**vector** : an arrow in arrow inside a coordinate system with tail at the ORIGIN

- a pair of numbers describing how to get from the ORIGIN to a location in space

$$
\mathbf{v} = 
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}
$$

**adding vectors** : 

1. move the second vector so its tail sits at the tip of the first one
2. draw a new vector from tail of first to tip of second vector

$$
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} + 
\begin{bmatrix} y_1 \\ y_2 \\ y_3 \end{bmatrix} = 
\begin{bmatrix} x_1 + y1 \\ x_2 + y_2 \\ x_3 + y_3 \end{bmatrix}
$$

**multiplying vectors (scalar multiplication)** : scaling a vector with a number (**scalar**)

$$ n * \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} x_1 * n \\ x_2 * n \\ x_3 * n \end{bmatrix}$$

Each coordinate in a vector $\mathbf{v}$ should be seen as scalar that stretches/squishes a unit vector

- $\hat{i}$ : unit vector in the x direction
- $\hat{j}$ : unit vector in the y direction
- together they are the **basis vectors**

... so $\mathbf{v} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$ = $(x_1)\hat{i} + (y_1)\hat{j}$ = the sum of 2 scaled vectors

**linear combination** : when vectors are multiplied by scalars and then added together

$$a(\overrightarrow{v}) + b(\overrightarrow{w})$$

**span** : the set of all linear combinations of 2 vectors 

- what are all the possible vectors reachable only using addition and multiplication

**linear dependent** : when a vector already in the span of the others

$$\overrightarrow{u} = a(\overrightarrow{v}) + b(\overrightarrow{w})$$

... the inverse is **linearly independent**

**linear transformation/function** : keeping lines parallel and evenly spaced

- all lines remain lines without getting curved
- ORIGIN stays in place

by knowing the changes to $\hat{i}$ and $\hat{j}$, we can deduce the linear transformation to $\overrightarrow{v}$

if $\overrightarrow{v} = a(\hat{i}) + b(\hat{j})$ then $Transformed\,\overrightarrow{v} = a(Transformed\,\hat{i}) + b(Transformed\,\hat{j})$

$$
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = x_1
\begin{bmatrix} \hat{i}_1 \\ \hat{i}_2 \end{bmatrix} + x_2
\begin{bmatrix} \hat{j}_1 \\ \hat{j}_2 \end{bmatrix} = 
\begin{bmatrix} x_1\hat{i_1} + x_2\hat{j_1} \\ x_1\hat{i_2} + x_2\hat{j_2} \end{bmatrix}
$$

basically linear transformation can be found by knowing where $\hat{i}$ and $\hat{j}$ lands

**matrix multiplication** : applying multiple transformations to a vector

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}  
\begin{bmatrix} e & f \\ g & h \end{bmatrix}  
=
\begin{bmatrix} ae + bg & af + bh \\ ce + dg & cf + dh \end{bmatrix}
$$

... order matters in matrix multiplication

Example of multiplying two 3D matrices
$$
\mathbf{a}\mathbf{b} =
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}  
\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} 
$$
$$=
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix} 
\begin{bmatrix} a \\ d \\ g \end{bmatrix} +
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix} 
\begin{bmatrix} b \\ e \\ h \end{bmatrix} +
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix} 
\begin{bmatrix} c \\ f \\ i \end{bmatrix} 
$$
$$=
\begin{bmatrix} 
(1a + 2d + 3g) & (1b + 2e + 3h) & (1c + 2f + 3i) \\ 
(4a + 5d + 6g) & (4b + 5e + 6h) & (4c + 5f + 6i) \\ 
(7a + 8d + 9g) & (7b + 8e + 9h) & (7c + 8f + 9i) 
\end{bmatrix}
$$

**determinant** : factor by which a linear transformation changes any area/volume

negative determinant indicates a flip/inversion in space

$$det(\begin{bmatrix} a & b \\ c & d \end{bmatrix}) = ad - bc$$

- $a$ how much $\hat{i}$ is stretched/squished in the $x$
- $d$ how much $\hat{j}$ is stretched/squished in the $y$
- $b$ and $c$ how much the area is stretched/squished in the diagonal

... for 3D matrix :

$$
det(\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}) = 
a(ei - fh) - b(di - fg) + c(dh - eg)
$$
  
**dot product** : an indication of how much one vector aligns with another

- $a \cdot b > 0$ : vectors point in roughly the same direction
- $a \cdot b = 0$ : vectors are perpendicular
- $a \cdot b > 0$ : vectors point in roughly the opposite direction

$$
\begin{bmatrix} 
a \\ 
b \\ 
c
\end{bmatrix}
\cdot
\begin{bmatrix} 
d \\ 
e \\ 
f
\end{bmatrix}
= ad + be + cf
$$

**cross product** : finding a vector $\overrightarrow{p}$ that is perpendicular to two vectors $\overrightarrow{v}$ and $\overrightarrow{w}$

- order matters (determines orientation)
    - $> 0$ : $\overrightarrow{v}$ is on the right of $\overrightarrow{w}$
    - $< 0$ : $\overrightarrow{v}$ is on the left of $\overrightarrow{w}$

$$
\overrightarrow{p} = 
\overrightarrow{v} \times 
\overrightarrow{w}
$$
$$ 
=
\begin{bmatrix} v_x \\ v_y \\ v_z \end{bmatrix}
\times
\begin{bmatrix} w_x \\ w_y \\ w_z \end{bmatrix}
$$
$$
= 
det(
    \begin{bmatrix}
    \hat{i} & \hat{j} & \hat{k} \\
    v_x & v_y & v_z \\
    w_x & w_y & w_z 
    \end{bmatrix}
)
$$
$$
=
(v_y w_z - v_z w_y) \hat{i} -
(v_x w_z - v_z w_x) \hat{j} +
(v_x w_y - v_y w_x) \hat{k}
$$
$$
=
((v_y w_z - v_z w_y), -(v_x w_z - v_z w_x), (v_x w_y - v_y w_x))
$$

**Cramer's Rule** : formula to find the solution of a system of linear equations

Consider a system of \( n \) linear equations with \( n \) unknowns.

$$
\begin{aligned}
a_{11}x_1 + a_{12}x_2 + \dots + a_{1n}x_n &= b_1 \\
a_{21}x_1 + a_{22}x_2 + \dots + a_{2n}x_n &= b_2 \\
\vdots \\
a_{n1}x_1 + a_{n2}x_2 + \dots + a_{nn}x_n &= b_n
\end{aligned}
$$

This system can be written in matrix form as

$$
A \mathbf{x} = \mathbf{b}
$$

... where

$A$ is the **coefficient matrix** :

$$
A =
\begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\
a_{21} & a_{22} & \dots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & \dots & a_{nn}
\end{bmatrix}
$$

$ \mathbf{x} $ is the **unknowns vector** :

$$
\mathbf{x} =
\begin{bmatrix}
x_1 \\
x_2 \\
\vdots \\
x_n
\end{bmatrix}
$$

$\mathbf{b}$ is the **constant terms vector** :

$$
\mathbf{b} =
\begin{bmatrix}
b_1 \\
b_2 \\
\vdots \\
b_n
\end{bmatrix}
$$

... then the unqiue solution for each variable $x_i$ is given by 

$$x_i = \frac{det(A_i)}{det(A)}$$

... where

$det(A)$ is the determinant of the original coefficient matrix

$det(A_i) is the determinant of matrix formed by replacing the $i^{th}$ column of $A$ with $b$

**change of basis** : expressing a vector/linear transformation in terms of a new basis

If you have vector $v$ expressed in basis $B$ and want to express it in basis $C$, you can use a change of basis matrix $P$ that satisfies

$$[v]_C = P^{-1}[v]_B$$

... where

- $[v]_B$ : $v$ in original basis
- $[v]_C$ : $v$ in new basis
- $P$ : matrix whose columns are the new basis vectors expressed in the old basis

For transforming matrix $A$ from basis $B$ to $C$

$$[A]_C = P^{-1}AP$$

**eigenvectors** : vectors whose spans are unaffected by a transformation

**eigenvalues** : value eigenvectors are stretched/squished during a transformation

In terms of 3D space, it will be the **axis of rotation**

