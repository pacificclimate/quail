from pywps import LiteralInput, ComplexInput, Format
from datetime import date

ci_file = ComplexInput(
    "ci_file",
    "climdexInput file",
    abstract="File that holds climdexInput object (recommended file extension .rda)",
    supported_formats=[
        Format("application/x-gzip", extension=".rda", encoding="base64")
    ],
)
ci_name = LiteralInput(
    "ci_name",
    "climdexInput name",
    abstract="Name of the climdexInput obejct",
    data_type="string",
)
output_obj = LiteralInput(
    "output_obj",
    "Output object",
    abstract="Name of the output object",
    min_occurs=0,
    max_occurs=1,
    default="fd",
    data_type="string",
)
output_file = LiteralInput(
    "output_file",
    "Output file name",
    abstract="Filename to store the output (recommended file extension .rda)",
    min_occurs=0,
    max_occurs=1,
    default="output.rda",
    data_type="string",
)
