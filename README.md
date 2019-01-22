# video
Can we [kill the radio star](https://www.youtube.com/watch?v=Iwuy4hHO3YQ)?

## Idea

Conducting an unprecedented wide and deep radio survey with the low-frequency radio interferometer (LOFAR) we recently detected variable and strong circularly-polarized broadband radio emission from a nearby M-dwarf (M4.5V, V=13.3, I=10.1). Since the star itself is quiescent (the first low-frequency detection of a non-flare star), one hypothesis is that the emission comes from the magnetosphere of a gas-giant planet. Astronomers have been contemplating low-frequency radio emission from exoplanets for more than 30 years, so if true this would indeed be very exciting (and would obviously have significant impact on assessing exoplanetary magnetospheres, interiors, and climates).

So we asked ourselves, is there any evidence for a planet around this star? It turns out that there are about a dozen RV-measurements from ELODIE, SOPHIE, and ESPADONS taken over the course of 20+ years. The RV of the star varies by up to 500 m/s, both between epochs observed with the same instrument, and across instruments. However, the window function is so poor that no reliable period can be identified and the data analysing is high. The story is also more complicated as the TRES team led by David did not see any significant offset in their two epochs on the system.

We have had 13 epochs of the star with HARPS-North over about 2 weeks to test the planet hypothesis. The reported CCF RVs from the automated pipeline appear significant. However, the automated pipeline failed to use the correct mask despite continual requests to change it (K5 instead of M2). We therefore believe that the uncertainties on the RVs are much larger than quoted. 

## Method

We want to use [wobble](https://github.com/megbedell/wobble) to get good RVs from these HARPS-N data. 

## Data

All HARPS-N data are in data/. 