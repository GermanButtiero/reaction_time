library(lme4)
library(ggplot2)
library(glue)

setwd("~/course_Exper/Repo/reaction_time")

#* Reading the data
df <- read.table("expanded_rt_incon_accurate.csv", header=TRUE, sep=",", as.is=TRUE)
df$group  <- as.factor(df$group)
df$trial  <- as.factor(df$trial)
df$log_rt <- log(df$rt)

remove_outliers <- function(data, column) {
  Q1 <- quantile(data[[column]], 0.25, na.rm = TRUE) # First quartile
  Q3 <- quantile(data[[column]], 0.75, na.rm = TRUE) # Third quartile
  IQR <- Q3 - Q1 # Interquartile range
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  
  # Filter data within the IQR
  data[data[[column]] >= lower_bound & data[[column]] <= upper_bound, ]
}


#* QQ Nomality check for the log transform reaction times for each pairwise groups

df_exer_tr1 <- subset(df, group == "exercise" & trial == 1)
df_exer_tr1 <- remove_outliers(df_exer_tr1, "rt")
qqnorm(df_exer_tr1$log_rt, main= "QQplot for log transformed exercise tr1")
qqline(df_exer_tr1$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_exer_tr1$log_rt)$p.value, 7)))

df_exer_tr2 <- subset(df, group == "exercise" & trial == 2)
df_exer_tr2 <- remove_outliers(df_exer_tr2, "rt")
qqnorm(df_exer_tr2$log_rt, main= "QQplot for log transformed exercise tr2")
qqline(df_exer_tr2$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_exer_tr2$log_rt)$p.value, 7)))

df_cont_tr1 <- subset(df, group == "control" & trial == 1)
df_cont_tr1 <- remove_outliers(df_cont_tr1, "rt")
qqnorm(df_cont_tr1$log_rt, main= "QQplot for log transformed control tr1")
qqline(df_cont_tr1$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_cont_tr1$log_rt)$p.value, 7)))

df_cont_tr2 <- subset(df, group == "control" & trial == 2)
df_cont_tr2 <- remove_outliers(df_cont_tr2, "rt")
qqnorm(df_cont_tr2$log_rt, main= "QQplot for log transformed control tr2")
qqline(df_cont_tr2$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_cont_tr2$log_rt)$p.value, 7)))

#* Fitting the data to the linear mixed model
model_lmm <- lmer(log_rt ~ trial * group + (1 | id), data=df)

plot(fitted(model_lmm), residuals(model_lmm),
     xlab="Fitted Values", ylab="Residuals",
     main="Residuals vs. Fitted Values")
abline(h=0, col="red")


ggplot(data.frame(residuals = residuals(model_lmm), fitted = fitted(model_lmm), 
                  group = df$group, trial = df$trial), 
       aes(x = fitted, y = residuals)) +
  geom_point(alpha = 0.5) +
  facet_grid(trial ~ group) +
  geom_hline(yintercept = 0, color = "red") +
  labs(title = "Residuals vs. Fitted Values by Group and Trial")


boxplot(residuals(model_lmm) ~ interaction(df$group, df$trial),
        xlab="Group and Trial", ylab="Residuals",
        main="Residuals by Group and Trial")

qqnorm(residuals(model_lmm), main= "QQ plot for the residuals of the model")
qqline(residuals(model_lmm), col = "red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(residuals(model_lmm))$p.value, 7)))


#* Fit glmm
model_glmm <- glmer(rt ~ trial * group + (1 | id), data = df, family = Gamma(link = "log"))
    
summary(model_glmm)
    # Summary of the model
fixed_ef <- exp(fixef(model_glmm))













#####################




































df_exer_tr1 <- subset(df, group == "exercise" & trial == 1)
df_exer_tr2 <- subset(df, group == "exercise" & trial == 2)
df_cont_tr1 <- subset(df, group == "control" & trial == 1)
df_cont_tr2 <- subset(df, group == "control" & trial == 2)

hist(subset(df_exer_tr1)$rt)
hist(subset(df_exer_tr2)$rt)
hist(subset(df_cont_tr1)$rt)
hist(subset(df_cont_tr2)$rt)

remove_outliers <- function(data, column) {
  Q1 <- quantile(data[[column]], 0.25, na.rm = TRUE)
  Q3 <- quantile(data[[column]], 0.75, na.rm = TRUE)
  IQR <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  
  data[data[[column]] >= lower_bound & data[[column]] <= upper_bound, ]
}

df_exer_tr1_clean <- remove_outliers(df_exer_tr1, "rt")
df_exer_tr2_clean <- remove_outliers(df_exer_tr2, "rt")
df_cont_tr1_clean <- remove_outliers(df_cont_tr1, "rt")
df_cont_tr2_clean <- remove_outliers(df_cont_tr2, "rt")

df_exer_tr1_clean$label <- "exercise_tr1"
df_exer_tr2_clean$label <- "exercise_tr2"
df_cont_tr1_clean$label <- "control_tr1"
df_cont_tr2_clean$label <- "control_tr2"

combined_cleaned_df <- rbind(df_exer_tr1_clean, df_exer_tr2_clean, df_cont_tr1_clean, df_cont_tr2_clean)

boxplot(rt ~ label, data = combined_cleaned_df,
        main = "Reaction Times by Group and Trial (Without Outliers)",
        xlab = "Group and Trial",
        ylab = "Reaction Time",
        col = c("lightblue", "lightgreen", "pink", "lightyellow"))

df_exer_tr1$label <- "exercise_tr1"
df_exer_tr2$label <- "exercise_tr2"
df_cont_tr1$label <- "control_tr1"
df_cont_tr2$label <- "control_tr2"

combined_df <- rbind(df_exer_tr1, df_exer_tr2, df_cont_tr1, df_cont_tr2)


boxplot(rt ~ label, data = combined_df,
        main = "Reaction Times by Group and Trial",
        xlab = "Group and Trial",
        ylab = "Reaction Time",
        col = c("lightblue", "lightgreen", "pink", "lightyellow"))

