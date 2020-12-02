setwd('/Users/tunder/Dropbox/python/asymmetry/mapculture')
library(ggplot2)
library(plyr)
data <- read.csv('precocity_of_reviewed_fiction.tsv', sep = '\t')
data$prominence = as.factor(data$reviewstatus)
data$prominence = revalue(data$prominence, c('1' = 'reviewed', '0' = 'random'))
p <- ggplot(data, aes(x = age, y = precocity, 
                      color = prominence, group = prominence,
                      shape = prominence)) +
  geom_point(alpha = 0.85) + geom_smooth(method = 'lm', se = FALSE, fill = NA) +
  theme_bw() + scale_x_continuous("author age at publication") +
  ggtitle('Precocity as a function of\nauthor age and prominence') +
  scale_color_manual(values = c('black', 'skyblue3')) +
  scale_y_continuous('precocity as a z-score') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16, lineheight=1.1))

tiff("AgeVPrecocity.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)