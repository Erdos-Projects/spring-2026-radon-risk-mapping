# Data Inventory

## 1. 2016 Canadian Census Profile

**Source:**  
Statistics Canada – 2016 Census Profile  
Catalogue no. 98-401-X2016046  
File: `98-401-X2016046_English_CSV_data.csv`

**Granularity:**  
Forward Sortation Area (FSA) level

**Geographic Unit:**  
FSA (first three characters of Canadian postal code)

**Data Structure:**

The Census Profile file is provided in long format:

    GEO_CODE (POR) × Member ID → Value

The dataset is pivoted to a wide FSA × Member ID matrix before feature engineering.

Only the following columns are loaded for processing:

- `GEO_CODE (POR)`
- `GEO_LEVEL`
- `Member ID: Profile of Forward Sortation Areas (2247)`
- `Dim: Sex (3): Member ID: [1]: Total - Sex`

Filtering logic:

- `GEO_LEVEL == 2` corresponds to Forward Sortation Areas.
- The Canada aggregate row (`GEO_CODE (POR) == "01"`) is removed.

---

### Structural Housing Variables (100% Data)

Source Table: Structural type of dwelling (100% sample)

| Feature | Member ID | Description |
|----------|------------|-------------|
| total_occupied_private_dwellings | 41 | Total occupied private dwellings |
| single_detached | 42 | Single-detached house |
| highrise_apartment_5plus | 43 | Apartment in building ≥5 storeys |
| other_attached_total | 44 | Other attached dwelling |
| semi_detached | 45 | Semi-detached house |
| row_house | 46 | Row house |
| duplex | 47 | Apartment in duplex |
| lowrise_apartment_lt5 | 48 | Apartment <5 storeys |
| other_single_attached | 49 | Other single-attached |
| movable_dwelling | 50 | Movable dwelling |

Derived features:

- `pct_single_detached = 42 / 41`
- `pct_highrise = 43 / 41`
- `pct_other_attached = 44 / 41`
- `pct_movable = 50 / 41`

---

### Known Census Data Issues

1. **Rounding artifacts**  
   Census counts are rounded to the nearest multiple of 5.  
   As a result:

   - Subcategory sums may not exactly equal parent totals.
   - Proportions may not sum exactly to 1.

2. **Mixed sampling fractions**  
   - Structural dwelling variables are 100% data.
   - Some other variables (e.g., housing age, condition, income) are based on 25% sample data.

3. **Small-area suppression / missingness**  
   Very small FSAs may have missing values in 25% sample tables.

4. **Geographic coding**  
   `GEO_LEVEL` is numerically coded.  
   Code `2` corresponds to FSA level.

---

## 2. Cross-Canada Radon Survey

**Source:**  
Health Canada – Cross-Canada Survey of Radon Concentrations in Homes

**Granularity:**  
Individual dwelling measurement level

**Key Variables Used:**

| Variable | Description |
|-----------|-------------|
| ForwardSortationAreaCodes | FSA of dwelling |
| AverageRadonConcentrationInBqPerM3 | Measured radon concentration |
| Province | Province |
| Health Region | Health region |

---

### Radon Data Handling

- Radon values reported as `"<15"` are converted to numeric.
- A numeric column `radon_numeric` is created.
- A log-transformed variable `log_radon` is created for regression modeling.
- Approximately three FSA codes did not match census data during merge.

---

## Final Modeling Unit

The modeling dataset is constructed by:

1. Engineering FSA-level census features.
2. Merging census features onto each individual radon measurement via FSA code.
3. Performing modeling at the individual radon measurement level.

---

## Notes for Reproducibility

- Census file is loaded using `usecols` to minimize memory footprint.
- Census long format is pivoted once to a canonical FSA × Member ID matrix.
- All feature construction is performed on the pivoted matrix.
- Geographic filtering and cleaning are handled in modular preprocessing functions.