# Processes
- [Climdex Days](#climdex-days)
- [Climdex DTR](#climdex-dtr)
- [Get Indices](#get-indices)
- [Climdex GSL](#climdex-gsl)
- [Climdex MMDMT](#climdex-mmdmt)
- [Climdex Ptot](#climdex-ptot)
- [Climdex Quantile](#climex-quantile)
- [Climdex RMM](#climdex-rmm)
- [Climdex Rxn day](#climdex-rxn-day)
- [Climdex SDII](#climdex-sdii)
- [Climdex Spells](#climdex-spells)
- [Climdex Temp Pctl](#climdex-temp-pctl)
- [ClimdexInput CSV](#climdexinput-csv)
- [ClimdexInputRaw](#climdexinput-raw)

## Climdex Days
Takes a climdexInput object as input and computes the annual count of days where daily temperature satisfies some condition.
  - `climdex.su` "summer": the annual count of days where daily maximum temperature exceeds 25 degrees Celsius
  - `climdex.id` "icing": the annual count of days where daily maximum temperature was below 0 degrees Celsius
  - `climdex.fd` "frost": the annual count of days where daily minimum temperature was below 0 degrees Celsius
  - `climdex.tr` "tropical nights": the annual count of days where daily minimum temperature stays above 20 degrees Celsius

[Notebook Demo](formatted_demos/wps_climdex_days_demo.html)

## Climdex DTR
Computes the mean daily diurnal temperature range.

[Notebook Demo](formatted_demos/wps_climdex_dtr_demo.html)

## Get Indices
Takes a `climdexInput` object as input and returns a dictionary with the names of all the indices which may be computed as values and which processes they are accessible by as keys

[Notebook Demo](formatted_demos/wps_get_available_indices_demo.html)

## Climdex GSL
Computes the growing season length (GSL). Growing season length is the number of days between the start of the first spell of warm days in the first half of the year, defined as six or more days with mean temperature above 5 degrees Celsius, and the start of the first spell of cold days in the second half of the year, defined as six or more days with a mean temperature below 5 degrees Celsius.

[Notebook Demo](formatted_demos/wps_climdex_gsl_demo.html)

## Climdex MMDMT
This process wraps climdex functions:
- `climdex.txx`: Monthly (or annual) Maximum of Daily Maximum Temperature
- `climdex.tnx`: Monthly (or annual) Maximum of Daily Minimum Temperature
- `climdex.txn`: Monthly (or annual) Minimum of Daily Maximum Temperature
- `climdex.tnn`: Monthly (or annual) Minimum of Daily Minimum Temperature

[Notebook Demo](formatted_demos/wps_climdex_mmdmt_demo.html)

## Climdex Ptot
Wraps `climdex.r95ptot`, `climdex.r99ptot` and `climdex.prcptot`. Computes the annual sum of precipitation in days where daily precipitation exceeds the daily precipitation threshold in the base period. If threshold is not given, annual sum of precipitation in wet days (> 1mm) will be calculated.

[Notebook Demo](formatted_demos/wps_climdex_ptot.html)

## Climdex Quantile
This function implements `R`’s type=8 in a more efficient manner.

[Notebook Demo](formatted_demos/wps_climdexInput_quantile_demo.html)

## Climdex RMM
Wraps `climdex.r10mm`, `climdex.r20mm` and `climdex.rnnmm`. The annual count of days where daily precipitation is more than [threshold] mm per day.

[Notebook Demo](formatted_demos/wps_climdex_rmm_demo.html)

## Climdex Rxn day
- `climdex.rx1day`: monthly or annual maximum 1-day precipitation
- `climdex.rx5day`: monthly or annual maximum 5-day consecutive precipitation.

[Notebook Demo](formatted_demos/wps_climdex_rxnday_demo.html)

## Climdex SDII
Computes the climdex index SDII, or Simple Precipitation Intensity Index. This is defined as the sum of precipitation in wet days (days with precipitation over 1mm) during the year divided by the number of wet days in the year.

[Notebook Demo](formatted_demos/wps_climdex_sdii_demo.html)

## Climdex Spells
Cold or warm spell duration index and maximum consecutive dry or wet days. Wraps:
- `climdex.cdd`
- `climdex.csdi`
- `climdex.cwd`
- `climdex.wsdi`

[Notebook Demo](formatted_demos/wps_climdex_spells_demo.html)

## Climdex Temp Pctl
This process wraps climdex functions
- `climdex.tn10p`: computes the monthly or annual percent of values below the 10th percentile of baseline daily minimum temperature.
- `climdex.tn90p`: computes the monthly or annual percent of values above the 90th percentile of baseline daily minimum temperature.
- `climdex.tx10p`: computes the monthly or annual percent of values below the 10th percentile of baseline daily maximum temperature.
- `climdex.tx90`p: computes the monthly or annual percent of values above the 90th percentile of baseline daily maximum temperature.

[Notebook Demo](formatted_demos/wps_climdex_temp_pctl_demo.html)

## ClimdexInput CSV
Process for creating climdexInput object from CSV files.

[Notebook Demo](formatted_demos/wps_climdexInput_csv_demo.html)

## ClimdexInput Raw
Process for creating climdexInput object from data already ingested into `R`.

[Notebook Demo](formatted_demos/wps_climdexInput_raw_demo.html)
