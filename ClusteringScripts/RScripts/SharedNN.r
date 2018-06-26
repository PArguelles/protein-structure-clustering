library("dbscan")

df <- read.table("D:/Dados/cath/dompdb_tmscore_table/table_1c4zA02_RMSD_GDT-HA", 
                 header = FALSE)

x <- df[,c(1,2)]

# Out of k = 20 NN 7 (eps) have to be shared to create a link in the sNN graph.
# A point needs a least 16 (minPts) links in the sNN graph to be a core point.
# Noise points have cluster id 0 and are shown in black.
cl <- sNNclust(x, k = 20, eps = 7, minPts = 16)
plot(x, col = cl$cluster + 1L, cex = .5)

res.fcm4 <- ppclust2(cl, "fclust")
idxsf <- SIL.F(res.fcm4$Xca, res.fcm4$U, alpha=1)
idxpe <- PE(res.fcm4$U)
idxpc <- PC(res.fcm4$U)
idxmpc <- MPC(res.fcm4$U)

cat("Fuzzy Silhouette Index: ", idxsf)