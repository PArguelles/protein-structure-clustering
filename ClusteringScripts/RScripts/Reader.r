library(ppclust)
library(factoextra)
library(cluster)
library(fclust)

df <- read.table("D:/Dados/cath/dompdb_tmscore_table/table_test", 
                 header = FALSE)

df <- setNames(data.frame(as.list(1:3)), LETTERS[1:3])

df[,c("A","B")]

res.fcm <- fcm(df, centers=3)