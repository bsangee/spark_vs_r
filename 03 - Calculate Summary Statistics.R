library(readr) #if not installed: install.packages('readr')
library(magrittr) #if not installed; install.packages('magrittr')
library(dplyr) #if not installed; install.packages('dplyr')

dataFiles = c("2008.csv","00-08.csv","95-08.csv")

#Function to calculate desired summary statistics
newSummary = function(x){
  c(Mean = mean(x,na.rm=T),Variance = var(x,na.rm=T),NonZero = sum(x > 0,na.rm=T),Max = max(x,na.rm=T),Min = min(x,na.rm=T))
}

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
  #Calculate summary statistics
  try({
    timing_wide = system.time({summary_wide = vapply(tmp,newSummary,c(Mean=1,Variance=1,NonZero=1,Max=1,Min=1))})
    write.csv(summary_wide,paste0("Basic-Statistics/",strsplit(i,"\\.")[[1]][1]," wide summary R.txt"))
  })

  #reduce the number of columns
  tmp %<>% select(ActualElapsedTime, CRSElapsedTime, AirTime, Distance)
  #Calculate summary statistics
  try({
    timing_narrow = system.time({summary_narrow = vapply(tmp,newSummary,c(Mean=1,Variance=1,NonZero=1,Max=1,Min=1))})
    write.csv(summary_narrow,paste0("Basic-Statistics/",strsplit(i,"\\.")[[1]][1]," narrow summary R.txt"))
  })

  #clean up
  readr::write_csv(dplyr::data_frame(File=i,Tool="R",NarrowTime=timing_narrow[3],WideTime=timing_wide[3],Technique="summary"),
    "performance measures.txt",
    append=T)
  rm(tmp,summary_wide,summary_narrow)
}