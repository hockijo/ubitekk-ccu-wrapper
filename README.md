# Single Photon Environment Setup

## Description

This guide provides instructions for setting up a Conda environment named "single_photon" and installing the necessary dependencies for the project.

## Prerequisites

- Anaconda or Miniconda installed, see <https://www.anaconda.com/download>

## Steps

1. Create the Conda environment:

   ```bash
   conda create --name single_photon
   ```

2. Activate the environment

    ```bash
    conda activate single_photon
    ```

3. Install the required packages

    ```bash
    conda install numpy matplotlib scipy pandas
    ```

4. Install the CCU control package
    - Navigate to the directory containing the CCU control package
    - Run the following command

    ```bash
    pip install -e .
    ```

## Examples

Here is some example usage fore connecting the device, reading the counts, and then appending it to a csv file:

```python
ccu = CCU()
ccu.connect("/dev/ttyUSB0")
ccu.append_counts_to_csv("counts.csv")
ccu.close()
```

You can read individual counts using:

```python
ch1 = ccu.read_count("CH1")
ch2 = ccu.read_count("CH2")
coincidence = ccu.read_count("COINCIDENCE")
```
