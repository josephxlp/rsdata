# RSData

RSData is a Python-based project designed to download and process satellite imagery from Sentinel-1 and Sentinel-2. It allows users to specify a time range and geographical area to obtain the median image with selected bands for Sentinel-2, while Sentinel-1 data is always processed with VV and VH polarizations. Users can also select the polarization and direction (descent/ascent) for Sentinel-1.

## Features

- **Sentinel-1 and Sentinel-2 Data Download**: Automatically download satellite imagery based on user-specified parameters.
- **Median Image Calculation**: Compute the median image for the specified time and geometry.
- **Band Selection for Sentinel-2**: Choose specific bands for processing Sentinel-2 data.
- **Polarization and Direction Selection for Sentinel-1**: Default processing with VV and VH polarizations, with options to select polarization and direction.

## Requirements

- Python 3.x
- Required Python libraries (install via `requirements.txt`)

## Installation

1. Clone the repository:
   