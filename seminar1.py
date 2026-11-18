import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", layout_file="layouts/seminar1.slides.json")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Seminar 1

    ## input
    * $\Delta f_o= {} \text{ Hz}$
    * $\Delta f_r= 0.2 \text{ Hz}$
    *

    ## Problems
    """)
    return


@app.cell(hide_code=True)
def _(pd):
    data = pd.DataFrame(
        [
            ["Berg",     "North", 150, 160, 145,  55],
            ["By",       "South", 200, 190,  80,  60],
            ["Ede",      "North", 250, 230, 105,  50],
            ["Fallet",   "North", 250, 230,  95,  70],
            ["Fjärd",    "North", 250, 150, 125,  45],
            ["Flislinge", "South", 200, 350, 230, 100],
            ["Forsen",   "North", 200, 220, 100,  75],
            ["Hamn",     "North", 200, 260, 160,  80],
            ["Sele",     "North", 150, 180,  75,  60],
            ["Språnget", "North", 300, 500, 350, 150],
            ["Stad",     "South", 100, 400, 390, 140],
            ["Strömmen", "South", 250, 200,  75,  50],
        ],
        columns=[
            "power_plant",
            "location",
            "gain_mw_per_hz",
            "installed_capacity_mw",
            "base_generation_mw",
            "minimal_generation_mw",
        ],
    )


    data['share_of_gain'] = data['gain_mw_per_hz'] / data['gain_mw_per_hz'].sum()

    data
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    _df = mo.sql(
        f"""

        """
    )
    return


@app.cell
def _():
    OPERATIONAL_DELTA_HZ = 0.2
    RESERVE_DELTA_HZ = 0.4
    TRANSMISSION_CAPACIY_MW = 4000 # Between North and South
    return OPERATIONAL_DELTA_HZ, RESERVE_DELTA_HZ


@app.cell(hide_code=True)
def _(data, mo):
    data_grouped = mo.sql(
        f"""
        select
            location,
            sum(gain_mw_per_hz) as gain,
            sum(installed_capacity_mw) as installed_capacity_mw,
            sum(base_generation_mw) as base_generation_mw,
            sum(minimal_generation_mw) as minimal_generation_mw,
            sum(installed_capacity_mw) - sum(base_generation_mw) as available_delta,
            max(installed_capacity_mw) as max_installed_capacity_mw
        from data

        group by location

        order by location
        """
    )
    return


@app.cell(hide_code=True)
def _(data, mo):
    data_total = mo.sql(
        f"""
        select
            sum(gain_mw_per_hz) as gain,
            sum(installed_capacity_mw) as installed_capacity_mw,
            sum(base_generation_mw) as base_generation_mw,
            sum(minimal_generation_mw) as minimal_generation_mw,
            max(base_generation_mw) as max_base_generation_mw
        from data
        """
    )
    return (data_total,)


@app.cell
def _():
    # need tot allocate capacity to both the operational and reserve
    # gain of the reserve: max generation / delta reserve hz
    # allocate gain of the reserve first in north
    # 
    return


@app.cell
def _(OPERATIONAL_DELTA_HZ, data_total, mo):
    delta_operational_generation_mw = (
        data_total['gain'].item() * OPERATIONAL_DELTA_HZ
    )

    mo.md(f'$\Delta G_O = {delta_operational_generation_mw}$')
    return (delta_operational_generation_mw,)


@app.cell
def _(RESERVE_DELTA_HZ, data_total):
    gain_reserve = data_total['max_base_generation_mw'].item() / RESERVE_DELTA_HZ

    gain_reserve
    return


@app.cell
def _(delta_operational_generation_mw):
    delta_operational_generation_mw * 0.3, delta_operational_generation_mw * (1-0.3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    * Which power plants are contributing to the normal
    operation reserve and how large is then the total gain of the normal operation reserve?
        *
    * Which power plants are contributing to the disturbance reserve and how large is then the total gain of the disturbance reserve?
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## AI Prompts
    > Do you dimension normal operation reserve using delta G = (delta f)*R
    >
    > and disturbance reserve from loss of the largest power plan: R = (max capacity) / (delta f)
    """)
    return


if __name__ == "__main__":
    app.run()
