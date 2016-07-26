library("sanon")
disnum <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_disnum", header=TRUE, sep=",")
disnum["num"] <- scale(disnum["num"], center = FALSE, scale = max(disnum["num"]))

alpha <- sanon(num  ~ grp(class) + strt(age), data = disnum)
print(summary(alpha))


expnum <- read.table("/Users/virpatel/Desktop/pub_stuff/relevant_data/kruskal_data/mirstrat_disnum", header=TRUE, sep=",")
disnum["num"] <- scale(disnum["num"], center = FALSE, scale = max(disnum["num"]))

alpha <- sanon(num  ~ grp(class) + strt(age), data = disnum)
print(summary(alpha))