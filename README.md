# Solid-State Hydrogen Storage System Calculator

A Python-based calculation tool for evaluating the energy density and system-level performance of solid-state hydrogen storage systems.

The calculator integrates metal hydride properties, dehydrogenation energy consumption, fuel cell performance, storage vessel geometry, and system-level mass and volume calculations. It provides a framework for comparing hydrogen storage materials and evaluating their suitability for different engineering applications.

## Key Features

### 1. Hydrogen Storage Material Database

Includes six preset solid-state hydrogen storage materials:

| Material | Chemical Formula |
|---|---|
| Magnesium Hydride | MgH2 |
| Titanium Iron Hydride | TiFeH2 |
| Magnesium Nickel Hydride | Mg2NiH4 |
| Lanthanum Nickel Hydride | LaNi5H6 |
| Lithium Aluminum Hydride | LiAlH4 |
| Sodium Borohydride | NaBH4 |

Users can also define custom material properties, including:

- Dehydrogenation enthalpy (kJ/mol)
- Material density (kg/m3)
- Hydrogen mass fraction

### 2. Fuel Cell and System Parameters

The calculator allows users to configure:

- Fuel cell efficiency (%)
- Rated output power (kW)
- Endurance time (h)
- Fuel cell stack mass (kg)
- Fuel cell stack volume (L)
- Error Correction Factor

These parameters are used to estimate the required hydrogen storage capacity and overall system performance.

### 3. Storage Vessel Geometry and Enclosure Design

Supports multiple storage vessel configurations:

- Cylindrical vessel with specified radius
- Cylindrical vessel with specified height
- Minimum-surface-area cylindrical configuration
- Cuboid configuration
- Custom vessel configuration

Additional parameters include:

- Number of storage vessels
- Material filling ratio (%)
- Enclosure wall thickness (mm)
- Enclosure material density (kg/m3)

Both preset and user-defined enclosure material properties are supported.

The calculator estimates enclosure volume, enclosure mass, and the resulting system-level energy density.

### 4. System-Level Energy Density Analysis

The calculator evaluates energy density at different system boundaries:

- Material-level gravimetric energy density (kWh/kg)
- Material-level volumetric energy density (kWh/m3)
- System-level gravimetric energy density without enclosure
- System-level volumetric energy density without enclosure
- System-level gravimetric energy density with enclosure
- System-level volumetric energy density with enclosure

This approach makes it possible to investigate how fuel cell mass, fuel cell volume, and enclosure design affect the effective energy density of a complete hydrogen storage system.

### 5. Visualization and Material Comparison

The application provides interactive visualizations, including:

- Material performance radar charts
- System mass composition charts
- System volume composition charts
- Energy density comparisons

These visualizations help identify the differences between intrinsic material properties and practical system-level performance.

### 6. Calculation Details and Engineering Principles

The application provides step-by-step calculation explanations, covering:

- Dehydrogenation energy consumption
- Net energy generation
- Hydrogen storage material requirements
- Storage vessel geometry calculations
- Enclosure mass and volume estimation
- Overall system energy density

The calculation results can be inspected together with the corresponding mathematical relationships.

### 7. Batch Calculation and Data Export

The batch calculation module supports parametric studies involving:

- Fuel cell efficiency
- Material filling ratio
- Endurance time
- Hydrogen storage material selection
- Enclosure material selection
- Storage vessel geometry
- Preset fuel cell configurations

Batch results include system-level energy density, required material mass and volume, total system mass and volume, and vessel dimensions.

Results can be exported as CSV files for further analysis.

## Calculation Methodology

The calculator uses a simplified energy-density model based on hydrogen energy content, dehydrogenation energy consumption, hydrogen mass fraction, and fuel cell efficiency.

### 1. Dehydrogenation Energy Consumption

The dehydrogenation energy consumption is estimated as:

Q_dehydrogenation = (ΔH × 500) / 3600

Where:

- ΔH: Dehydrogenation enthalpy (kJ/mol)
- 500: Assumed molar conversion factor (mol/kg-H2)
- Q_dehydrogenation: Dehydrogenation energy consumption (kWh/kg-H2)

### 2. Net Energy Generation

The effective energy contribution after considering dehydrogenation energy consumption and fuel cell efficiency is:

E_net = (39.4 − Q_dehydrogenation) × η

Where:

- 39.4 kWh/kg: Fixed hydrogen energy density used in the source code
- η: Fuel cell efficiency (fraction)
- E_net: Net energy generation per unit mass of hydrogen

### 3. Material-Level Gravimetric Energy Density

The material-level gravimetric energy density is calculated as:

ED_mass = E_net × w_H2

Where:

- w_H2: Hydrogen mass fraction of the storage material

### 4. Material-Level Volumetric Energy Density

ED_volume = ED_mass × ρ_material

Where:

- ρ_material: Material density (kg/m3)

### 5. Required Hydrogen Storage Material

For power-based calculations:

E_required = P × t / f_correction

m_material = E_required / ED_mass

V_material = m_material / ρ_material

Where:

- P: Fuel cell rated power (kW)
- t: Required endurance time (h)
- f_correction: Error Correction Factor
- m_material: Required hydrogen storage material mass
- V_material: Required hydrogen storage material volume

### 6. System-Level Energy Density

With the enclosure included:

ED_system,mass = E_required / m_system

ED_system,volume = E_required / V_system

The system mass and volume account for the relevant storage material, fuel cell stack, and enclosure contributions according to the selected calculation mode.

## Installation

### Requirements

- Python 3.12 or later recommended
- Streamlit
- Pandas
- Plotly

### Install Dependencies

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/solid-state-hydrogen-storage-calculator.git

cd solid-state-hydrogen-storage-calculator
```

Install the required packages:

```bash
pip install streamlit pandas plotly
```

### Run the Application

```bash
streamlit run app.py
```

The application will start locally and provide a URL in the terminal, usually:

```text
http://localhost:8501
```

Note: Save the calculator source file as `app.py`, or replace `app.py` in the command with the actual Python filename.

## Project Structure

```text
solid-state-hydrogen-storage-calculator/
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Applications

The calculation framework can support preliminary system-level evaluation for different engineering scenarios, including:

- Unmanned aerial vehicles (UAVs)
- Marine hydrogen power systems
- Robotic platforms
- Portable hydrogen power systems
- Other fuel cell-based applications

The system parameters can be adjusted to reflect different power requirements, endurance targets, fuel cell configurations, and enclosure designs.

## Scope and Limitations

This project is intended as an engineering calculation and preliminary design evaluation tool.

The results depend on the input material properties, model assumptions, fixed conversion parameters, and selected system configurations.

The current model does not constitute a complete simulation of:

- Hydrogen absorption and desorption kinetics
- Transient thermal management
- Detailed heat transfer and reactor behavior
- Structural stress and pressure vessel safety
- Fuel cell dynamic response
- Full vehicle or platform-level performance

The calculated energy density should therefore be interpreted as a model-based estimate rather than experimentally validated system performance.

Further experimental validation, material characterization, and engineering safety assessment are required before practical implementation.

## Contributions

Suggestions, bug reports, and contributions are welcome.

If you would like to improve the material database, calculation models, visualization methods, or application features, feel free to open an issue or submit a pull request.

## License

Please refer to the `LICENSE` file for licensing information.

An explicit open-source license should be selected and included before public release.

---

Developed for the preliminary evaluation and system-level design of solid-state hydrogen storage technologies.


