from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, FORMATS
from pywps.inout.formats import Format

climdex_input = ComplexInput(
    "climdex_input",
    "climdexInput",
    abstract="Rdata (.rda) file containing R Object of type climdexInput",
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

output_path = LiteralInput(
    "output_path",
    "Output file name",
    abstract="Filename to store the output Rdata (extension .rda)",
    data_type="string",
)