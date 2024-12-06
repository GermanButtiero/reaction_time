library(lme4)
# library(lmerTest)
library(ggplot2)
library(glue)
library(dplyr)



#* Reading the data
df <- read.table("expanded_rt_incon_accurate.csv", header=TRUE, sep=",", as.is=TRUE)
df$group  <- as.factor(df$group)
df$trial  <- as.factor(df$trial)
df$log_rt <- log(df$rt)

remove_large_vals <- function(data, column) {
  data[data[[column]] < 2.5, ]
}

create_comparison_boxplot <- function(data_pre, data_post, value_col, pre_name, post_name) {
  data_pre$filter_status <- pre_name
  data_post$filter_status <- post_name
  combined_data <- rbind(data_pre, data_post)
  combined_data$filter_status <- factor(combined_data$filter_status, levels = c(pre_name, post_name))
  #* boxplot
  ggplot(combined_data, aes(x = filter_status, y = combined_data[[value_col]], fill = filter_status)) +
    geom_boxplot(alpha = 0.7) +
    labs(
      title = glue::glue("Comparison of {pre_name} and {post_name}"),
      x = "Filter Status",
      y = value_col
    ) +
    theme_minimal() +
    theme(legend.position = "none")
}

#* QQ Nomality check for the log transform reaction times for each pairwise groups

df_exer_tr1_pre <- subset(df, group == "exercise" & trial == 1)
df_exer_tr1 <- remove_large_vals(df_exer_tr1_pre, "rt")
create_comparison_boxplot(df_exer_tr1_pre, df_exer_tr1, "rt", "exer tr1 - Unfiltered", "df_exer_tr1 - Filtered")
qqnorm(df_exer_tr1$log_rt, main= "QQplot for log transformed exercise tr1")
qqline(df_exer_tr1$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_exer_tr1$log_rt)$p.value, 7)))

df_exer_tr2_pre <- subset(df, group == "exercise" & trial == 2)
df_exer_tr2 <- remove_large_vals(df_exer_tr2_pre, "rt")
create_comparison_boxplot(df_exer_tr2_pre, df_exer_tr2, "rt", "exer tr2 - Unfiltered", "df_exer_tr2 - Filtered")
qqnorm(df_exer_tr2$log_rt, main= "QQplot for log transformed exercise tr2")
qqline(df_exer_tr2$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_exer_tr2$log_rt)$p.value, 7)))

df_cont_tr1_pre <- subset(df, group == "control" & trial == 1)
df_cont_tr1 <- remove_large_vals(df_cont_tr1_pre, "rt")
create_comparison_boxplot(df_cont_tr1_pre, df_cont_tr1, "rt", "cont tr1 - Unfiltered", "df_cont_tr1 - Filtered")
qqnorm(df_cont_tr1$log_rt, main= "QQplot for log transformed control tr1")
qqline(df_cont_tr1$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_cont_tr1$log_rt)$p.value, 7)))

df_cont_tr2_pre <- subset(df, group == "control" & trial == 2)
df_cont_tr2 <- remove_large_vals(df_cont_tr2_pre, "rt")
create_comparison_boxplot(df_cont_tr2_pre, df_cont_tr2, "rt", "cont tr2 - Unfiltered", "df_cont_tr2 - Filtered")
qqnorm(df_cont_tr2$log_rt, main= "QQplot for log transformed control tr2")
qqline(df_cont_tr2$log_rt, col="red")
legend("topleft", legend = paste("p-val =", round(shapiro.test(df_cont_tr2$log_rt)$p.value, 7)))

#-------------------------------------------------------------------------------
#* Linear mixed model - unaveraged data
df_exer_tr1$label <- "exercise_tr1"
df_exer_tr2$label <- "exercise_tr2"
df_cont_tr1$label <- "control_tr1"
df_cont_tr2$label <- "control_tr2"
cleared_df <- rbind(df_exer_tr1, df_exer_tr2, df_cont_tr1, df_cont_tr2)

# library(lmerTest)
model_lmm <- lmer(log_rt ~ trial * group + (1 | id), data=cleared_df)
summary(model_lmm)
origScale_fixed_ef <- exp(fixef(model_lmm))
origScale_fixed_ef


ggplot(cleared_df, aes(x = trial, y = log_rt, color = as.factor(id))) +
  geom_point() +
  geom_line(aes(y = predict(model_lmm), group = id), linetype = "dashed") +
  theme_minimal()

cleared_df$predicted <- predict(model_lmm)

# Plot the data
ggplot(cleared_df, aes(x = trial, y = log_rt, color = group)) +
  geom_point(alpha = 0.6) +  # Observed data points
  geom_line(aes(y = predicted, group = id), linetype = "dashed", alpha = 0.7) +  # Individual fits
  stat_smooth(method = "lm", aes(group = group), se = FALSE, size = 1.2) +  # Group-level trends
  labs(
    title = "Reaction Time Across Trials by Group",
    x = "Trial",
    y = "Log Reaction Time"
  ) +
  theme_minimal() +
  theme(legend.position = "top")



#* LMM Resudual analysis
plot(fitted(model_lmm), residuals(model_lmm),
     xlab="Fitted Values", ylab="Residuals",
     main="Residuals vs. Fitted Values")
abline(h=0, col="red")

ggplot(data.frame(residuals = residuals(model_lmm), fitted = fitted(model_lmm), 
                  group = cleared_df$group, trial = cleared_df$trial), 
       aes(x = fitted, y = residuals)) +
  geom_point(alpha = 0.5) +
  facet_grid(trial ~ group) +
  geom_hline(yintercept = 0, color = "red") +
  labs(title = "Residuals vs. Fitted Values by Group and Trial")


boxplot(residuals(model_lmm) ~ interaction(df$group, df$trial),
        xlab="Group and Trial", ylab="Residuals",
        main="Residuals by Group and Trial")

qqnorm(residuals(model_lmm), main= "LLM residuals - QQ plot")
qqline(residuals(model_lmm), col = "red")
legend("topleft", legend = paste("p-val =", shapiro.test(residuals(model_lmm))$p.value))
#_______________________________________________________________________________

#*------------------------------------------------------------------------------

model_lmm_randTr <- lmer(log_rt ~ trial * group + (trial | id), data=cleared_df)
summary(model_lmm_randTr)
origScale_fixed_ef <- exp(fixef(model_lmm_randTr))
origScale_fixed_ef


ggplot(cleared_df, aes(x = trial, y = log_rt, color = as.factor(id))) +
  geom_point() +
  geom_line(aes(y = predict(model_lmm_randTr), group = id), linetype = "dashed") +
  theme_minimal()

cleared_df$predicted <- predict(model_lmm_randTr)


ggplot(cleared_df, aes(x = trial, y = log_rt, color = group)) +
  geom_point(alpha = 0.6) +  
  geom_line(aes(y = predicted, group = id), linetype = "dashed", alpha = 0.7) 
  stat_smooth(method = "lm", aes(group = group), se = FALSE, size = 1.2) +  
  labs(
    title = "Reaction Time Across Trials by Group",
    x = "Trial",
    y = "Log Reaction Time"
  ) +
  theme_minimal() +
  theme(legend.position = "top")



#* LMM Resudual analysis
plot(fitted(model_lmm_randTr), residuals(model_lmm_randTr),
     xlab="Fitted Values", ylab="Residuals",
     main="Residuals vs. Fitted Values")
abline(h=0, col="red")

ggplot(data.frame(residuals = residuals(model_lmm_randTr), fitted = fitted(model_lmm_randTr), 
                  group = cleared_df$group, trial = cleared_df$trial), 
       aes(x = fitted, y = residuals)) +
  geom_point(alpha = 0.5) +
  facet_grid(trial ~ group) +
  geom_hline(yintercept = 0, color = "red") +
  labs(title = "Residuals vs. Fitted Values by Group and Trial")


boxplot(residuals(model_lmm_randTr) ~ interaction(df$group, df$trial),
        xlab="Group and Trial", ylab="Residuals",
        main="Residuals by Group and Trial")

qqnorm(residuals(model_lmm_randTr), main= "LLM residuals - QQ plot")
qqline(residuals(model_lmm_randTr), col = "red")
legend("topleft", legend = paste("p-val =", shapiro.test(residuals(model_lmm_randTr))$p.value))


anova(model_lmm, model_lmm_randTr)



#* Generalized mixed linear model
model_glmm <- glmer(rt ~ trial * group + (1 | id), data = cleared_df, family = Gamma(link = "log"))
    
summary(model_glmm)
    # Summary of the model
origScale_fixed_ef <- exp(fixef(model_glmm))




































# df_exer_tr1_clean$label <- "exercise_tr1"
# df_exer_tr2_clean$label <- "exercise_tr2"
# df_cont_tr1_clean$label <- "control_tr1"
# df_cont_tr2_clean$label <- "control_tr2"
# 
# combined_cleaned_df <- rbind(df_exer_tr1_clean, df_exer_tr2_clean, df_cont_tr1_clean, df_cont_tr2_clean)
# 
# boxplot(rt ~ label, data = cleared_df,
#         main = "Reaction Times by Group and Trial (Without Outliers)",
#         xlab = "Group and Trial",
#         ylab = "Reaction Time",
#         col = c("lightblue", "lightgreen", "pink", "lightyellow"))
# 
# df_exer_tr1$label <- "exercise_tr1"
# df_exer_tr2$label <- "exercise_tr2"
# df_cont_tr1$label <- "control_tr1"
# df_cont_tr2$label <- "control_tr2"
# 
# combined_df <- rbind(df_exer_tr1, df_exer_tr2, df_cont_tr1, df_cont_tr2)
# 
# 
# boxplot(rt ~ label, data = combined_df,
#         main = "Reaction Times by Group and Trial",
#         xlab = "Group and Trial",
#         ylab = "Reaction Time",
#         col = c("lightblue", "lightgreen", "pink", "lightyellow"))

