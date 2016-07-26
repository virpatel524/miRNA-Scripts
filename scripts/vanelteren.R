# library("sanon")
# disnum <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_disnum", header=TRUE, sep=",")
# disnum["num"] <- scale(disnum["num"], center = FALSE, scale = max(disnum["num"]))

# alpha <- sanon(num  ~ grp(class) + strt(age), data = disnum)
# print(summary(alpha))


# expnum <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_expnum", header=TRUE, sep=",")
# expnum["num"] <- scale(expnum["num"], center = FALSE, scale = max(expnum["num"]))

# alpha <- sanon(num  ~ grp(class) + strt(age), data = expnum)
# print(summary(alpha))


# tarnum <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_tarnum", header=TRUE, sep=",")
# tarnum["num"] <- scale(tarnum["num"], center = FALSE, scale = max(tarnum["num"]))

# alpha <- sanon(num  ~ grp(class) + strt(age), data = tarnum)
# print(summary(alpha))





library("sanon")
disjac <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_disjac", header=TRUE, sep=",")

alpha <- sanon(jac  ~ grp(class) + strt(age), data = disjac)
print(summary(alpha))


expjac <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_expjac", header=TRUE, sep=",")

alpha <- sanon(jac  ~ grp(class) + strt(age), data = expjac)
print(summary(alpha))


tarjac <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_tarjac", header=TRUE, sep=",")

alpha <- sanon(num  ~ grp(class) + strt(age), data = tarjac)
print(summary(alpha))