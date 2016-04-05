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
  set.seed(1000) # reproducibility
  #First extract all for which a regression makes sense
  #Don't want to include:
  ## Diverted because something can't be cancled AND diverted
  ## TailNum and FlightNum because these are often single occurences
  ## Origin/Dest because there would be too many levels for it to be meaningful in logistic regression
  ## Delays because they're mostly missing values
  ## The remaining because they're nearly always missing when cancelled
  tmp = readr::read_csv(i,col_types = types) %>%
    dplyr::select(-Year,-CancellationCode,-Diverted,-TailNum,-FlightNum,-Origin,-Dest,
                  -CarrierDelay,-WeatherDelay,-NASDelay,-SecurityDelay,-LateAircraftDelay,
                  -DepDelay,-TaxiOut,-TaxiIn,-DepTime,-ArrTime,-ActualElapsedTime,-AirTime,ArrDelay,DepDelay) %>%
    dplyr::mutate(UniqueCarrier = as.factor(UniqueCarrier),
                  Month = as.factor(Month),
                  DayOfWeek = as.factor(DayOfWeek),
                  DayofMonth = as.factor(DayofMonth))

  #Calculate summary statistics
  try({
    trainRows = base::sample(1:nrow(tmp),ceiling(nrow(tmp)*.7))
    tmp = tmp[trainRows,]
    timing_wide = system.time({
      wide_model = glm(Cancelled~.,family = binomial(link = "logit"),data = tmp)
    })
    write.csv(summary(wide_model)$coefficients,paste0("Logistic-Regression/",strsplit(i,"\\.")[[1]][1]," wide logistic R.txt"))
    #dput(wide_model,paste0("Logistic-Regression/",strsplit(i,"\\.")[[1]][1]," wide logistic R.dput"))
    rm(wide_model)
  })

  #reduce the number of columns
  tmp %<>% select(-Month,-DayofMonth,-DayOfWeek,-UniqueCarrier)
  #Calculate summary statistics
  try({
    timing_narrow = system.time({
      narrow_model = glm(Cancelled~.,family = binomial(link = "logit"),data = tmp)
    })
    write.csv(summary(narrow_model)$coefficients,paste0("Logistic-Regression/",strsplit(i,"\\.")[[1]][1]," narrow logistic R.txt"))
    #dput(narrow_model,paste0("Logistic-Regression/",strsplit(i,"\\.")[[1]][1]," narrow logistic R.dput"))
    rm(narrow_model)
  })

  #clean up
  try({
    readr::write_csv(dplyr::data_frame(File=i,Tool="R",NarrowTime=timing_narrow[3],WideTime=timing_wide[3],Technique="logistic"), "performance measures.txt", append=T)
    rm(tmp)
    rm(timing_narrow,timing_wide)
    gc()
  })
}