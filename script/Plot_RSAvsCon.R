#R code
library(ggplot2)
library(scales)
library(RColorBrewer)
library(readr)
library(tidyr)
library(reshape)
library(stringr)
library(dplyr)
library(ggrepel)
library(gridExtra)
library(data.table)
require(cowplot)

t <- read_tsv('result/ISG15_sites_cluster1and2.tsv') %>%
       mutate(RSA_mean=RSA_mean*100) %>%
       mutate(RSA_sd=RSA_sd*100) %>%
       mutate(Lys_Conservation=Lys_Conservation*100)
textsize <- 7
p  <- ggplot(t, aes(Lys_Conservation, RSA_mean)) + 
        geom_point(size=0.5) + 
        geom_errorbar(aes(ymin=RSA_mean-RSA_sd, ymax=RSA_mean+RSA_sd), width=0) +
        xlab(expression(bold("Sequence conservation (%)"))) +
	ylab(expression(bold("Relative Solvent Accessibility (%)"))) +
	theme(plot.title=element_blank(),
	      axis.title=element_text(size=textsize,face="bold"),
	      axis.text=element_text(size=textsize,face="bold"),
	      axis.text.x=element_text(angle = 0, hjust=0.5, size=textsize, vjust=0.5,face="bold"),
	      legend.key.size=unit(0.08,'in'),
	      legend.title=element_blank(),
	      legend.text=element_text(size=textsize,face="bold"),
	      legend.position='none') 
ggsave('graph/RSA_vs_Con_Cluster1and2.png',p,height=2.5,width=2.5, dpi=300)
print (cor.test(t$Lys_Conservation, t$RSA_mean))
