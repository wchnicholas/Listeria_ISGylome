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

clusterinfo <- read_tsv('data/clusterinfo.tsv')
cluster1_ID <- clusterinfo %>% filter(`C: Cluster`=='cluster 1') %>% .$`Razor Protein`
cluster2_ID <- clusterinfo %>% filter(`C: Cluster`=='cluster 2') %>% .$`Razor Protein`
ID_of_interest <- c(cluster1_ID, cluster2_ID)

#PLOT LYS CONSERVATION 
t <- read_tsv('result/ISG15_Lys_con.tsv') %>%
       filter(UniProt_ID %in% ID_of_interest)
textsize <- 7
p  <- ggplot(t, aes(Type, K)) +
        geom_violin() +
        geom_boxplot(width=.1, outlier.colour=NA) +
        xlab("Lys site") +
        ylab(expression(bold("Lys Conservation (%)"))) +
        theme(plot.title=element_blank(),
              axis.title=element_text(size=textsize,face="bold"),
              axis.text=element_text(size=textsize,face="bold"),
              axis.text.x=element_text(angle = 0, hjust=0.5, size=textsize, vjust=0.5,face="bold"),
              legend.key.size=unit(0.08,'in'),
              legend.title=element_blank(),
              legend.text=element_text(size=textsize,face="bold"),
              legend.position='none')
ggsave('graph/Compare_Lys_Con.png',p,height=2.5,width=2.5, dpi=300)
print (t.test(filter(t,Type=="ISG15")$K, filter(t,Type=="Other")$K))

#PLOT RSA
t <- read_tsv('result/ISG15_Lys_RSA_filtered.tsv') %>%
       filter(UniProt_ID %in% ID_of_interest)
textsize <- 7
p  <- ggplot(t, aes(Type, RSA)) +
        geom_violin() +
        geom_boxplot(width=.1, outlier.colour=NA) +
        xlab("Lys site") +
        ylab(expression(bold("RSA (A2)"))) +
        theme(plot.title=element_blank(),
              axis.title=element_text(size=textsize,face="bold"),
              axis.text=element_text(size=textsize,face="bold"),
              axis.text.x=element_text(angle = 0, hjust=0.5, size=textsize, vjust=0.5,face="bold"),
              legend.key.size=unit(0.08,'in'),
              legend.title=element_blank(),
              legend.text=element_text(size=textsize,face="bold"),
              legend.position='none')
ggsave('graph/Compare_RSA.png',p,height=2.5,width=2.5, dpi=300)
print (t.test(filter(t,Type=="ISG15")$RSA, filter(t,Type=="Other")$RSA))
