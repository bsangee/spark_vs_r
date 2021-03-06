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
  ## Diverted because something can't be cancled AND diverted
  ## Delays because they're mostly missing values
  ## The remaining because they're nearly always missing when cancelled
  tmp = readr::read_csv(i,col_types = types) %>%
    dplyr::select(-Year,-CancellationCode,-Diverted,
      -CarrierDelay,-WeatherDelay,-NASDelay,-SecurityDelay,-LateAircraftDelay,
      -DepDelay,-TaxiOut,-TaxiIn,-DepTime,-ArrTime,-ActualElapsedTime,-AirTime,-ArrDelay,-DepDelay) %>%
    dplyr::mutate(UniqueCarrier = as.factor(UniqueCarrier),
      Month = as.factor(Month),
      DayOfWeek = as.factor(DayOfWeek),
      DayofMonth = as.factor(DayofMonth))

  #Calculate summary statistics
  try({
    trainRows = base::sample(1:nrow(tmp),ceiling(nrow(tmp)*.7))
    tmp = tmp[trainRows,]
    timing_wide = system.time({
      wide_model = rpart(Cancelled~.,data = tmp,method="class")
    })
    write.csv(wide_model$cptable,paste0("DecisionTrees/",strsplit(i,"\\.")[[1]][1]," wide decision tree R.txt"))
    preds = as.numeric(predict(wide_model,tmp)[,2] > 0.5)
    rm(wide_model)
    preds = factor(preds,levels = c(0,1))
    accTab = table(preds,tmp$Cancelled)
    accuracy = (accTab[1,1] + accTab[2,2])/sum(accTab)
    cat("Accuracy on wide training dataset: ",round(accuracy*100,2),"%\n",sep="")
  })

  #reduce the number of columns
  tmp %<>% select(-Month,-DayofMonth,-DayOfWeek,-UniqueCarrier,-TailNum,-Origin,-Dest)
  #Calculate summary statistics
  try({
    timing_narrow = system.time({
      narrow_model = rpart(Cancelled~.,data = tmp,method="class")
    })
    write.csv(narrow_model$cptable,paste0("DecisionTrees/",strsplit(i,"\\.")[[1]][1]," narrow decision tree R.txt"))
    preds = as.numeric(predict(narrow_model,tmp)[,2] > 0.5)
    rm(narrow_model)
    preds = factor(preds,levels = c(0,1))
    accTab = table(preds,tmp$Cancelled)
    accuracy = (accTab[1,1] + accTab[2,2])/sum(accTab)
    cat("Accuracy on narrow training dataset: ",round(accuracy*100,2),"%\n",sep="")
  })

  #clean up
  try({
    readr::write_csv(dplyr::data_frame(File=i,Tool="R",NarrowTime=timing_narrow[3],WideTime=timing_wide[3],Technique="logistic"), "performance measures.txt", append=T)
    rm(tmp)
    rm(timing_narrow,timing_wide)
    gc()
  })
}