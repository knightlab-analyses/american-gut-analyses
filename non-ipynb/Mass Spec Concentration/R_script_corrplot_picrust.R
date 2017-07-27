### AGP metagenome prediction Picrust analysis & point plot (conjugated) linoleic acid 
### Author Chris Callewaert
### Date May 15, 2017

### Load packages
library(gdata)
library(psych)
library(corrplot)
library(ggplot2)
install.packages("extrafont")
library(extrafont)

### Read in data
MetagenomeL2 <- read.csv("MetagenomeL2_AGP_V3.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
MetagenomeL2b <- MetagenomeL2[,-1]
MetagenomeL2b <- MetagenomeL2b[-c(7713, 7714, 7715), ]
ImpBact <- read.csv("Important_bact_families_AGP_V2.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
ImpBactb <- ImpBact[,-1]
ImpBactL6 <- read.csv("Important_bact_families_AGP_L6_V1.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
ImpBactL6b <- ImpBactL6[,-1]
MetagenomeL3 <- read.csv("MetagenomeL3_AGP_V1.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
MetagenomeL3b <- MetagenomeL3[,-1]
MetagenomeL3c <- read.csv("MetagenomeL3_AGP_V2.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
MetagenomeL3d <- MetagenomeL3c[,-1]
ImpBactL6c <- read.csv("Important_bact_families_AGP_L6_V2.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
ImpBactL6d <- ImpBactL6c[,-1]

### Read in data for scatterplot Justine
CLA_LA <- read.csv("CLA_LA_processed_normalized_for_Justine.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
CLA_LA_melt <- read.csv("CLA_LA_processed_normalized_for_Justine_melt.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)

### Make corrplot
res1 <- cor(ImpBactb, MetagenomeL2b, use = "complete.obs")
png(height=2900, width=2500, pointsize=40, file="Corrplot1c.png")
corrplot(res1, method="color", tl.col = "black")
dev.off()

res2 <- cor(ImpBactb, MetagenomeL3b, use = "complete.obs")
png(height=1530, width=3250, pointsize=22, file="Corrplot2b.png")
corrplot(res2, method="square", tl.col = "black")
dev.off()

res3 <- cor(ImpBactL6b, MetagenomeL2b, use = "complete.obs")
png(height=2900, width=2500, pointsize=40, file="Corrplot3a.png")
corrplot(res3, method="color", tl.col = "black")
dev.off()

res4 <- cor(ImpBactL6d, MetagenomeL3d, use = "complete.obs")
png(height=1530, width=3250, pointsize=22, file="Corrplot5c.png")
corrplot(res4, method="color", tl.col = "black")
dev.off()

### Point plot Justine
pdf(file = "Plot_Justine_V1d.pdf", width = 10, height = 7, family = "Helvetica", useDingbats=FALSE)
ggplot(CLA_LA_melt, aes(x = Label, y = Value, color = Label)) + 
  geom_point(position = position_jitter(width = 0.3)) + 
  theme_bw() + theme(panel.grid = element_blank()) + 
  ylab("LA CLA") +
  facet_grid (. ~ LA.CLA) 
dev.off()

pdf(file = "Plot_Justine_V1b.pdf", width = 7, height = 7, family = "Helvetica", useDingbats=FALSE)
ggplot(CLA_LA_melt, aes(x = Label, y = Value, color = Label)) + 
  geom_point(position = position_jitter(width = 0.2), aes(shape = factor(Label))) + 
  scale_shape(solid = FALSE) +
  theme_bw() + theme(panel.grid = element_blank()) + 
  ylab("LA CLA") +
  facet_grid (. ~ LA.CLA) 
dev.off()

pdf(file = "Plot_Justine_V2.pdf", width = 7, height = 7, family = "Helvetica")
ggplot(CLA_LA_melt, aes(x = Label, y = Value, color = Label)) + 
  geom_point(position = position_jitter(width = 0.2), shape = 21, size = 2, stroke = 1) + 
  theme_bw() + theme(panel.grid = element_blank()) + 
  ylab("LA CLA") +
  facet_grid (. ~ LA.CLA) 
dev.off()

p <- ggplot(CLA_LA_melt, aes(x = Label, y = Value, color = Label)) + 
  geom_point(position = position_jitter(width = 0.3), shape = 21, size = 2, stroke = 1) + 
  theme_bw() + theme(panel.grid = element_blank()) + 
  ylab("LA CLA") +
  facet_grid (. ~ LA.CLA)
ggsave(plot=p,height=7,width=10,dpi=200, filename="Plot_Justine_V3b.pdf", useDingbats=FALSE)
