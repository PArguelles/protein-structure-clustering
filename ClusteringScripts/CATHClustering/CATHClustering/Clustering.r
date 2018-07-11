library(ppclust)
library(factoextra)
library(cluster)
library(fclust)
library(dbscan)

path_wo <- "D:/Dados/cath/clustering_results"
path_to_results <- "D:/Dados/cath/clustering_results/pdb"
path_to_tables <- "D:/Dados/cath/dompdb_tmscore_table/"

structures <- c('1c4zA02','1xfjA00','2asfA00','2evvA00','2vxzA01','3bfmA01','3bpkA01','3hisA02','4kp1A01')

for(str in structures){

	#_pdbid_#
	patt <- paste("_",str,sep="")
	patt <- paste(patt,"_",sep="")
	files <- list.files(path=path_to_tables, full.names=FALSE, pattern = patt)

	dir.create(file.path(path_wo, str), showWarnings = FALSE)

	for(name in files){

		#################################
		# SET VARIABLES
		#################################

		table_path <- paste(path_to_tables,name, sep="")

		div <- strsplit(name,"_")

		structure <- div[[1]][2]
		measure1 <- div[[1]][3]
		measure2 <- div[[1]][4]

		aux <- paste(structure,"/",sep="")
		current_path <- gsub("pdb",aux,path_to_results)

		path_to_summaries <- paste(current_path,structure,sep="")
		path_to_summaries <- paste(path_to_summaries,measure1,sep="_")
		path_to_summaries <- paste(path_to_summaries,measure2,sep="_")
		path_to_summaries <- paste(path_to_summaries,"algorithm",sep="_")

		path_to_plots <- paste(current_path,"plot",sep="")
		path_to_plots <- paste(path_to_plots,structure,sep="_")
		path_to_plots <- paste(path_to_plots,measure1,sep="_")
		path_to_plots <- paste(path_to_plots,measure2,sep="_")
		path_to_plots <- paste(path_to_plots,"algorithm",sep="_")
		path_to_plots <- paste(path_to_plots,".png",sep="")

		#################################
		# LOAD DATA
		#################################

		df <- read.table(table_path, header = FALSE)

		x <- df[,c(2,3)]

		names(x) <- c(measure1, measure2)

		#################################
		# FUZZY C-MEANS 
		#################################

		n_centers <- 2

		res.fcm <- fcm(x, centers=n_centers)
		res.fcm2 <- ppclust2(res.fcm, "kmeans")

		fcm_path <- paste("fcm",n_centers,sep="_")
		fcm_summary_path <- gsub("algorithm",fcm_path,path_to_summaries)
		fcm_plot_path <- gsub("algorithm",fcm_path,path_to_plots)
		
		#################################
		# SAVE RESULTS
		#################################

		plotcmeans <- factoextra::fviz_cluster(res.fcm2, data = x, ellipse.type = "convex", palette = "jco", labelsize = 0, repel = FALSE)
	
		png(filename=fcm_plot_path)
		plot(plotcmeans)
		dev.off()
		sink(fcm_summary_path)
		print(res.fcm)
		sink()

		#################################
		# SHARED NEAREST NEIGHBORS
		#################################

		k = 20
		eps = 7
		minPts = 16
		cl <- sNNclust(x, k = k, eps = eps, minPts = minPts)
		
		snn_path <- paste("snn",k,sep="_")
		snn_path <- paste(snn_path,eps,sep="_")
		snn_path <- paste(snn_path,minPts,sep="_")
		snn_summary_path <- gsub("algorithm",snn_path,path_to_summaries)
		snn_plot_path <- gsub("algorithm",snn_path,path_to_plots)

		#################################
		# SAVE RESULTS
		#################################

		sink(snn_summary_path)
		print(cl)
		sink()

		png(filename=snn_plot_path)
		plot(x, col = cl$cluster + 1L, cex = .9)
		dev.off()

	}
}

