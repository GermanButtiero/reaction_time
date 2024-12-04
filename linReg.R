setwd("~/course_Exper/Repo/reaction_time")
D <- read.table("rt_data_with_computed_averages.csv", header=TRUE, sep=",", as.is=TRUE)
df <- D[, c("id", "group", "trial", "avg_incongruent")]

#Converting group and trial in R factor variables
df$group <- as.factor(df$group)
df$trial <- as.factor(df$trial)

#Simple Linear Regression model
linReg_model <- lm(avg_incongruent ~ group + trial, data= df)
summary(linReg_model)

plot(df$group, df$avg_incongruent)


set.seed(100)
# Generate x
x <- runif(n = 20, min = -2, max = 4)
# Simulate y
beta0 <- 50; beta1 <- 200; sigma <- 90
y <- beta0 + beta1 * x + rnorm(n = length(x), mean = 0, sd = sigma)
# From here: like for the analysis of 'real data', we have data in x and y:
# Scatter plot of y against x
plot(x, y)
# Find the least squares estimates, use Theorem 5.4
(beta1hat <- sum( (y - mean(y))*(x-mean(x)) ) / sum( (x-mean(x))^2 ))
(bet0hat <- mean(y) - beta1hat*mean(x))
# Use lm() to find the estimates
lm(y ~ x)
# Plot the fitted line
abline(lm(y ~ x), col="red")

