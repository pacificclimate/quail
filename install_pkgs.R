# Create user library
dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE)
.libPaths(Sys.getenv("R_LIBS_USER"))

# Install and load RcppTOML
if (!requireNamespace("RcppTOML", quietly = TRUE)) {
    install.packages("RcppTOML", repos = "https://cloud.r-project.org")
}
library(RcppTOML)

# Read the TOML file
toml_data <- RcppTOML::parseTOML("pyproject.toml")

# Extract dependencies
deps <- toml_data$tool$quail$`r-dependencies`

if (!requireNamespace("remotes", quietly = TRUE)) {
    install.packages("remotes", repos = "https://cloud.r-project.org")
}

# Install packages with versions using remotes
for (pkg in names(deps)) {
    ver <- deps[[pkg]]
    if (!(pkg %in% rownames(installed.packages()))) {
        if (is.null(ver) || ver == "*" || ver == "") {
            install.packages(pkg, repos = "https://cloud.r-project.org")
        } else {
            remotes::install_version(pkg, version = ver, repos = "https://cloud.r-project.org")
        }
    }
}


remotes::install_github("pacificclimate/climdex.pcic@daf4790",
    dependencies = TRUE,
)
