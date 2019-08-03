#R code
library(stringr)
library(phytools)

ISG15_classification <- function(label){
  label_split <- unlist(str_split(label,"||"))
  ISG15 <- label_split[length(label_split)-3]
  return (ISG15)
  }

Site_identification <- function(label){
  label_split <- unlist(str_split(label,"||"))
  site <- label_split[length(label_split)-6]
  return (site)
  }

ISG15_to_coloring <- function(ISG15){
  if (ISG15=='Y'){return ('red')}
  else {return ('grey')}
  }

Site_to_coloring <- function(site){
  if (site=='K'){return ('blue')}
  else {return ('white')}
  }

plot_tree <- function(filename, graphname){
  tree <- read.tree(filename)
  tree_rooted <- midpoint.root(tree)
  ISG15 <- mapply(ISG15_classification, tree_rooted$tip.label)
  site  <- mapply(Site_identification, tree_rooted$tip.label)
  color_ISG15 <- mapply(ISG15_to_coloring, ISG15)
  color_site  <- mapply(Site_to_coloring, site)
  tree_rooted$tip.label <- as.character(mapply(Site_identification, tree_rooted$tip.label))
  png(graphname,res=150,height=1600,width=600)
  plot(tree_rooted,show.tip.label=F,align.tip.label=F,label.offset=0.1,no.margin=T,font=0,lwd=1)
  tiplabels(pch = 22, bg = color_site, cex = 1, adj = 0.5)
  tiplabels(pch = 22, bg = color_ISG15, cex = 1, adj = 0.54)
  dev.off()
  }

plot_tree('Tree/Ortholog_Q9JLN9_2066.tree', 'graph/Tree_Q9JLN9_2066.png')
plot_tree('Tree/Ortholog_Q80W47_198.tree', 'graph/Tree_Q80W47_198.png')
plot_tree('Tree/Ortholog_A2AH22_175.tree', 'graph/Tree_A2AH22_175.png')
