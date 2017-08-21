### AGP Figure 2G,H Point plot (conjugated) linoleic acid 
### Author Chris Callewaert
### Date May 15, 2017

### Load packages
library(gdata)
library(psych)
library(corrplot)
library(ggplot2)
install.packages("extrafont")
library(extrafont)

### Read in data:
CLA_LA <- read.csv("CLA_LA_processed_normalized_for_Justine.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)
CLA_LA_melt <- read.csv("CLA_LA_processed_normalized_for_Justine_melt.txt", header=TRUE, sep="\t", stringsAsFactors=FALSE)

### Point plot:
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
