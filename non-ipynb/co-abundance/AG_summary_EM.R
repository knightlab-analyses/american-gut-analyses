
#### load mapping file and otu table ####
m <- load.qiime.mapping.file('american_gut/1250/ag_map_with_alpha.txt') 
dim(m)
x <- load.qiime.otu.table('american_gut/1250/wf_taxa_summary/deblur_125nt_no_blooms_L6_R.txt')
dim(x)
m <- m[rownames(x),]
row.names(m) == row.names(x)
min.prevalence <- 0.1 
x <- x[,colMeans(x>0) > min.prevalence]
dim(x)

# only US 
m_US <- subset(m, m$country == 'USA')
x_US <-  x[rownames(m_US),]
dim(x_US)

# only UK 
m_UK <- subset(m, m$country == 'United Kingdom')
x_UK <-  x[rownames(m_UK),]
dim(x_UK)

#load library
library(propr)

#proportionaly on US samples
rho <- perb(x_US, ivar = 0)
rho_m <- as.matrix(rho@matrix)
colnames(rho_m) <- colnames(x_US)
rownames(rho_m) <- colnames(x_US)

perb <- NULL
for (i in 1:nrow(rho_m)) {
  for (j in 1:ncol(rho_m)) {
    perb <- rbind(correlation, c(rownames(rho_m)[i], rownames(rho_m)[j], rho_m[i,j]))
  }
}
colnames(perb) <- c('source', 'target', 'prop')
write.table(perb, 'prop_US.txt', row.names=FALSE, quote=FALSE, sep='\t')

#subset abs prop >0.3
perb <- read.table('prop_US.txt', header = T, sep = '\t')
perb_0.3 <- subset(perb, abs(prop)   > 0.3 )
perb_0.3 <- perb_0.3[with(perb_0.3, order(prop)), ]

# supress duplicates
perb_0.3 <- perb_0.3[!duplicated(t(apply(perb_0.3, 1, sort))),]
write.table(perb_0.3, 'prop_US_O.3.txt', row.names=FALSE, quote=FALSE, sep='\t')


### proportionaly on UK samples
rho <- perb(x_UK, ivar = 0)
rho_m <- as.matrix(rho@matrix)
colnames(rho_m) <- colnames(x_UK)
rownames(rho_m) <- colnames(x_UK)

perb <- NULL
for (i in 1:nrow(rho_m)) {
  for (j in 1:ncol(rho_m)) {
    perb <- rbind(correlation, c(rownames(rho_m)[i], rownames(rho_m)[j], rho_m[i,j]))
  }
}
colnames(perb) <- c('source', 'target', 'prop')
write.table(perb, 'prop_UK.txt', row.names=FALSE, quote=FALSE, sep='\t')

#subset abs prop >0.3
perb <- read.table('prop_UK.txt', header = T, sep = '\t')
perb_0.3 <- subset(perb, abs(prop)   > 0.3 )
perb_0.3 <- perb_0.3[with(perb_0.3, order(prop)), ]

# supress duplicates
perb_0.3_sup <- perb_0.3[!duplicated(t(apply(perb_0.3, 1, sort))),]
write.table(perb_0.3_sup, 'prop_UK_O.3.txt', row.names=FALSE, quote=FALSE, sep='\t')


