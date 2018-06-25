library(ppclust)
library(factoextra)
library(cluster)
library(fclust)

df <- read.table("D:/Dados/cath/dompdb_tmscore_table/table_1c4zA02_RMSD_GDT-HA", 
                 header = FALSE)

x <- df[,c(1,2)]

x

res.fcm <- fcm(x, centers=2)

res.fcm$v0

summary(res.fcm)

res.fcm3 <- ppclust2(res.fcm, "fanny")

res.fcm2 <- ppclust2(res.fcm, "kmeans")
factoextra::fviz_cluster(res.fcm2, data = x, 
  ellipse.type = "convex",
  palette = "jco",
  repel = TRUE)

res.fcm4 <- ppclust2(res.fcm, "fclust")
idxsf <- SIL.F(res.fcm4$Xca, res.fcm4$U, alpha=1)
idxpe <- PE(res.fcm4$U)
idxpc <- PC(res.fcm4$U)
idxmpc <- MPC(res.fcm4$U)

cat("Fuzzy Silhouette Index: ", idxsf)