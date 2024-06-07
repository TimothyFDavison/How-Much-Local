import streamlit as st

import altair as alt
import logging
import pandas as pd
import random
import sys
from time import time

import config


# Control variables

# Display variables
if "text" not in st.session_state:
    st.session_state.text = ""
if "show_formula" not in st.session_state:
    st.session_state.show_formula = False
if "show_table" not in st.session_state:
    st.session_state.show_table = False


def clear_fields():
    st.session_state["text"] = ""


def calculate_safe_dose(weight, input):
    """
    Calculate the dosage. To-do, move the list to a config file.
    """
    percent = float(input.split("%")[0])
    answer = weight * config.SAFE_DOSAGES[input] * (.1 / percent)  # 1mL/%*10mg
    answer = round(answer, 4)
    return answer, config.SAFE_DOSAGES[input], percent


if __name__ == "__main__":


    # Main display
    st.markdown("### Calculator - How much local can you inject?")
    weight = st.text_input(f"Weight (kg)")
    anesthetic = st.selectbox(
        label="Anesthetic",
        options=sorted(list(config.SAFE_DOSAGES.keys()))
    )
    submit = st.button("Submit")

    # Control logic
    if (weight and anesthetic) or submit:
        try:
            weight = float(weight)
        except Exception as e:
            st.warning("Could not parse weight input. Please provide a number.")

        answer, dosage_amount, percent = calculate_safe_dose(
            weight,
            anesthetic
        )
        st.success(f"{answer} mL")

    # Display variables
    show_formula = st.checkbox("Show Formula")
    if show_formula:
        try:
            weight = float(weight)
            answer, dosage_amount, percent = calculate_safe_dose(
                weight,
                anesthetic
            )
            st.latex(rf'''
                        {weight} kg \times  ({dosage_amount} \frac{{mg}}{{kg}}) \times 
                        (\frac{{1 ml}}{{{percent} \times 10 mg}})

            ''')
        except Exception as e:
            st.warning("Could not parse weight input. Please provide a number.")

    show_table = st.checkbox("Show Conversion Table", value=st.session_state.show_table)
    if show_table:
        df = pd.DataFrame(
            {
                "Anesthetic": config.SAFE_DOSAGES_TABLE.keys(),
                "Safe Dosage (mg/kg)": config.SAFE_DOSAGES_TABLE.values()
            }
        )
        st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    show_calculator = st.checkbox("Show Calculator")
    if show_calculator:
        calculator_input = st.text_input("Input a mathematical expression, e.g. \"60*12/2+12\"")
        calculator_enter = st.button("Enter")
        if calculator_enter:
            try:
                allowed_chars = "0123456789+-*(). /"
                for char in calculator_input:
                    if char not in allowed_chars:
                        raise Exception(f"Unsafe evaluation: {calculator_input}")
                result = eval(calculator_input, {"__builtins__":None}, {})  # DO NOT LAUNCH UNTIL INPUTS SANITIZED
                st.success(result)
            except Exception as e:
                print(e)
                st.warning("Could not resolve expression.")
