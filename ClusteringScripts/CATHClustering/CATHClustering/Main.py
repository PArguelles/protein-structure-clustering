import AffinityPropScript as ap
import KMeansScript as km
import DBSCANScript as dbs

#aff = [ap.affinityProp()]
#kmeans = [km.kmeansFunc(2),km.kmeansFunc(4),km.kmeansFunc(6)]
#dbscan = [dbs.dbscanFunc()]

kmeans_limit = 10
i = 2
interval = 2
while i < kmeans_limit:
    km.kmeansFunc(i)
    i += interval

ap.affinityProp()