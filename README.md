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

Here is some example usage for connecting the device (on linux), reading the counts, and then appending it to a csv file:

```python
from ccu.ccu import CCU

ccu = CCU()
ccu.connect("/dev/ttyUSB0")
ccu.append_counts_to_csv("counts.csv")
ccu.close()
```

The address of the device can be found using `ccu.list_devices()`, which will return a list of serial devices. Usually it will be the only device listed, but if there is more than one it may be required to try each one until the correct one is found. You can select devices to connect to from the output of `ccu.list_devices()` by using the following syntax:

```python
ports = ccu.list_ports()
ccu.connect(ports[0].device)
```

To take a measurement, use `ccu.take_measurement()`. This will wait `dwell` (ie. the count collection time) + 1 seconds before allowing the program to continue.

You can read individual counts using:

```python
ch1 = ccu.read_count("CH1")
ch2 = ccu.read_count("CH2")
coincidence = ccu.read_count("COINCIDENCE")
```

If you are needing extra functionality beyond this, you may write SCPI commands directly to the device using the following syntax:

```python
ccu.send_command(SCPI_COMMAND_STRING)
```

Where SCPI_COMMAND_STRING is the SCPI command you wish to send, a full list of which may be found on page 10 within the manual of the CCU device.
