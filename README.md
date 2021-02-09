# propellant-selector
Works with thermodynamic, thermophysical and performance data for a small range
of propellants, to allow rapid calculation of vehicle performance

Performance calculation looks at engine performance, tank volume and weight.
May be expanded to include stuff like temperature, flow rate for given thrust
etc

All data sourced from NIST tables, https://webbook.nist.gov/chemistry/fluid/,
and fit to order 10 polynomials with numpy
