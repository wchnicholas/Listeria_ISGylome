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

plot_pie <- function(filename, graphname, class){
  t <- read_tsv(filename)
  setDT(t)
  t <- melt(t,id='TaxClass') %>%
         mutate(TaxClass=factor(TaxClass,levels=c('Species without ISG15','Species with ISG15')))
  p <-  ggplot(filter(t,TaxClass==class),aes(x="",y=value,fill=variable)) + 
	  geom_bar(width = 1, stat = "identity", color='black') +
	  coord_polar("y", start=0) + 
	  scale_fill_manual(values=c("blue", "white"))
  ggsave(graphname, p, height=5, width=5)
  }

plot_pie('Tree/Count_Lys_Q9JLN9_2066.tsv', 'graph/Pie_yesLys_Q9JLN9_2066.png','Species with ISG15')
plot_pie('Tree/Count_Lys_Q9JLN9_2066.tsv', 'graph/Pie_noLys_Q9JLN9_2066.png','Species without ISG15')
plot_pie('Tree/Count_Lys_Q80W47_198.tsv', 'graph/Pie_yesLys_Q80W47_198.png','Species with ISG15')
plot_pie('Tree/Count_Lys_Q80W47_198.tsv', 'graph/Pie_noLys_Q80W47_198.png','Species without ISG15')
plot_pie('Tree/Count_Lys_A2AH22_175.tsv', 'graph/Pie_yesLys_A2AH22_175.png','Species with ISG15')
plot_pie('Tree/Count_Lys_A2AH22_175.tsv', 'graph/Pie_noLys_A2AH22_175.png','Species without ISG15')
