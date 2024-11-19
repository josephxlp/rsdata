# RSData Project Metadata

RSData is designed to scale Google Earth Engine for downloading large volumes of data. It supports multiple datasets with various options for customization and processing.

## Available Datasets and Options

### Sentinel-1
- **Area of Interest (AOI)**: Specify as a polygon or bounding box.
- **Polarization (pol)**: Options are 'VV' or 'VH'.
- **Orbit Pass (opass)**: Options are 'ASCENDING' or 'DESCENDING'.
- **Date Range**: Specify start date (`idate`) and end date (`fdate`), e.g., '2019-01-01' to '2022-12-01'.
- **Returns**: VV and VH bands.

### Sentinel-2
- **Region**: Specify the area of interest.
- **Band Codes**: Select specific bands for processing.
- **Cloud Filter**: Default is 30.
- **Date Range**: Specify start and end dates.
- **Returns**: Median image with specified bands in `band_codes`.

### Copernicus DSM
- **Input**: Takes a polygon or bounding box.
- **Returns**: Variables within the dataset, including:
  - `WBM`: Water Body Mask
  - `HEM`: Height Error Mask
  - `FLM`: Forest Loss Mask
  - `EDM`: Elevation Data Mask
  - `DEM`: Digital Elevation Model

### Aster
- **Input**: Takes coordinates in the format (xmin, ymin, xmax, ymax) in EPSG:4326 (WGS 84).
- **Returns**: Both ASTER DEM and water mask.

## Usage

The project is structured to handle large datasets efficiently, leveraging Google Earth Engine's capabilities to process and download data based on user-defined parameters.

For more detailed instructions on how to use each dataset option, refer to the specific scripts `S1.py` and `S2.py` included in the project.