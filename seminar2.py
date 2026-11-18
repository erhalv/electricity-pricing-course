import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full", layout_file="layouts/seminar2.slides.json")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd

    return mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Seminar 2
    Electricty pricing and emissions

    Erik Hallberg
    """)
    return


@app.cell
def _(pd):
    countries = ["Aland", "Beland", "Celand", "Deland"]

    power_sources = [
        "Solar PV",
        "Wind power",
        "Hydro power",
        "Nuclear power",
        "Biofuels",
        "Coal condensing",
        "Natural gas"
    ]

    # Production capability [TWh/year]
    production = pd.DataFrame(
        [
            [4, 1, 1, 4],
            [40, 14, 21, 19],
            [65, 145, 12, 0],
            [49, 0, 34, 0],
            [12, 0, 18, 10],
            [2, 0, 5, 3],
            [0, 5, 5, 5]
        ],
        index=power_sources,
        columns=countries
    ).assign(
        total = lambda df: df.sum(axis=1)
    )

    # Variable costs [€/MWh] (min, max)
    variable_cost = pd.DataFrame(([
        [0, 0],
        [20, 30],
        [30, 50],
        [90, 110],
        [350, 550],
        [300, 400],
        [450, 600]
    ]), index=power_sources, columns=['min', 'max'] )
    variable_cost['delta'] = variable_cost['max'] - variable_cost['min']

    # CO2 emissions [kg/MWh]
    co2_emissions = pd.Series(
        [0, 0, 0, 0, 0, 1000, 500],
        index=power_sources,
        name="CO2 emissions [kg/MWh]"
    )

    # Electricity consumption [TWh/year]
    consumption = pd.Series(
        [129, 132, 82, 37],
        index=countries
    )

    export = 40 # TWh/year
    return co2_emissions, consumption, export, production, variable_cost


@app.cell
def _(mo, production, variable_cost):
    mo.hstack([
        mo.md(f'Production {mo.as_html(production)}'), 
        mo.md(f'Variable costs {mo.as_html(mo.as_html(variable_cost))}')
    ])
    return


@app.cell
def _(co2_emissions, consumption, mo):
    mo.hstack([
        mo.md(f'CO2 emissions {mo.as_html(co2_emissions)}'), 
        mo.md(f'Consumption (+40 TWh/year export){mo.as_html(mo.as_html(consumption))}')
    ])
    return


@app.cell
def _(production):
    def calc_price(total_demand, base_production, additional_sources, variable_cost):
        x_1 = (
            production.loc[additional_sources, 'total'] * \
            variable_cost.loc[additional_sources].apply(lambda x: x['min']/ (x['max'] - x['min']), axis=1)
        ).sum()


        x_2 = (
            production.loc[additional_sources, 'total'] * \
            variable_cost.loc[additional_sources].apply(lambda x: 1/ (x['max'] - x['min']), axis=1)
        ) .sum()

        return (total_demand - base_production + x_1) /x_2

    return (calc_price,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem a
    Assume that there is no price or limitation on CO2 emissions in the Landic electricity market.
    Calculate the electricity price and the total CO2 emissions per year.

    ### We are looking for
    * Electricty price
    * CO2 emissions


    We assume a price range of (300, 450), and solve:
    $$
    \frac{ \lambda  - \beta_{\text{coal, min}}^C }{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}}+
    \frac{ \lambda  - \beta_{\text{bio, min}}^C }{\beta_{\text{bio, max}}^C - \beta_{\text{bio, min}}^C}  G_{\text{bio, max}}= 11,
    $$
    """)
    return


@app.cell
def _(
    calc_price,
    co2_emissions,
    consumption,
    export,
    mo,
    production,
    variable_cost,
):
    def _():
        total_demand = export + consumption.sum()

        fully_utilized_sources = ['Solar PV', 'Wind power', 'Hydro power', 'Nuclear power']
        base_production = production.loc[fully_utilized_sources, 'total']

        delta = total_demand - base_production.sum()

        price_range = (300, 550)

        additional_sources = ['Biofuels', 'Coal condensing']

        price = calc_price(total_demand, base_production.sum(), additional_sources, variable_cost)

        additional_sources_prodution = production.loc[additional_sources, 'total'] * \
                variable_cost.loc[additional_sources].apply(lambda x: (price-x['min'])/ (x['max'] - x['min']), axis=1)
        total_co2_emissions = (additional_sources_prodution * co2_emissions.loc[additional_sources]).sum() + (base_production * co2_emissions.loc[fully_utilized_sources]).sum()


        return mo.md(fr'''which gives us 

            $$\lambda = {round(price, 3)} \text{{ ¤/MWh}} \\
            \text{{CO2 emissions}} = {round(total_co2_emissions, 3)} \text{{ kton/MWh}} = {round(total_co2_emissions, 3)/1000} \text{{ Mton/MWh}} $$ 
        ''')

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem b
    Assume that Land introduced a tax of 45 ¤/ton for CO2 emissions. Calculate the electricity price
    and the total CO2 emissions per year.

    ### Data
    * CO2 tax = 45 ¤/ton $\Rightarrow$ 0.045 ¤/kg

    ### We are looking for
    * Electricity price
    * CO2 emissions

    We assume a price range in (300, 450) and solve
    $$
    \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \beta^E_\text{coal} \tau) }{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}}+
    \frac{ \lambda  - \beta_{\text{bio, min}}^C }{\beta_{\text{bio, max}}^C - \beta_{\text{bio, min}}^C}  G_{\text{bio, max}}= 11,
    $$
    """)
    return


@app.cell
def _(
    calc_price,
    co2_emissions,
    consumption,
    export,
    mo,
    production,
    variable_cost,
):
    def _():
        tau_co2 = 45/ 1000

        total_demand = export + consumption.sum()

        variable_cost_change = (co2_emissions * tau_co2)
        variable_cost_taxed = variable_cost.add(variable_cost_change, axis=0)

        # same demand 

        fully_utilized_sources = ['Solar PV', 'Wind power', 'Hydro power', 'Nuclear power']
        base_production = production.loc[fully_utilized_sources, 'total'].sum()

        delta = total_demand - base_production

        price_range = (300, 450)

        additional_sources = ['Coal condensing', 'Biofuels']

        price = calc_price(total_demand, base_production, additional_sources, variable_cost_taxed)

        additional_sources_prodution = production.loc[additional_sources, 'total'] * \
                variable_cost_taxed.loc[additional_sources].apply(
                    lambda x: (price-x['min'])/ (x['max'] - x['min']), axis=1
                )
        total_co2_emissions = (additional_sources_prodution * co2_emissions.loc[additional_sources]).sum()

        # return price,variable_cost_change, variable_cost_taxed, price, additional_sources_prodution, total_co2_emissions,tau_co2

        return mo.md(fr'''which gives us 

            $$\lambda = {round(price, 3)} \text{{ ¤/MWh}} \\
            \text{{CO2 emissions}} = {round(total_co2_emissions, 3)} \text{{ kton/MWh}} = {round(total_co2_emissions, 3)/1000} \text{{ Mton/MWh}} $$ 
        ''')

    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem c
    Assume that a feebate system is introduced in the Landic electricity market. The feebate system
    requires producers to pay a fee per ton CO2 emissions and then the sum of all CO2 fees is paid back to
    the involved power plants proportional to their share of the generation. How large must the CO2 fee be
    in order to result in any reduction of the CO2 emissions?

    ### Unkowns
    * price
    * payback
    * CO2 emissions fee
    ### Constraints
    * less CO2
    """)
    return


@app.cell(hide_code=True)
def _(co2_fee, mo):
    mo.md(rf"""
    ### Solve for CO2 emissions fee

    $$
    \beta_{{\text{{gas, min}}}}^C + \beta_{{\text{{gas}}}}^E \varphi - \rho \leq
    \beta_{{\text{{coal, min}}}}^C + \beta_{{\text{{coal}}}}^E \varphi - \rho
    \Rightarrow
    $$

    $$
    \beta_{{\text{{gas, min}}}}^C + \beta_{{\text{{gas}}}}^E \varphi \leq
    \beta_{{\text{{coal, min}}}}^C + \beta_{{\text{{coal}}}}^E \varphi
    \Rightarrow
    $$

    $$
    \varphi \leq \frac{{\beta_{{\text{{coal, min}}}}^C - \beta_{{\text{{gas, min}}}}^C}}{{\beta_{{\text{{gas}}}}^E - \beta_{{\text{{coal}}}}^E}} = {co2_fee} \text{{ ¤/kg}}
    $$
    """)
    return


@app.cell
def _(co2_emissions, variable_cost):
    co2_fee = (variable_cost.loc['Coal condensing']['min'] - variable_cost.loc['Natural gas']['min']) / (co2_emissions.loc['Natural gas'] - co2_emissions.loc['Coal condensing'])
    return (co2_fee,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We assume a price range of (300, 600) and get the following equations
    $$
    \frac{ \lambda  - (\beta_{\text{gas, min}}^C + \beta_{\text{gas}}^E \varphi - \rho)}{\beta_{\text{gas, max}}^C - \beta_{\text{gas, min}}^C} G_{\text{gas, max}} +
    \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \beta_{\text{coal}}^E \varphi - \rho)}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}}+\\
    \frac{ \lambda  - \beta_{\text{bio, min}}^C }{\beta_{\text{bio, max}}^C - \beta_{\text{bio, min}}^C}  G_{\text{bio, max}}= 11,
    $$
    $$
        \varphi \big (\beta_{\text{gas}}^E  \frac{ \lambda  - (\beta_{\text{gas, min}}^C + \beta_{\text{gas}}^E \varphi - \rho)}{\beta_{\text{gas, max}}^C - \beta_{\text{gas, min}}^C} G_{\text{gas, max}}+
        \beta_{\text{coal}}^E \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \beta_{\text{coal}}^E \varphi - \rho)}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C}G_{\text{coal, max}} \big) \\
        =
        \rho \big (\frac{ \lambda  - (\beta_{\text{gas, min}}^C + \beta_{\text{gas}}^E \varphi - \rho)}{\beta_{\text{gas, max}}^C - \beta_{\text{gas, min}}^C} G_{\text{gas, max}}+
        \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \beta_{\text{coal}}^E \varphi - \rho)}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}}\big),
    $$
    """)
    return


@app.cell
def _(
    co2_emissions,
    co2_fee,
    consumption,
    export,
    pd,
    production,
    variable_cost,
):
    import sympy as sp

    total_demand = export + consumption.sum()

    fully_utilized_sources = ['Solar PV', 'Wind power', 'Hydro power', 'Nuclear power']
    base_production = production.loc[fully_utilized_sources, 'total'].sum()

    delta = total_demand - base_production

    df = pd.merge(left=production['total'], right=variable_cost[['min', 'max']], right_index=True, left_index=True).merge(right=co2_emissions, left_index=True, right_index=True)

    data = df.values[4:]
    _x, _y = sp.symbols('x y')

    sym_eq1 = sp.Eq (
        ((_x - (data[0, 1] )) / (data[0, 2] - data[0, 1])) * data[0, 0] +
        ((_x - (data[1, 1] + data[1, 3] * co2_fee  - _y  )) / (data[1, 2] - data[1, 1])) * data[1, 0] +
        ((_x - (data[2, 1] + data[2, 3] * co2_fee  - _y )) / (data[2, 2] - data[2, 1])) * data[2, 0], 
        delta
    )

    sym_eq2 = sp.Eq (
        ((_x - (data[1, 1] + data[1, 3] * co2_fee  - _y  )) / (data[1, 2] - data[1, 1])) * data[1, 0] * data[1, 3] * co2_fee+
        ((_x - (data[2, 1] + data[2, 3] * co2_fee  - _y )) / (data[2, 2] - data[2, 1])) * data[2, 0] * data[2, 3]* co2_fee,
        ((_x - (data[1, 1] + data[1, 3] * co2_fee  - _y  )) / (data[1, 2] - data[1, 1])) * data[1, 0] * _y +
        ((_x - (data[2, 1] + data[2, 3] * co2_fee  - _y )) / (data[2, 2] - data[2, 1])) * data[2, 0] * _y, 
    )

    solutions = sp.solve([sym_eq1, sym_eq2], [_x, _y])
    # solutions
    return data, solutions, sp, total_demand


@app.cell(hide_code=True)
def _(co2_fee, mo, solutions):
    mo.md(rf"""
    By solving the equations we get two candidates:

    Solution 1: 
    $$
     \lambda_1 = {round(float(solutions[0][0]), 3)} \text{{ ¤/MWh}}\\
     \rho_1 = {round(float(solutions[0][1]), 3)} \text{{ ¤/MWh}}\\
     \varphi = {co2_fee}\text{{ ¤/kg}} \\
    \text{{CO2 emissions}} = 2250 \text{{ kton/MWh}}
    $$

    Solution 2: 
    $$
     \lambda_2 = {round(float(solutions[1][0]), 3)} \text{{ ¤/MWh}} \\
     \rho_2 = {round(float(solutions[1][1]), 3)} \text{{ ¤/MWh}}\\
     \varphi = {co2_fee}\text{{ ¤/kg}} \\
     \text{{CO2 emissions}} = 0 \text{{ kton/MWh}}
    $$
    """)
    return


@app.cell
def _(co2_fee, data, solutions):
    for sol in solutions:
        x1=sol[0] 
        y1 =sol[1] 


        print('+++ Price', x1, 'CO2 fee', co2_fee, 'Payback', y1 , '+++')


        print(
            "Generation",
            ((x1 - (data[0, 1] )) / (data[0, 2] - data[0, 1])) * data[0, 0] ,
            ((x1 - (data[1, 1] + data[1, 3] * co2_fee  - y1  )) / (data[1, 2] - data[1, 1])) * data[1, 0] ,
            ((x1 - (data[2, 1] + data[2, 3] * co2_fee  - y1 )) / (data[2, 2] - data[2, 1])) * data[2, 0]

        )

        print(
            "Payout balance",
            ((x1 - (data[1, 1] + data[1, 3] * co2_fee  - y1  )) / (data[1, 2] - data[1, 1])) * data[1, 0] * data[1, 3] * co2_fee+
            ((x1 - (data[2, 1] + data[2, 3] * co2_fee  - y1 )) / (data[2, 2] - data[2, 1])) * data[2, 0] * data[2, 3]* co2_fee,
            ((x1 - (data[1, 1] + data[1, 3] * co2_fee  - y1  )) / (data[1, 2] - data[1, 1])) * data[1, 0] * y1 +
            ((x1 - (data[2, 1] + data[2, 3] * co2_fee  - y1 )) / (data[2, 2] - data[2, 1])) * data[2, 0] * y1,   
        )
        print(
            "Emissions",
            ((x1 - (data[1, 1] + data[1, 3] * co2_fee  - y1  )) / (data[1, 2] - data[1, 1])) * data[1, 0] * data[1, 3] +
            ((x1 - (data[2, 1] + data[2, 3] * co2_fee  - y1 )) / (data[2, 2] - data[2, 1])) * data[2, 0] * data[2, 3]  

        )
    return


@app.cell
def _(co2_emissions, co2_fee, solutions, variable_cost):
    (_price, _payback) = solutions[0]


    variable_cost_change = (co2_emissions * co2_fee)
    variable_cost_taxed = variable_cost.add(variable_cost_change, axis=0)
    variable_cost_taxed = variable_cost_taxed.add( - float(_payback) * (co2_emissions > 0).values , axis=0)
    # variable_cost_taxed
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem d
    Assume that tradable green certificates are introduces in the Landic electricity market. Green
    certificates are issued for electricity generation from solar PV, wind power and biofuels. The penalty fee
    for missing certificates is 1 000 ¤/MWh. How high must the quota for green certificates be in order to
    reduce the emissions to 5 Mton/year? What will the electricity price and price of green certificates
    become with this quota

    ### Data
    * Penalty fee = 1000 EUR/MWh
    * Total emissions = 5 Mton / year
    * Participating sources = Solar PV, wind power and biofuels

    ### We are looking for
    * Quota for green certificates
    * Electricity price
    * Green certificate price
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Assume price between (300, 450) EUR/MWh
    $$
        G_{\text{solar, max}} + G_{\text{wind, max}} + G_{\text{hydro, max}} + G_{\text{nuclear, max}} +
        G_{\text{bio}} + G_{\text{coal}} + G_{\text{gas}} = 420
    $$

    $$
        G_{\text{solar, max}} + G_{\text{wind, max}} +  G_{\text{bio}} = 420x,
    $$

    $$
      \beta_{\text{coal}}^E  \frac{ \lambda  - \beta_{\text{coal, min}}^C}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^c} G_{\text{coal, max}} = 5000
    $$

    where $x$ green certificate quota.
    """)
    return


@app.cell
def _(co2_emissions, mo, production, sp, variable_cost):
    green_power_sources = ['Solar PV', 'Wind power', 'Biofuels']


    _G_b, _x = sp.symbols('G_b x')

    _price = (5000/ co2_emissions.loc['Coal condensing']) * (variable_cost.loc['Coal condensing', 'delta'])  * 1/ production.loc['Coal condensing', 'total'] + variable_cost.loc['Coal condensing', 'min']

    _coal_production = (_price - variable_cost.loc['Coal condensing', 'min'])/(variable_cost.loc['Coal condensing', 'delta']) * production.loc['Coal condensing', 'total']


    total_generation_eq = sp.Eq( 
        production.loc['Solar PV', 'total'] + production.loc['Wind power', 'total']  + production.loc['Nuclear power', 'total']  + production.loc['Hydro power', 'total'] + \
        _G_b + _coal_production, 
       420
    )

    green_certificate_eq = sp.Eq( 
        production.loc['Solar PV', 'total'] + production.loc['Wind power', 'total'] + _G_b, 
       420 * _x
    )

    _solutions = sp.solve([total_generation_eq, green_certificate_eq])


    marginal_cost_last_bio = float(variable_cost.loc['Biofuels', 'min'] + (_solutions[_G_b] / production.loc['Biofuels', 'total']) * variable_cost.loc['Biofuels', 'delta'])

    green_certificate_price = marginal_cost_last_bio - _price

    _solutions[_x],_price,marginal_cost_last_bio, green_certificate_price

    mo.md(rf"""
    Solving the equations gives us
    $$
    x = {round(float(_solutions[_x]), 4)} = {round(float(_solutions[_x]) * 100, 3) } \% \\
    \lambda = {_price} \text{{ ¤/MWh}}\\
    \text{{Certificate price}} = {green_certificate_price} \text{{ ¤/MWh}}
    $$

    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem e
    Assume that electricity disclosure is introduced in the Landic electricity market. The demand
    for renewable electricity (i.e., solar, wind, hydro and biofuels) is 333 TWh/year and these consumers are
    willing to pay up to 100 ¤/MWh extra for renewable electricity (compared to the price of grey electricity). Calculate the electricity price for renewable electricity and grey electricity respectively as well as
    the total CO2 emissions per year.

    ### Data
    * Renewable demand = 333 TWh/year
    * $\Delta$Premium = 100 EUR/MWh

    ### We are looking for
    * Renewable electricity price
    * Grey electricity price
    * Total CO2 emissions per year
    """)
    return


@app.cell
def _(co2_emissions, production, total_demand, variable_cost):
    renewable_power_sources = ['Solar PV','Wind power', 'Hydro power', 'Biofuels']

    renewable_demand = 333

    # assumed price (300, 400)
    price_grey = (total_demand - renewable_demand - production.loc['Nuclear power', 'total']) * \
        variable_cost.loc['Coal condensing', 'delta'] * 1/(production.loc['Coal condensing', 'total']) + variable_cost.loc['Coal condensing', 'min'] 

    max_renewable_power_sources = ['Solar PV','Wind power', 'Hydro power']

    #  assumed price range (350 440)

    price_renewables = (renewable_demand - production.loc[max_renewable_power_sources, 'total'].sum()) * \
         variable_cost.loc['Biofuels', 'delta'] * 1/(production.loc['Biofuels', 'total']) + variable_cost.loc['Biofuels', 'min'] 

    _total_emissions = co2_emissions.loc['Coal condensing'] * production.loc['Coal condensing', 'total'] * (price_grey - variable_cost.loc['Coal condensing', 'min'] )/ (variable_cost.loc['Coal condensing', 'delta']) 


    price_renewables, price_grey, price_renewables - price_grey, _total_emissions, total_demand - renewable_demand , production.loc['Nuclear power', 'total'], renewable_demand ,production.loc[max_renewable_power_sources, 'total'].sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let $\lambda_g$ be the grey electricity price, assume a price range of (300, 400) => Demand = 420 - 333 - 83 =4 TWh/year
    $$
    \frac{ \lambda_g  - \beta_{\text{coal, min}}^C }{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}} = 4 \text{ TWh/year},
    $$
    solving this gives us
    $$
        \lambda_g = 340\text{{ ¤/MWh}}.
    $$
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Let $\lambda_r$ be the renewable electricity price, assume a price range of (350, $\lambda_g + 100 = 440$) => Demand = 333 - 326 = 7 TWh/year

    $$
    \frac{ \lambda_r  - \beta_{\text{bio, min}}^C }{\beta_{\text{bio, max}}^C - \beta_{\text{bio, min}}^C} G_{\text{bio, max}} = 7\text{ TWh/year}
    $$

    solving this gives us
    $$
        \lambda_r = 385.\text{{ ¤/MWh}}
    $$
    And finally the total emisssions per year in this case are
    $$
        \text{CO2 emissions} = 4 \text{ Mton/year}
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Problem f
    Assume that tradable emission rights are introduced in the Landic electricity market.
    The penalty fee for emitting 1 ton CO2 without holding an emission right is set to 1 000 ¤/ton.
    The number of emission rights is set to 3.5 Mton/year. Calculate the electricity price and the price of emission rights.

    ### Data
    * Penalty fee = 1000 ¤/ton
    * Number of emission rights = 3.5 Mton/year

    ### We are looking for
    * Electricity price
    * Price of the emission rights
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Assume that the emissions are equal to the cap $\Rightarrow \xi < 1000$, further assume a price range of (300, 450).

    $$
    \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \xi )}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}}+
    \frac{ \lambda  - \beta_{\text{bio, min}}^C }{\beta_{\text{bio, max}}^C - \beta_{\text{bio, min}}^C}  G_{\text{bio, max}}= 11
    $$
    $$
        \beta_{\text{coal}}^E \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \xi )}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C}G_{\text{coal, max}}
        = 3500
    $$
    """)
    return


@app.cell
def _(co2_emissions, mo, production, sp, variable_cost):
    emission_cap = 3500

    _lambda, _xi = sp.symbols('\\lambda \\xi')

    _total_generation_eq = sp.Eq(
        # production.loc['Natural gas','total']*(_lambda - (variable_cost.loc['Natural gas', 'min'] + _xi)) / variable_cost.loc['Natural gas', 'delta'] +\
        production.loc['Coal condensing','total'] *(_lambda - (variable_cost.loc['Coal condensing', 'min'] + _xi)) / variable_cost.loc['Coal condensing', 'delta'] +\
        production.loc['Biofuels','total'] * (_lambda - (variable_cost.loc['Biofuels', 'min'])) / variable_cost.loc['Biofuels', 'delta'],
        11
    )

    _emission_balance = sp.Eq(
        # co2_emissions.loc['Natural gas']*production.loc['Natural gas','total']*(_lambda - (variable_cost.loc['Natural gas', 'min'] + _xi)) / variable_cost.loc['Natural gas', 'delta'] +\
        co2_emissions.loc['Coal condensing'] * production.loc['Coal condensing','total'] *(_lambda - (variable_cost.loc['Coal condensing', 'min'] + _xi)) / variable_cost.loc['Coal condensing', 'delta'],
       emission_cap
    )
    _solutions = sp.solve([_total_generation_eq, _emission_balance])

    float(_solutions[_xi]),float(_solutions[_lambda])

    mo.md(fr'''Solving the equations gives us

    $$
        \lambda = {round(float(_solutions[_lambda]),3)} \text{{ ¤/MWh}} \\
        \xi = {round(float(_solutions[_xi]),3)} \text{{ ¤/MWh}}.\\
    $$
    ''')
    return (emission_cap,)


@app.cell
def _():
    _xi= 52.5 
    _lambda = 387.5

    # production.loc['Coal condensing','total'] *(_lambda - (variable_cost.loc['Coal condensing', 'min'] + _xi)) / variable_cost.loc['Coal condensing', 'delta'],
    # production.loc['Biofuels','total'] * (_lambda - (variable_cost.loc['Biofuels', 'min'])) / variable_cost.loc['Biofuels', 'delta'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem g
    Suggest another method besides tradable emission rights that can reduce the emissions from
    the Landic electricity market to 3.5 Mton/year. Calculate the electricity price and any other relevant
    parameters for your market design.

    ### Suggestion: CO2-tax => we need to solve:
    Price assumption (300, 450)
    $$
    \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \beta_{\text{coal}}^E \tau)}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}}+
    \frac{ \lambda  - \beta_{\text{bio, min}}^C }{\beta_{\text{bio, max}}^C - \beta_{\text{bio, min}}^C}  G_{\text{bio, max}}= 11
    $$

    $$
     \beta_{\text{coal}}^E \frac{ \lambda  - (\beta_{\text{coal, min}}^C + \beta_{\text{coal}}^E \tau)}{\beta_{\text{coal, max}}^C - \beta_{\text{coal, min}}^C} G_{\text{coal, max}}
    = 3500
    $$
    """)
    return


@app.cell
def _(co2_emissions, emission_cap, mo, production, sp, variable_cost):

    _lambda, _xi = sp.symbols('\\lambda \\xi')

    _total_generation_eq = sp.Eq(
        # production.loc['Natural gas','total']*(_lambda - (variable_cost.loc['Natural gas', 'min'] + co2_emissions.loc['Natural gas']*_xi)) / variable_cost.loc['Natural gas', 'delta'] +\
        production.loc['Coal condensing','total'] *(_lambda - (variable_cost.loc['Coal condensing', 'min'] + co2_emissions.loc['Coal condensing']*_xi)) / variable_cost.loc['Coal condensing', 'delta'] +\
        production.loc['Biofuels','total'] * (_lambda - (variable_cost.loc['Biofuels', 'min'])) / variable_cost.loc['Biofuels', 'delta'],
        11
    )

    _emission_balance = sp.Eq(
        # co2_emissions.loc['Natural gas']*production.loc['Natural gas','total']*(_lambda - (variable_cost.loc['Natural gas', 'min'] +co2_emissions.loc['Natural gas']*_xi)) / variable_cost.loc['Natural gas', 'delta'] +\
        co2_emissions.loc['Coal condensing'] * production.loc['Coal condensing','total'] *(_lambda - (variable_cost.loc['Coal condensing', 'min'] + co2_emissions.loc['Coal condensing']*_xi)) / variable_cost.loc['Coal condensing', 'delta'],
       emission_cap 
    )

    _solutions = sp.solve([_total_generation_eq, _emission_balance])

    float(_solutions[_xi]),float(_solutions[_lambda])

    mo.md(fr'''$$\lambda= {float(_solutions[_lambda])} \text{{ ¤/MWh}}$$ 
    $$\tau= {float(_solutions[_xi])} \text{{ ¤/kg}} $$''')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem h
    In this question you will need to use the excel workbook ```Nordic price``` to analyse the Nordic
    electricity market. The model itself is found on the first sheet (“Overview”). Additional data, sources
    and calculations are found on the other two sheets. For this problem, you will however only need to edit
    the blue fields in the overview. The model will use the simple price model explained in the lectures on
    electricity pricing for a rough estimate of the Nordic electricity price.
    The default data in the model is for 2019, which was a fairly average year in terms of hydro inflow.
    Which electricity prices would be obtained if 2019 had been a wet year (75 TWh hydro power in Swe-
    den, 140 TWh in Norway and 16 TWh in Finland) or a dry year (55 TWh hydro power in Sweden,
    110 TWh in Norway and 12 TWh in Finland). Compare the impact of hydro inflow on electricity prices
    to the impact if the fifth Finnish nuclear power plant Olkiluoto 3 had been operational in 2019? The
    annual generation from Olkiluoto 3 is expected to be between 12 and 13 TWh/year.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem h
    ### Price if it was a wet year
    * Hydro power: Sweden 75 TWh, Norway 140 TWh and Finland 16 TWh
    * The model gives => 317.10 kr /MWh

    ### Price if it was a dry year
    * Hydro power: Sweden 55 TWh, Norway 110 TWh and Finland 12 TWh
    * The model gives => 472.92 kr /MWh


    ### Impact of Hydro inflow if Olkiluoto 3 had been operational in 2019
    * Olkiluto 3: 12 - 13 TWh/ year => we set production to 12.5 TWh/year
    * Wet year price => 279.02 kr/MWh
    * Dry year price => 455.30 kr/MWh
    """)
    return


@app.cell(hide_code=True)
def _(mo, table3):
    mo.md(rf"""
    ## Problem i
    Table 3 shows data for hydro power generation, wind power generation and demand in the Nordic countries 
    in 2020. Assume that all other data are the same as for 2019 and use the Nordic price
    model to estimate the electricity price. Compare the result to the average system price in the Nord Pool
    Elspot market 2020, which was 114.31 SEK/MWh. Explain the difference between the result of the
    model and the actual average price.

    Table 3:
    {mo.as_html(table3)}
    """)
    return


@app.cell(hide_code=True)
def _(np, pd):
    table3 = pd.DataFrame({
        "Sweden":  [72, 28, 127],
        "Norway":  [142, 10, 125],
        "Finland": [16, 8, 81],
        "Denmark": [np.nan, 17, 33]
    }, index=[
        "Hydro power generation [TWh]",
        "Wind power generation [TWh]",
        "Electricity consumption [TWh]"
    ])
    return (table3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem i
    By using the values in table 3 we get a price of 97.25 kr /MWh. Why do we get a difference?

    * The model is based on the simple price model => assumptions
        * Perfect competition, perfect information etc..
    * Does not take into account the swedish electricty zones.
    * 2019 was a year of low prices but a also a year of big differences between the different zone [1]
    * Trade and export data is from 2019

    [1] "Rekordlåga elpriser sammanfattar elåret 2020", Energiföretagen https://www.mynewsdesk.com/se/energiforetagen/pressreleases/rekordlaaga-elpriser-sammanfattar-elaaret-2020-3062339
    """)
    return


if __name__ == "__main__":
    app.run()
