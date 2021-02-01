from pywps import LiteralInput, ComplexInput, ComplexOutput, Format

climdex_input = ComplexInput(
    "climdex_input",
    "climdexInput",
    abstract="Rdata (.rda) file containing R Object of type climdexInput",
    min_occurs=0,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)

ci_rds = ComplexInput(
    "ci_rds",
    "climdexInput RDS",
    abstract="RDS (.rds) file containing R Object of type climdexInput. "
    "You must include input for one of either ci_rds or ci_rda.",
    min_occurs=0,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)

ci_rda = ComplexInput(
    "ci_rda",
    "climdexInput RDA",
    abstract="Rdata (.rda) file containing R Object of type climdexInput. "
    "You must include input for one of either ci_rds or ci_rda.",
    min_occurs=0,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", extension=".rds", encoding="base64")
    ],
)

ci_name = LiteralInput(
    "ci_name",
    "climdexInput name",
    abstract="Name of the climdexInput object. Only needed when using ci_rda input.",
    default="ci",
    min_occurs=1,
    max_occurs=1,
    data_type="string",
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
    abstract="Rda file containing R output data",
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
