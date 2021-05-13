from pywps import LiteralInput, ComplexInput, ComplexOutput, Format
from wps_tools.io import log_level, collect_args


climdex_input = ComplexInput(
    "climdex_input",
    "climdexInput file",
    abstract="RDS or Rdata (.rds, .rda, .rdata) file containing R Object of type climdexInput",
    min_occurs=1,
    max_occurs=100,
    supported_formats=[Format("application/x-gzip", encoding="base64")],
)

climdex_single_input = ComplexInput(
    "climdex_input",
    "climdexInput file",
    abstract="RDS or Rdata (.rds, .rda, .rdata) file containing R Object of type climdexInput",
    min_occurs=1,
    max_occurs=1,
    supported_formats=[Format("application/x-gzip", encoding="base64")],
)

output_file = LiteralInput(
    "output_file",
    "Output file name",
    abstract="Filename to store the output Rdata (extension .rda)",
    min_occurs=0,
    max_occurs=1,
    default="output.rda",
    data_type="string",
)

rda_output = ComplexOutput(
    "rda_output",
    "Rda output file",
    abstract="Rda file containing R output data. Objects are saved based on climate index name, "
    "file input index, and name from file - default 'ci' for RDS (e.g. su0_ci, su1_climdedexInput, etc.).",
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)

tmax_column = LiteralInput(
    "tmax_column",
    "tmax column",
    default="tmax",
    abstract="Column name for tmax data.",
    data_type="string",
)

tmin_column = LiteralInput(
    "tmin_column",
    "tmin column",
    default="tmin",
    abstract="Column name for tmin data.",
    data_type="string",
)

prec_column = LiteralInput(
    "prec_column",
    "prec column",
    default="prec",
    abstract="Column name for prec data.",
    data_type="string",
)

tavg_column = LiteralInput(
    "tavg_column",
    "tavg column",
    default="tavg",
    abstract="Column name for tavg data.",
    data_type="string",
)

base_range = LiteralInput(
    "base_range",
    "basline range",
    default="c(1961, 1990)",
    abstract="Years to use for the baseline",
    data_type="string",
)

cal = LiteralInput(
    "cal",
    "calendar type",
    default="gregorian",
    abstract="The calendar type used in the input files.",
    data_type="string",
)

date_fields = LiteralInput(
    "date_fields",
    "date fields",
    default="c('year', 'jday')",
    abstract="Vector of names consisting of the columns to be concatenated together with spaces.",
    data_type="string",
)

date_format = LiteralInput(
    "date_format",
    "date format",
    default="%Y %j",
    abstract="Date format as taken by strptime.",
    data_type="string",
)

n = LiteralInput(
    "n",
    "number of days",
    default=5,
    abstract="Number of days to use as window for daily quantiles.",
    data_type="integer",
)

northern_hemisphere = LiteralInput(
    "northern_hemisphere",
    "number of days",
    default=True,
    abstract="Number of days to use as window for daily quantiles.",
    data_type="boolean",
)

quantiles = LiteralInput(
    "quantiles",
    "threshold quantiles",
    abstract="Threshold quantiles for supplied variables.",
    default="NULL",
    data_type="string",
)

temp_qtiles = LiteralInput(
    "temp_qtiles",
    "precipitation quantiles",
    default="c(0.1, 0.9)",
    abstract="Quantiles to calculate for temperature variables",
    data_type="string",
)

prec_qtiles = LiteralInput(
    "prec_qtiles",
    "temperature quantiles",
    default="c(0.95, 0.99)",
    abstract="Quantiles to calculate for precipitation",
    data_type="string",
)

max_missing_days = LiteralInput(
    "max_missing_days",
    "maximum missing days",
    default="c(annual = 15, monthly =3)",
    abstract="Vector containing thresholds for number of days allowed missing per year (annual) and per month (monthly).",
    data_type="string",
)

min_base_data_fraction_present = LiteralInput(
    "min_base_data_fraction_present",
    "minimum fraction of base data",
    default=0.1,
    abstract="Minimum fraction of base data that must be present for quantile to be calculated for a particular day",
    data_type="float",
)

vector_name = LiteralInput(
    "vector_name",
    "Output vector variable name",
    abstract="Name to label the output vector",
    default="days",
    min_occurs=0,
    max_occurs=1,
    data_type="string",
)

ci_output = ComplexOutput(
    "climdexInput",
    "generated climdexInput",
    abstract="Output R data file for generated climdexInput",
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)

freq = LiteralInput(
    "freq",
    "Frequency",
    abstract="Time frequency to aggregate to",
    allowed_values=["monthly", "annual"],
    default="monthly",
    min_occurs=0,
    max_occurs=1,
    data_type="string",
)

tmax_file_content = LiteralInput(
    "tmax_file_content",
    "daily maximum temperature data file content",
    abstract="Content of file with daily maximum temperature data "
    "(temporary alternative to taking file).",
    min_occurs=0,
    max_occurs=1,
    data_type="string",
)

tmin_file_content = LiteralInput(
    "tmin_file_content",
    "daily minimum temperature data file",
    abstract="Content of file with daily minimum temperature data "
    "(temporary alternative to taking file).",
    min_occurs=0,
    max_occurs=1,
    data_type="string",
)

prec_file_content = LiteralInput(
    "prec_file_content",
    "daily total precipitation data file content",
    abstract="Content of file with daily total precipitation data "
    "(temporary alternative to taking file).",
    min_occurs=1,
    max_occurs=1,
    data_type="string",
)

tavg_file_content = LiteralInput(
    "tavg_file_content",
    "mean temperature data file content",
    abstract="Content of file with daily mean temperature data "
    "(temporary alternative to taking file).",
    min_occurs=0,
    max_occurs=1,
    data_type="string",
)

na_strings = LiteralInput(
    "na_strings",
    "climdexInput name",
    abstract="Strings used for NA values; passed to read.csv",
    default="NULL",
    data_type="string",
)

tmax_file = ComplexInput(
    "tmax_file",
    "daily maximum temperature data file",
    abstract="Name of file containing daily maximum temperature data.",
    min_occurs=0,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", encoding="base64"),
    ],
)

tmin_file = ComplexInput(
    "tmin_file",
    "daily minimum temperature data file",
    abstract="Name of file containing daily minimum temperature data.",
    min_occurs=0,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", encoding="base64"),
    ],
)

prec_file = ComplexInput(
    "prec_file",
    "daily total precipitation data file",
    abstract="Name of file containing daily total precipitation data.",
    min_occurs=1,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", encoding="base64"),
    ],
)

tavg_file = ComplexInput(
    "tavg_file",
    "mean temperature data file",
    abstract="Name of file containing daily mean temperature data.",
    min_occurs=0,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", encoding="base64"),
    ],
)

tmax_name = LiteralInput(
    "tmax_name",
    "daily maximum temperature object name",
    default="tmax",
    abstract="In a Rda file, the name of the R object containing daily "
    "maximum temperature data. You may leave as default for RDS files.",
    data_type="string",
)

tmin_name = LiteralInput(
    "tmin_name",
    "daily minimum temperature data file",
    default="tmin",
    abstract="In a Rda file, the name of the R object containing daily "
    "minimum temperature data. You may leave as default for RDS files.",
    data_type="string",
)

prec_name = LiteralInput(
    "prec_name",
    "daily total precipitation data file",
    default="prec",
    abstract="In a Rda file, the name of the R object containing daily "
    "mean temperature data. You may leave as default for RDS files.",
    data_type="string",
)

tavg_name = LiteralInput(
    "tavg_name",
    "mean temperature data file",
    default="tavg",
    abstract="In a Rda file, the name of the R object containing daily total "
    "precipitation data. You may leave as default for RDS files.",
    data_type="string",
)

days_type = LiteralInput(
    "days_type",
    "Day type to compute",
    abstract="Day type condition to compute",
    allowed_values=["su", "id", "fd", "tr"],
    min_occurs=1,
    max_occurs=1,
    data_type="string",
)

ci_name = LiteralInput(
    "ci_name",
    "climdexInput name",
    abstract="Name of the climdexInput object. Only needed when using Rdata input. "
    "For RDS input it may be left as the default value.",
    default="ci",
    min_occurs=1,
    max_occurs=1,
    data_type="string",
)

gsl_mode = LiteralInput(
    "gsl_mode",
    "GSL mode",
    abstract="Growing season length method to use. The three alternate modes provided ('GSL_first', 'GSL_max', and 'GSL_sum') are for testing purposes only.",
    default="GSL",
    min_occurs=0,
    max_occurs=1,
    allowed_values=["GSL", "GSL_first", "GSL_max", "GSL_sum"],
    data_type="string",
)

csv_inputs = [
    tmax_file_content,
    tmin_file_content,
    prec_file_content,
    tavg_file_content,
    na_strings,
    tmax_column,
    tmin_column,
    prec_column,
    tavg_column,
    base_range,
    cal,
    date_fields,
    date_format,
    n,
    northern_hemisphere,
    quantiles,
    temp_qtiles,
    prec_qtiles,
    max_missing_days,
    min_base_data_fraction_present,
    output_file,
    vector_name,
    log_level,
]

raw_inputs = [
    tmax_file,
    tmin_file,
    prec_file,
    tavg_file,
    tmax_name,
    tmin_name,
    prec_name,
    tavg_name,
    tmax_column,
    tmin_column,
    prec_column,
    tavg_column,
    base_range,
    cal,
    date_fields,
    date_format,
    n,
    northern_hemisphere,
    quantiles,
    temp_qtiles,
    prec_qtiles,
    max_missing_days,
    min_base_data_fraction_present,
    output_file,
    vector_name,
    log_level,
]

days_inputs = [
    climdex_input,
    output_file,
    days_type,
    log_level,
]

dtr_inputs = [
    climdex_input,
    output_file,
    freq,
    log_level,
]

avail_indices_inputs = [
    climdex_single_input,
    ci_name,
    output_file,
    log_level,
]

gsl_inputs = [
    climdex_input,
    output_file,
    gsl_mode,
    log_level
]
