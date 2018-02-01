# p3-Profiler
Experiments on profiling SpiNNaker.

The SpiNNProfiler.MDI gives a complete interface for observing (profiling) the SpiNNaker while running a program on it.

To record power data (using SpiNN-4 board), a simple script (called profiler_cli.py) was created. To use this script, a serial connection (usually at /dev/ttyACM0 in Fedora machine) must be accessible. The script also requires python serial module to work with.


