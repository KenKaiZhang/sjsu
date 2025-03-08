# ISE 201 Zybook

### 2.1

**mean** : the arithmetic average of the observations in a dataset

$$\bar{x} = (\frac{1}{n})\sum_{i=1}^{n}x_i$$

**variance** : measure of variability of dataset

$$s^2 = (1\frac{1}{n-1})\sum_{i=1}^{n}(x_i - \bar{x})^2$$

**standard deviation** : positive square root of the standard deviation

**degrees of freedom** : number of independent comparisons that can be made among the elements of a sample

**sample/population range** : difference between the max and min observations in a dataset

$$r = max(x_i) - min(x_1)$$

### 2.2

**stem-and-leaf diagram** : method of displaying data where:

- stem : range of data values
- leaf : last digit

**median** : value that divides the data into two equal halves

**quartiles (Q1, Q2, Q3)** : partitions the data into four equal partitions

**percentiles** : set of values that divide the sample into 100 equal partitions

**Interquartile Range (IQR)** : difference between the 3rd and 1st quartiles

$$IQR = Q_3 - Q_1$$

### 2.3

**frequency distribution** : arrangement of the frequencies of observations according to the values that the observations take observations

| class | 70 ≤ x ≤ 90 | 90 ≤ x 110 | 110 ≤ x ≤ 130 |
|-|-|-|-|
| frequency | 2 | 3 | 6 |
| relative frequency | 0.0250 | 0.0375 | 0.0750 |
| cumulative relative frequency | 0.0250 | 0.0625 | 0.1375 |

- **bin** : interval ranges
- in a histogram, each bin is a bar
- reasonable number of bins = $\sqrt{n}$

**relative frequency distribution** : the proportion of times the event occured ina series of trials of a random experiment

$$\frac{ObservedFrequencyPerBin}{TotalObservations}$$

**pareto chart** : bar chart used to rank the causes of a problem

**cumulative frequency plot** : heigth of each bar is the total nmber of observations less than or equal to the upper limit of the bin

**histograms** : visual display of frequency distribution

- **unimodal** : one mode that stands out
- **bimodal** : two modes that stands out
- **multimodal** : multiple modes that stand out
- **skewed left** : peak at right, tail at left (mode > median)
- **skewed right** : peak at left, tail at right (mode < median)

**z-score** : number of standard deviations an observed data point is from the mean

$$\frac{ObservedData - Mean}{StandardDeviation}$$


### 2.4

**box-plot** : graphical display of data where: 

- the box contains the middle 50% of the data (IQR)
- dividing middle line (median)
- whiskers that extend to the smallest & largest values (limits)

### 2.5

**time series/sequence** : data set in which the observations are recorded in the order they occurred

stem-and-leaf + time series plot = **digidot plot**

### 2.6

**scatter plot** : diagram displaying observations on two variables x and y where each observation is represented by a point

**matrix of scatter diagrams** : basically multiple scatter plots displayed at once

**sample correlation coefficient / Pearson correlation coefficient** : quantitative measure of strength of the linear relationship between two random variables

$$r_{xy} = \frac{\sum_{i=1}^{n}(y_i - \bar{y})(x_i - \bar{x})}{\sqrt{\sum_{i=1}^{n}(y_i - \bar{y})^2\sum_{i=1}^{n}(x_i - \bar{x})^2}}$$

- $r_{xy} = 1$ : perfectly linearly related with a positive slope
- $r_{xy} = -1$ : perfectly linearly relative with a negative slope
- $r_{xy} = 0$ : no linear relationship


### 2.7

**probability plot** : graphical method for determining whether a sample data conforms to the hypothesized distribution based on subjective visual examination of the data

**normal probability plot** : scale the y such that the normal cumulative distribution is a straight line

- plot the standardized normal scores $z_{(j)}$ against $x_{(j)}$ where the standardized normal scores satisfy

$$\frac{j-0.5}{n} = P(Z ≤ z_j) = \phi(z_j)$$
