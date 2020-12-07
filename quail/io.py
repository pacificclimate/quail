from pywps import LiteralInput, ComplexInput, ComplexOutput, Format

climdex_input = ComplexInput(
    "climdex_input",
    "climdexInput",
    abstract="Rdata (.rda) file containing R Object of type climdexInput",
    min_occurs=1,
    max_occurs=1,
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)

ci_name = LiteralInput(
    "ci_name",
    "climdexInput name",
    abstract="Name of the climdexInput object",
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
