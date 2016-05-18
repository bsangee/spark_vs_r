library(readr) #if not installed: install.packages('readr')
library(magrittr) #if not installed; install.packages('magrittr')
library(dplyr) #if not installed; install.packages('dplyr')
library(rpart) #if not installed; install.packages('rpart')

dataFiles = c("2008.csv","00-08.csv","95-08.csv")

types = c("i", "i", "i", "i", "i", "i",
  "i", "i", "c", "i", "c", "i",
  "i", "i", "i", "i", "c", "c",
  "i", "i", "i", "i", "c", "i",
  "i", "i", "i", "i", "i"
) %>% paste(collapse='')

for(i in dataFiles){
  cat("Starting file",i,"\n")
  set.seed(1000) # reproducibility
  #First extract all for which a regression makes sense
  #Don't want to include:
  ## Cancelled and CancellationCode because they don't co-occur
  ## TailNum and FlightNum because these are often single occurences
  ## Origin/Dest because there would be too many levels for it to be meaningful in linear regression
  ## Diverted and TaxiOut because they generate singularities
  ## Delays because they're mostly missing values (>50%)
  tmp = readr::read_csv(i,col_types = types) %>%
    dplyr::select(-Year,-CancellationCode,-Cancelled,-TailNum,-FlightNum,-Origin,-Dest,-Diverted
                  -CarrierDelay,-WeatherDelay,-NASDelay,-SecurityDelay,-LateAircraftDelay) %>%
    dplyr::mutate(UniqueCarrier = as.factor(UniqueCarrier),
                  Month = as.factor(Month),
                  DayOfWeek = as.factor(DayOfWeek),
                  DayofMonth = as.factor(DayofMonth))

  #Calculate model
  try({
    trainRows = base::sample(1:nrow(tmp),ceiling(nrow(tmp)*.7))
    tmp = tmp[trainRows,]
    timing_wide = system.time({
      wide_model = rpart(ArrDelay~.,data = tmp,method="anova")
    })
    write.csv(wide_model$cptable,paste0("DecisionTrees/",strsplit(i,"\\.")[[1]][1]," wide regression decision tree R.txt"))
    residuals = tmp$ArrDelay - predict(wide_model,tmp)
    rm(wide_model)
    cat("MSE from wide training dataset: ",mean(residuals^2,na.rm=T),"\n",sep="")
  })

  #reduce the number of columns
  tmp %<>% select(-Month,-DayofMonth,-DayOfWeek,-UniqueCarrier)
  #Calculate summary statistics
  try({
    timing_narrow = system.time({
      narrow_model = rpart(ArrDelay~.,data = tmp,method="anova")
    })
    write.csv(narrow_model$cptable,paste0("DecisionTrees/",strsplit(i,"\\.")[[1]][1]," narrow regression decision tree R.txt"))
    residuals = tmp$ArrDelay - predict(narrow_model,tmp)
    rm(narrow_model)
    cat("MSE from narrow training dataset: ",mean(residuals^2,na.rm=T),"\n",sep="")
  })

  #clean up
  try({
    readr::write_csv(dplyr::data_frame(File=i,Tool="R",NarrowTime=timing_narrow[3],WideTime=timing_wide[3],Technique="regression decision tree"), "performance measures.txt", append=T)
    rm(tmp)
    rm(timing_narrow,timing_wide)
    gc()
  })
}