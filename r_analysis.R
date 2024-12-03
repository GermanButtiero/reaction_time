setwd("~/course_Exper/Repo/reaction_time")
library(ggplot2)
D <- read.table("rt_data_with_computed_averages.csv", header=TRUE, sep=",", as.is=TRUE)
df <- D[, c("id", "group", "trial", "avg_incongruent")]


library(lme4)

# Fit the mixed-effects model
model <- lmer(avg_incongruent ~ trial * group + (1 | id), data = df)

# Summary of the model
summary(model)


library(gamm4)


df$trial <- as.factor(df$trial)
model_nonparametric <- gamm4(avg_incongruent ~ trial * group, 
                             random = ~(1 | id), 
                             data = df)
summary(model_nonparametric$mer)
