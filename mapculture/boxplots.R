# horizontal boxplot for Can We Map Culture
data = read.csv('/Users/tunder/Dropbox/python/asymmetry/mapculture/viz_for_effect_size.tsv', sep = '\t')
medians = data$middle
lower = data$bottom
upper = data$top

data = data.frame(ymin = lower, ymax = upper, med = medians, 
                  method = as.factor(c('kl', 'cos', 'kl', 'cos')),
                  test = as.factor(c('Bestsellers 1900-50\nKL divergence', 
                             'Bestsellers 1900-50\ncosine distance',
                             'Prominently reviewed\nKL divergence',
                             'Prominently reviewed\ncosine distance')))

data$test = factor(data$test, 
                     levels = c('Bestsellers 1900-50\nKL divergence', 
                                'Bestsellers 1900-50\ncosine distance',
                                'Prominently reviewed\nKL divergence',
                                'Prominently reviewed\ncosine distance'),
                     ordered = TRUE)

library(ggplot2)

p <- ggplot(data, aes(x = test, ymin = ymin, ymax = ymax, med = med, color = method)) +
  geom_errorbar(aes(x = test, ymin = ymin, ymax = ymax), width = 0.5, size = 1) + geom_point(aes(x= test, y = med), size=4, shape=21, fill="white") + 
  coord_flip() + scale_colour_manual(values = c('darkorchid2', 'darkseagreen4')) +
  scale_y_continuous(limits = c(0, 0.68)) +
  labs(y = "\neffect size (Cohen's d)", x = '') +
  theme(legend.position="none",
        text = element_text(size = 16, family = "Avenir Next Medium"))

tiff("/Users/tunder/Dropbox/python/asymmetry/mapculture/fig3boxplots.tiff", height = 3.8, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)