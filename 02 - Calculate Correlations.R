library(readr) #if not installed: install.packages('readr')
library(magrittr) #if not installed; install.packages('magrittr')
library(dplyr) #if not installed; install.packages('dplyr')

dataFiles = c("2008.csv","00-08.csv","95-08.csv")

for(i in dataFiles){
  #First extract all numeric columns for which a correlation makes sense
  tmp = readr::read_csv(i) %>% 
    dplyr::select(ActualElapsedTime, CRSElapsedTime, AirTime, ArrDelay, DepDelay,
                  Distance, TaxiIn, TaxiOut, CarrierDelay, WeatherDelay, NASDelay,
                  SecurityDelay, LateAircraftDelay)
  #Calculate correlation matrix with pairwise deletion
  timing_wide = system.time({correls_wide = cor(tmp,use="na.or.complete")})
  print(correls_wide)
  #reduce the number of columns
  
  tmp %<>% select(-contains("Delay"),-contains("Taxi"))
  #Calculate correlation matrix with pairwise deletion
  timing_narrow = system.time({correls_narrow = cor(tmp,use="na.or.complete")})
  print(correls_narrow)
  
  #clean up
  readr::write_csv(dplyr::data_frame(File=i,Tool="R",NarrowTime=timing_narrow[3],WideTime=timing_wide[3],Technique="correlation"),
                   "performance measures.txt",
                   append=T)
  rm(tmp,correls_wide,correls_narrow)
}