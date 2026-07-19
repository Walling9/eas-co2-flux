"""Air-sea CO2 flux physics for the Eastern Arabian Sea work.

Kept in one module so the site-flux and modern-map notebooks share the same
equations rather than each redefining them. Each function is one published
relationship, cited inline.

Flux form:      F = k * K0 * dpCO2          Wanninkhof (1992)
                                
Transfer vel.:  k = 0.251 * u^2 * (Sc/660)^-0.5   Wanninkhof (2014), Eq. 4
Schmidt no.:    Sc(SST)                     Wanninkhof (2014), Table 1
Solubility K0:  Weiss (1974)

Note on Wanninkhof vintage: the 0.251 coefficient and the 5-term Sc polynomial
below are the 2014 revision. The classic 1992 paper uses 0.31 (short-term wind)
or 0.39 (long-term/monthly wind) and an older 4-term Sc.
"""
import numpy as np

def co2_solubility(sst_c, salinity=35.0): #CO2 solubility K0 [mol kg^-1 atm^-1], Weiss (1974)
    T = sst_c + 273.15
    t100 = T / 100.0
    ln_K0 = (-60.2409 + 93.4517 / t100 + 23.3585 * np.log(t100) + salinity * (0.023517 - 0.023656 * t100 + 0.0047036 * t100**2))
    return np.exp(ln_K0)

def schmidt_co2(sst_c): #Schmidt number of CO2 in seawater, Wanninkhof (2014) Table 1 (S=35)
    #Sc adjusts it for the fact that CO₂ diffuses faster in warm water than cold
    T = sst_c
    return 2116.8 - 136.25*T + 4.7353*T**2 - 0.092307*T**3 + 0.0007555*T**4

def gas_transfer_velocity(u10, sst_c): #Piston velocity k [cm/hr], Wanninkhof (2014) Eq. 4. u10 in m/s
    #For climatological/monthly winds you want the second moment <u^2>, not the square of the mean wind - they differ, and gas exchange cares about <u^2>.
    return 0.251 * u10**2 * (schmidt_co2(sst_c) / 660.0) ** -0.5

def co2_flux(u10, sst_c, delta_pco2_uatm, salinity=35.0, rho=1025.0): #Air-sea CO2 flux [mol m^-2 yr^-1]. +ve = outgassing, rho is seawater density [kg m^-3]
    k = gas_transfer_velocity(u10, sst_c) * (24 * 365) / 100.0   # cm/hr -> m/yr
    K0 = co2_solubility(sst_c, salinity) * rho                  # mol kg^-1 -> mol m^-3
    return k * K0 * (delta_pco2_uatm * 1e-6)                     # atm from uatm