import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd

    return (pd,)


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

    From the figure we get

    $$
     \tilde{F_{\bar{W}}}(x) = \begin{cases}
         1 + \frac{1 - 0.4}{0-400}x & 0 \leq x \leq 400 \\
         0.8 + \frac{0.4 - 0.1}{400 - 700}x &  400 < x \leq 400 \\
         \frac{1}{3} + \frac{0.1 - 0}{700 - 1000}x &  700 < x \leq 1000
     \end{cases}
    $$
    The inverse is

    $$
     \tilde{F_{\bar{W}}}^{-1}(u)
        = \begin{cases}
         1000-3000u & 0 \leq u \leq 1 \\
         800 - 1000u &  0.1 < u \leq 0.4 \\
         \frac{2000}{3} - \frac{2000}{3}u &  0.4 < x \leq 1
     \end{cases}
     $$
    """)
    return


@app.cell
def _(pd, scenarios):
    def inverse_duration_wind(u):
        if 0 <= u and u <= 0.1:
            return 1000 -3000 * u
        elif 0.1 <= u and u <= 0.4:
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
          \hat{G}_g & 0 < u < p_g \\
            0 &  p_g \leq u \leq 1
     \end{cases}
     $$
    """)
    return


@app.cell
def _(data, scenarios, thermal_power_plants):
    def inverse_duration_thermal(u, p_g, G_hat):
        if 0 <= u and u < p_g:
           return G_hat
        else:
            return 0


    available_generation_capacity = []

    cols = scenarios.iloc[:, 1:11].columns

    data[cols] = None

    for j,scenario in scenarios.iloc[:, 1:11].iterrows():
        vals = []
        for i, u in enumerate(scenario):  
            G_hat ,p_g = thermal_power_plants.loc[i, ["Installed capacity [MW]", "Availability [%]"]] 
            p_g /= 100
        
            vals.append(inverse_duration_thermal(u, p_g, G_hat))
        data.loc[j, cols] = vals 

    data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem c
    What are the inverse of the duration curves (or distribution functions if that would be preferable) for the total load in Maa? Use the inverse function and the random numbers in table 5 to generate
    values of the total load for ten scenarios.

    ![alt](public/load_curve_1.png)

    Form the figure we get
    """)
    return


if __name__ == "__main__":
    app.run()
