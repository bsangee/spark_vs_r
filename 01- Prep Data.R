library(readr) #if not installed: install.packages('readr')
library(magrittr) #if not installed; install.packages('magrittr')

parent = structure(list(Year = integer(0), Month = integer(0), DayofMonth = integer(0), 
    DayOfWeek = integer(0), DepTime = integer(0), CRSDepTime = integer(0), 
    ArrTime = integer(0), CRSArrTime = integer(0), UniqueCarrier = character(0), 
    FlightNum = integer(0), TailNum = character(0), ActualElapsedTime = integer(0), 
    CRSElapsedTime = integer(0), AirTime = integer(0), ArrDelay = integer(0), 
    DepDelay = integer(0), Origin = character(0), Dest = character(0), 
    Distance = integer(0), TaxiIn = integer(0), TaxiOut = integer(0), 
    Cancelled = integer(0), CancellationCode = character(0), 
    Diverted = integer(0), CarrierDelay = character(0), WeatherDelay = character(0), 
    NASDelay = character(0), SecurityDelay = character(0), LateAircraftDelay = character(0)), .Names = c("Year", 
"Month", "DayofMonth", "DayOfWeek", "DepTime", "CRSDepTime", 
"ArrTime", "CRSArrTime", "UniqueCarrier", "FlightNum", "TailNum", 
"ActualElapsedTime", "CRSElapsedTime", "AirTime", "ArrDelay", 
"DepDelay", "Origin", "Dest", "Distance", "TaxiIn", "TaxiOut", 
"Cancelled", "CancellationCode", "Diverted", "CarrierDelay", 
"WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"
), row.names = integer(0), class = c("tbl_df", "tbl", "data.frame"))

appendr = function(x,types){
  print(x)
  tmp = readr::read_csv(x,col_types = types)
  if(grepl('^2',x)) readr::write_csv(tmp,'00-08.csv',append = T)
  if(grepl('^199[5-9]|^2',x)) readr::write_csv(tmp,'95-08.csv',append = T)
  readr::write_csv(tmp,'everything.csv',append=T)
}

csvFiles = list.files() %>% .[grepl('[0-9]{4}.csv$',.)]
types = c("i", "i", "i", "i", "i", "i", 
"i", "i", "c", "i", "c", "i", 
"i", "i", "i", "i", "c", "c", 
"i", "i", "i", "i", "c", "i", 
"c", "c", "c", "c", "c"
) %>% paste(collapse='')

readr::write_csv(parent,'00-08.csv')
readr::write_csv(parent,'95-08.csv')
readr::write_csv(parent,'everything.csv')

lapply(csvFiles,appendr,types)
