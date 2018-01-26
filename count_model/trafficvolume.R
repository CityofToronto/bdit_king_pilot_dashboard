library(RPostgreSQL)
library(arm)
library(lme4)
library(gnm)
################################
# IMPORT FROM POSTGRESQL
################################


drv <- dbDriver("PostgreSQL")
source("C:\\Users\\alouis2\\Documents\\R\\connect\\connect.R")
filepath = "C:\\Users\\alouis2\\Documents\\final.sql"
strSQL = readLines(filepath, encoding = "UTF-8")
data <- dbGetQuery(con, strSQL)
data$day <- as.POSIXlt(data$dt)$wday
data$day <- factor(data$day)
data$intersection_uid <- factor(data$intersection_uid)
View(data)



# Grand Mean Model 

grandmean = lm(data$totaladjusted_vol ~ 1)
summary(grandmean)
(anova(grandmean))


# Intersection 
for (i in length(data$intersection_uid)){data$intersection_uid[i]= toString(data$intersection_uid[i])} 
intermodel = lm(totaladjusted_vol ~ intersection_uid, data = data)
summary(intermodel)


# Leg 
legmodel = lm(totaladjusted_vol ~ factor(leg), data = data)
summary(legmodel)

# Direction
dirmodel = lm(totaladjusted_vol ~ factor(dir), data = data)
summary(dirmodel)

# Day
par(mfrow = c(1,4))
boxplot(data$totaladjusted_vol ~ data$intersection_uid)
boxplot(data$totaladjusted_vol ~ data$leg)
boxplot(data$totaladjusted_vol ~ data$dir)
boxplot(data$totaladjusted_vol ~ data$day)
daymodel = lm(totaladjusted_vol ~ factor(day), data = data)
summary(daymodel)

#glm
glm = glm(totaladjusted_vol ~ intersection_uid*leg*dir*day, data = data)
glm1 = glm(totaladjusted_vol ~ dir, data = data)
glm2 = glm(totaladjusted_vol ~ intersection_uid + factor(day)+ leg*dir, data = data)
glm3 = glm(totaladjusted_vol ~ intersection_uid + day + leg + dir + intersection_uid:day:leg:dir)

par(mfrow = c(1,1))
plot(glm, which = 1)
plot(glm1, which = 1)
plot(glm2, which = 1)
plot(glm3, which = 1)
plot(glm4, which = 1)
anova(glm, glm1, glm2, glm3, glm4)

library(gnm)

#mixed
ml = gnm(totaladjusted_vol ~ Mult(factor(intersection_uid), leg), data = data)
ml1 = lmer(totaladjusted_vol ~ dir:leg + (1|intersection_uid):day, data = data)






ml2 = lmer(totaladjusted_vol ~ (1|leg)+(1|dir)+ (1|intersection_uid), data = data)
ml3 = lmer(totaladjusted_vol ~ (leg|dir) + (1|intersection_uid), data = data)
par(mfrow = c(1,1))
plot(fitted(ml), residuals(ml), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(ml), residuals(ml)))
plot(fitted(ml1), residuals(ml1), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(ml1), residuals(ml1)))
plot(fitted(ml2), residuals(ml2), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(ml2), residuals(ml2)))
plot(fitted(ml3), residuals(ml3), xlab = "Fitted Values", ylab = "Residuals") 
abline(h = 0, lty = 2)
lines(lowess(fitted(ml3), residuals(ml3)))
anova(ml1, ml2, ml3, test = 'F')




#
ml1 = lmer(log(totaladjusted_vol) ~ log(dir:leg + day + (1|intersection_uid)), data = data)
summary(ml1)
AIC(ml1)
plot(fitted(ml1), residuals(ml1), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(ml1), residuals(ml1)))


#
ml2 = glm(totaladjusted_vol ~ intersection_uid, data = data)
summary(ml2)
AIC(ml2)
plot(fitted(ml2), residuals(ml2), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(ml2), residuals(ml2)))


# best model so far
ml3 = lmer(totaladjusted_vol ~ dir:leg + factor(day) + (1|intersection_uid), data = data)
summary(ml3)
AIC(ml3)
plot(fitted(ml3), residuals(ml3), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(ml3), residuals(ml3)))


#

data2 <- dbGetQuery(con, strSQL)
data2$day <- as.POSIXlt(data2$dt)$wday
data2$totaladjusted_vol <- log(data2$totaladjusted_vol)
data2$intersection_uid <- log((data$intersection_uid))  
#data2$totaladjusted_vol <- log(data2$totaladjusted_vol)
data2$leg[data2$leg == 'N'] <- 1
data2$leg[data2$leg == 'S'] <- 2
data2$leg[data2$leg == 'E'] <- 3
data2$leg[data2$leg == 'W'] <- 4
data2$dir[data2$dir == 'NB'] <- 1
data2$dir[data2$dir == 'SB'] <- 2
data2$dir[data2$dir == 'EB'] <- 3
data2$dir[data2$dir == 'WB'] <- 4
data2$dir <- as.numeric(data2$dir)
data2$leg <- as.numeric(data2$leg)
View(data2)

logl = glm(totaladjusted_vol ~ log(factor(day)) + log(log(leg+dir)) + log(factor(intersection_uid)), data = data2)
plot(logl, which = 1)
logl
summary(logl)

log2 = glm(totaladjusted_vol ~ factor(log(day)) + factor(log(leg*dir)) + factor(log(intersection_uid)), data = data2)
plot(log2, which = 1)
log2
summary(log2)





##############
# multiplicative
#############

#gnmControl(tolerance = 1e-04, iterStart = 2, iterMax = 500, trace = FALSE)

mult1 = gnm(totaladjusted_vol ~ Mult(dir, factor(day)), data = data, iterMax = 5000)
summary(mult1)
plot(mult1, which = 1)


mult2 = gnm(totaladjusted_vol ~ Mult(intersection_uid, factor(day)), data = data, iterMax = 700)
summary(mult2)
plot(mult2, which = 1)


mult3 = gnm(totaladjusted_vol ~ Mult(factor(intersection_uid), factor(day)) + Mult(leg, dir), data = data)
summary(mult3)
plot(mult3, which = 1)

#######################################################################################

drv <- dbDriver("PostgreSQL")
source("C:\\Users\\alouis2\\Documents\\R\\connect\\connect.R")
filepath2 = "C:\\Users\\alouis2\\Documents\\bathurstonly.sql"
strSQL = readLines(filepath2, encoding = "UTF-8")
bathurst <- dbGetQuery(con, strSQL)
bathurst$day <- as.POSIXlt(bathurst$dt)$wday
bathurst$day <- factor(bathurst$day)
bathurst$intersection_uid <- factor(bathurst$intersection_uid)
View(bathurst)

b1 = gnm(totaladjusted_vol ~ Mult(intersection_uid, factor(day), leg, dir), data = bathurst, iterMax = 1000)
summary(b1)
plot(b1, which = 1)

b3 = gnm(totaladjusted_vol ~ Mult(intersection_uid, factor(day))^2 + (leg:dir), data = bathurst, iterMax = 1000)
summary(b3)
plot(b3, which = 1)






b2 = glm(totaladjusted_vol ~ intersection_uid + leg:day + factor(day) + factor(dt), data = bathurst)
summary(b2)
par(mfrow = c(1,1))
plot(fitted(b2), residuals(b2), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(b2), residuals(b2)))
plot(b2, which = 1)
  



##################################################################

# no leg or direction 

View(data)
nolegdir = aggregate(data$totaladjusted_vol, by = list(data$dt, data$intersection_uid, data$day), FUN = sum)
names(nolegdir)[1] <- "dt"
names(nolegdir)[2] <- "intersection_uid"
names(nolegdir)[3] <- "day"
names(nolegdir)[4] <- "vols"
View(nolegdir)


par(mfrow = (c(1,1)))

nld1 = glm(vols ~ factor(intersection_uid) + factor(dt) + factor(day), data = nolegdir)
summary(nld1)
plot(nld1, which = 1)

nld2 = lmer(vols ~ intersection_uid + (dt|day), data = nolegdir)
summary(nld2)
plot(fitted(nld2), residuals(nld2), xlab = "Fitted Values", ylab = "Residuals")
abline(h = 0, lty = 2)
lines(lowess(fitted(nld2), residuals(nld2)))

nld4 = gnm( vols ~ Mult(intersection_uid, day, dt), data = nolegdir)
summary(nld4)
plot(nld4, which = 1)


predict(nld4, data.frame(intersection_uid = 28, day = 5))


