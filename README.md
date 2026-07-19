# Eastern Arabian Sea air-sea CO2 flux (SK-322/GC-02)

Calculates air-sea CO2 flux from the pCO2 gradient derived from boron isotopes (delta-11B), following the gas exchange formulation in Wanninkhof (2014).

## The physics

    F = k * K0 * dpCO2

Three quantities feed into this:

- **Solubility (K0)** - depends on sea surface temperature (SST) and salinity.
- **Gas transfer velocity (k)** - depends on SST (via the Schmidt number) and wind speed (U10).
- **pCO2 gradient (dpCO2)** - the difference between ocean surface pCO2 and atmospheric pCO2.

In this project:
- SST comes from Mg/Ca paleothermometry (measured on the core).
- Salinity is held fixed at 35 PSU.
- Wind (U10) comes from PMIP4 model output for LGM and mid-Holocene time slices (see below).
- Atmospheric pCO2 is not yet wired in - it requires the samples to be placed on an age axis first, then interpolated against an ice-core CO2 record. This is blocked on a revised age model (in progress, external to this repo).

## Files

- **`flux_physics.py`** - the core flux calculation. All physics equations live here, cited to source (Weiss 1974, Wanninkhof 2014). Imported by the notebooks below rather than redefined in each.
- **`eas_co2_flux.ipynb`** - main notebook. Loads the core's boron/Mg-Ca data, runs it through `flux_physics.py`, and plots the resulting flux down-core.
- **`pmip_wind.ipynb`** - downloads, merges, and averages PMIP4 paleo-wind NetCDF output for the site, across multiple climate models. Produces the wind values used in `eas_co2_flux.ipynb`.

## Coastal contamination in the wind extraction

The core site sits close to the Indian coastline. Initial wind values were extracted from the PMIP grid cell nearest the site's exact coordinates - but at this resolution, that nearest cell blends land and ocean conditions, biasing the wind estimate low.

Fix: the extraction point was shifted approximately 2.5 degrees west of the site, into a cell confirmed (via gridded maps) to be clear open ocean, before averaging. This raised the multi-model wind estimate from 4.74 +/- 0.60 m/s (coastal, contaminated) to 6.86 +/- 0.52 m/s (open ocean), consistent with the modern Arabian Sea monsoon range (6-9 m/s).

## PMIP models used

Three CMIP6/PMIP4 models, downloaded for both the `lgm` and `midHolocene` experiments:

| Folder name       | Full model name        | Institution |
|--------------------|------------------------|-------------|
| `AWI-ESM-1-1-LR`   | AWI-ESM-1.1-LR          | Alfred Wegener Institute |
| `INM-CM4-8`        | INM-CM4-8               | Institute for Numerical Mathematics (Russian Academy of Science) |
| `MPI-ESM1-2-LR`    | MPI-ESM1.2-LR           | Max Planck Institute for Meteorology |

## Status / next steps

1. **Age axis.** Once the revised age model arrives, add an `age_kyr_v2` column and plot against that instead of `depth_cm`.
2. **Real atmospheric CO2.** Load the ice-core CO2 series, interpolate it onto sample ages, and replace the current `pco2_atm` placeholder constant.
3. **Real wind, per sample.** Plug the PMIP-derived LGM and mid-Holocene wind values in at the correct ages, once the age model lands (currently a single constant applied across the whole record).
4. **Modern-day validation (in progress).** Before trusting the flux calculation on 50,000-year-old paleo data, check it against the present day, where the answer is already known. This builds a small gridded map of modern SST, wind, and pCO2 around the site, runs it through the same flux physics, and compares the result to the published modern Arabian Sea CO2 source (~90 Tg-C/yr, Takahashi et al. 1997, 2009). If the physics reproduces the known modern number, the same machinery can be trusted running backwards in time. Data sources: WOA23 (SST) and Takahashi (2009, surface pCO2) as primary inputs; GLODAP also being considered. Wind from CCMP or ERA5. Exact combination still being finalized.
