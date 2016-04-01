library(readr) #if not installed: install.packages('readr')
library(magrittr) #if not installed; install.packages('magrittr')
library(dplyr) #if not installed; install.packages('dplyr')

dataFiles = c("2008.csv","00-08.csv","95-08.csv")

types = c("i", "i", "i", "i", "i", "i",
  "i", "i", "c", "i", "c", "i",
  "i", "i", "i", "i", "c", "c",
  "i", "i", "i", "i", "c", "i",
  "i", "i", "i", "i", "i"
) %>% paste(collapse='')

for(i in dataFiles){
  #First extract all numeric columns for which a correlation makes sense
  tmp = readr::read_csv(i,col_types = types) %>%
    dplyr::select(which(strsplit(types,"")[[1]] == "i")) %>%
    dplyr::select(-Year)
  #Calculate correlation matrix with pairwise deletion
  try({
    timing_wide = system.time({correls_wide = cor(tmp,use="na.or.complete")})
    write.csv(correls_wide,paste0("Correlations/",strsplit(i,"\\.")[[1]][1]," wide correls R.txt"))
    })

  #reduce the number of columns
  tmp %<>% select(ActualElapsedTime, CRSElapsedTime, AirTime, Distance)
  #Calculate correlation matrix with pairwise deletion
  try({
    timing_narrow = system.time({correls_narrow = cor(tmp,use="na.or.complete")})
    write.csv(correls_narrow,paste0("Correlations/",strsplit(i,"\\.")[[1]][1]," narrow correls R.txt"))
  })

  #clean up
  readr::write_csv(dplyr::data_frame(File=i,Tool="R",NarrowTime=timing_narrow[3],WideTime=timing_wide[3],Technique="correlation"),
                   "performance measures.txt",
                   append=T)
  rm(tmp,correls_wide,correls_narrow)
}