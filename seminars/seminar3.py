import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", layout_file="layouts/seminar3.slides.json")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(mo):
    mo.md(r"""
    # Seminar 3
    Erik Hallberg


    The power system in Maa is divided in two parts: North and South. The generation in Maa is from wind
    power (only in southern Maa) and ten thermal power plants. The figures below shows the duration
    curves of the total load in Maa (left panel) and the duration curve of the available wind power genera-
    tion (right panel). Data for the thermal power plants are given in table 4. The transmission capacity
    between northern and southern Maa is 600 MW in either direction. Transmission and distribution
    losses can be neglected. The distribution of the total load between the two areas is computed using a
    coefficient C, which is uniformly distributed between 0.2 and 0.3:
    """)
    return


@app.cell
def _(pd):
    thermal_power_plants = pd.DataFrame({
        "Plant": range(1, 11),
        "Installed capacity [MW]": [900, 800, 750, 600, 500, 400, 500, 300, 250, 200],
        "Availability [%]": [95] * 10,
        "Variable cost [x/MWh]": [200, 220, 240, 250, 260, 280, 320, 350, 380, 420],
        "Area": ["South", "North", "North", "North", "South",
                 "North", "North", "North", "South", "North"]
    })


    scenarios = pd.DataFrame({
        "Scenario": range(1, 11),
        "Wind power": [0.308, 0.519, 0.768, 0.789, 0.871, 0.188, 0.270, 0.496, 0.739, 0.195],
        "Plant 1":  [0.180, 0.539, 0.283, 0.761, 0.270, 0.294, 0.962, 0.913, 0.568, 0.485],
        "Plant 2":  [0.654, 0.537, 0.996, 0.142, 0.975, 0.620, 0.720, 0.295, 0.600, 0.751],
        "Plant 3":  [0.641, 0.923, 0.889, 0.645, 0.296, 0.683, 0.277, 0.126, 0.570, 0.409],
        "Plant 4":  [0.560, 0.854, 0.097, 0.354, 0.974, 0.922, 0.969, 0.051, 0.884, 0.770],
        "Plant 5":  [0.240, 0.104, 0.186, 0.753, 0.953, 0.791, 0.187, 0.512, 0.081, 0.523],
        "Plant 6":  [0.134, 0.199, 0.108, 0.633, 0.952, 0.526, 0.337, 0.508, 0.990, 0.633],
        "Plant 7":  [0.365, 0.976, 0.782, 0.039, 0.985, 0.352, 0.278, 0.314, 0.640, 0.487],
        "Plant 8":  [0.271, 0.946, 0.410, 0.268, 0.863, 0.461, 0.701, 0.454, 0.745, 0.062],
        "Plant 9":  [0.067, 0.296, 0.612, 0.013, 0.382, 0.680, 0.914, 0.257, 0.104, 0.834],
        "Plant 10": [0.556, 0.005, 0.365, 0.769, 0.276, 0.292, 0.085, 0.188, 0.263, 0.645],
        "Total load": [0.227, 0.514, 0.695, 0.878, 0.807, 0.901, 0.857, 0.438, 0.589, 0.785],
        "Load distribution coefficient": [0.554, 0.621, 0.574, 0.736, 0.988, 0.133, 0.113, 0.702, 0.058, 0.560]
    }).set_index("Scenario") # table 5

    thermal_power_plants, scenarios 
    return scenarios, thermal_power_plants


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem a
    What are the inverse of the duration curves (or distribution functions if that would be preferable) for the wind power generation capacity in Maa? Use the inverse function and the random numbers
    in table 5 to generate values of the wind power generation capacity for ten scenarios.

    ![alt](public/image.png)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    From the figure we get

    $$
     \tilde{F_{\bar{W}}}(x) = \begin{cases}
         1 + \frac{1 - 0.4}{0-400}x & 0 \leq x \leq 400 \\
         0.8 + \frac{0.4 - 0.1}{400 - 700}x &  400 < x \leq 700 \\
         \frac{1}{3} + \frac{0.1 - 0}{700 - 1000}x &  700 < x \leq 1000
     \end{cases}
    $$
    The inverse is

    $$
     \tilde{F_{\bar{W}}}^{-1}(u)
        = \begin{cases}
         1000-3000u & 0 \leq u \leq 0.1 \\
         800 - 1000u &  0.1 < u \leq 0.4 \\
         \frac{2000}{3} - \frac{2000}{3}u &  0.4 < u \leq 1
     \end{cases}
     $$
    """)
    return


@app.cell
def _(pd, scenarios):
    def inverse_duration_wind(u):
        if 0 <= u and u <= 0.1:
            return 1000 -3000 * u
        elif 0.1 < u and u <= 0.4:
            return 800 - 1000 * u
        else:
            return 2000/3 - 2000/3 * u

    data = pd.DataFrame(columns=['Scenario' ]).set_index('Scenario')

    data['Wind power generation'] = scenarios['Wind power'].apply(inverse_duration_wind)

    data
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem b

    What are the inverse of the duration curves (or distribution functions if that would be preferable) for the thermal power generation capacity in Maa? Use the inverse function and the random numbers in table 5 to generate values of the available generation capacity in each thermal power plant for
    ten scenarios.


    $$
     \tilde{F}_{T}(x) = \begin{cases}
         1 & x < 0 \\
         p_g & 0 \leq x < \hat{G}_g \\
         0 &  \hat{G}_g \leq x
     \end{cases}
    $$
    The inverse is

    $$
     \tilde{F}_T^{-1}(u)
        = \begin{cases}
          \hat{G}_g & 0 \leq u < p_g \\
            0 &  p_g \leq u \leq 1
     \end{cases}
     $$
    """)
    return


@app.cell
def _(data, scenarios, thermal_power_plants):
    def inverse_duration_thermal(u, p_g, G_hat):
        if 0 <= u and u < p_g:
           return float(G_hat)
        else:
            return 0.0


    available_generation_capacity = []

    cols = scenarios.iloc[:, 1:11].columns

    data[cols] = None

    for _j,_scenario in scenarios.iloc[:, 1:11].iterrows():
        vals = []
        for _i, u in enumerate(_scenario):  
            G_hat ,p_g = thermal_power_plants.loc[_i, ["Installed capacity [MW]", "Availability [%]"]] 
            p_g /= 100

            vals.append(inverse_duration_thermal(u, p_g, G_hat))
        data.loc[_j, cols] = vals 

    data
    return (cols,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem c
    What are the inverse of the duration curves (or distribution functions if that would be preferable) for the total load in Maa? Use the inverse function and the random numbers in table 5 to generate
    values of the total load for ten scenarios.

    ![alt](public/load_curve_1.png)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Form the figure we get
    $$
    \tilde{F}_{\text{Dtot}}(x) = \begin{cases}
         1 & 0 < x \leq 2000 \\
         2.2 - 0.0006x & 2000 \leq x < 3500 \\
         0.45 - 0.0001x & 3500 < x < 4500
     \end{cases}
    $$

    The inverse is

    $$
    \tilde{F}_{\text{Dtot}}^{-1}(u) = \begin{cases}
         4500 - 10000u & 0 \leq u \leq 0.1 \\
         2000 + \frac{1500}{0.9}(1-u)& 0.1 < u \leq 1
     \end{cases}
    $$
    """)
    return


@app.cell
def _(data, scenarios):
    def inverse_load(u):
        if 0 <= u <= 0.1:
            return 4500 - 10_000 * u
        else:
            return 2000 + (1500 / 0.9) * (1 - u)


    data['Total load'] = scenarios['Total load'].apply(inverse_load)

    data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem d
    What are the inverse of the duration curves (or distribution functions if that would be preferable) for the load distribution coefficient? Use the inverse function and the random numbers in table 5 to
    generate values of the coefficient for ten scenarios.

    We have $C \sim U(0.2,0.3) \Rightarrow \tilde{F}^{-1}_C(u) = 0.3 - (0.3 - 0.2)u, \text{ } u \in [0,1]$
    """)
    return


@app.cell
def _(data, scenarios):
    def inverse_duration_load_coefficient(u):
        return 0.3 - (0.3 - 0.2) * u

    data['Load distribution coefficient'] = scenarios['Load distribution coefficient'].apply(inverse_duration_load_coefficient)

    data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem e
    Use the data from questions a–d to create ten scenarios for a Monte Carlo simulation of Maa.
    Describe the principle how TOC and LOLO are computed for one scenario and present the results of the
    ten scenarios in a table that shows the generation in each power plant, the transmission between the
    areas and the results for TOC and LOLO. Moreover, compute the estimates of ETOC and LOLP for this
    simulation.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### How TOC and LOLO are computed for scenario
    1. Compute area load/demand
        * $D^\text{{South}} = C D^\text{{tot}}$ MW
        * $D^\text{{North}} = (1-C) D^\text{{tot}}$  MW
    2. Allocate wind
       * Wind generation = min($D^\text{{South}}$, available wind)
       * Decrease the south demand with wind generation
       * If wind export is possible: (`south demand = 0 and available wind and transmission is ok`)
           * Increase wind generation by: min($D^\text{{South}}$, available wind )
           * Decrease north demand with same amount
           * Increase transmission (positive for south export, negative for north export)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    3. Iterate thermal power plants starting with the cheapest
       * Power plant generation = min($D^\text{{Area}}$, available capacity)
       * Decrease the area demand with generation
       * If export is possible: (`area demand = 0 and available capacity and transmission is ok`)
           * Increase power plant generation by: min($D^\text{{Export area}}$, available capacity )
           * Decrease export area demand with same amount
           * Increase transmission (positive for south export, negative for north export)
       * Increase TOC by: variable cost $\times$ total generation
    4. If south demand > 0 or north demand > 0 after the steps above we get load shedding
        * LOLO = 1
    """)
    return


@app.cell
def _(cols, data, pd, thermal_power_plants):

    def simulation(max_transmission):
        # # Model parameters
        # max_transmission = 600 # MW
    
        output = pd.DataFrame(columns=['Scenario', 'TOC', 'ENS', 'Transmission']).set_index('Scenario')
    
        output[cols] = None
    
        for _i,_scenario in data.iterrows():
    
            print(f"Scenario = {_i}")
    
            C = _scenario['Load distribution coefficient']
            total_load = _scenario['Total load']
    
            # load in each area
            north_load = (1-C) * total_load
            south_load = C * total_load
        
            output.loc[_i, 'North load'] = north_load
            output.loc[_i, 'South load'] = south_load

            south_generation = 0
            north_generation = 0
            TOC = 0
            transmission = 0

            # Wind (in the south)
            production = min(south_load, _scenario['Wind power generation'])
            south_load -= production
            TOC += 0  

            # we can export
            export_production = 0
            if south_load == 0 and _scenario['Wind power generation'] - production > 0 and abs(transmission) < max_transmission:
                export_production = min(north_load, _scenario['Wind power generation'] - production, max_transmission - abs(transmission))
                north_load -= export_production
                transmission += export_production

            wind_generation = production + export_production
            south_generation += wind_generation
        
            _vals = []
            for _j, power_plant_production in enumerate(_scenario[1:11]):  
    
                area, cost = thermal_power_plants.loc[_j, ["Area", "Variable cost [x/MWh]"]]
    
                if area == "North":
                
                    production = min(north_load, power_plant_production)
                
                    north_load -= production
            
                    export_production = 0
                    if north_load == 0 and power_plant_production - production > 0 and abs(transmission) < max_transmission and south_load > 0:
                        print('we are exporting from north to south')
                    
                        export_production = min(south_load, power_plant_production - production, max_transmission - abs(transmission))
                        south_load -= export_production
                        transmission-= export_production
                    

                    TOC += (production + export_production ) * cost
                    _vals.append(production + export_production)
                    north_generation += production + export_production
                else:
    
                    production = min(south_load, power_plant_production)

                    south_load -= production
            
                    export_production = 0
                
                    if south_load == 0 and power_plant_production - production > 0 and abs(transmission) < max_transmission and north_load > 0:
                    
                        print('we are exporting from south to north')
                        export_production = min(north_load, power_plant_production - production, max_transmission - abs(transmission))
                        north_load -= export_production
                        transmission += export_production
            
                    TOC += (production + export_production ) * cost
                    _vals.append(production + export_production)
                    south_generation += production + export_production
        
            output.loc[_i, cols] = _vals 
            output.loc[_i, 'TOC'] = TOC
        
            output.loc[_i, 'Wind generation'] = wind_generation
            output.loc[_i, 'South generation'] = south_generation
            output.loc[_i, 'North generation'] = north_generation

            LOLO = (north_load > 0) or (south_load > 0)
        
            output.loc[_i, 'LOLO'] = LOLO
            output.loc[_i, 'ENS'] = north_load + south_load 
            output.loc[_i, 'Transmission'] = transmission 
        return output

    output1 = simulation(max_transmission= 600)
    return output1, simulation


@app.cell
def _(ELOLO1, ETOC1, mo, output1):
    mo.md(f"""
    ###Results from simulation 1 (max transmission = 600 MW): {mo.as_html(output1)} 

    ### ETOC = {round(ETOC1, 3)} ¤/h
    ### ELOLO = {ELOLO1 * 100} %
    """)
    return


@app.cell
def _(output1):
    ETOC1 = output1['TOC'].mean()
    ELOLO1 = output1['LOLO'].mean()
    return ELOLO1, ETOC1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem f
    Assume that the transmission capacity between the two areas is increased to 900 MW. Consider
    the same 10 scenarios as in question e and use correlated sampling to estimate how much ETOC and
    LOLP will decrease
    """)
    return


@app.cell
def _(simulation):
    output2 = simulation(max_transmission=900)
    return (output2,)


@app.cell
def _(output2):
    ETOC2 = output2['TOC'].mean()
    ELOLO2 = output2['LOLO'].mean()

    return ELOLO2, ETOC2


@app.cell
def _(output1, output2):
    delta_etoc = (output2['TOC'] - output1['TOC']).mean()
    delta_elolo = (output2['LOLO'] - output1['LOLO']).mean()
    return delta_elolo, delta_etoc


@app.cell
def _(ELOLO2, ETOC2, delta_elolo, delta_etoc, mo, output2):
    mo.md(f"""
    ###Results from simulation 2 (max transmission = 900 MW): {mo.as_html(output2)} 

    ### ETOC = {round(ETOC2, 3)} => $\Delta$ ETOC = {round(delta_etoc, 3)} ¤/h
    ### ELOLO = {ELOLO2 * 100} % => $\Delta$ ELOLO = {delta_elolo * 100} %
    """)
    return


if __name__ == "__main__":
    app.run()
