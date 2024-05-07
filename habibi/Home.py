import streamlit as st

import altair as alt
import logging
import pandas as pd
import random
import sys
from time import time


# Control variables
anesthetics_list = [
        "0.25% Plain Lidocaine",
        "0.25% Plain Bupivacaine",
        "0.25% Lidocaine with Epinephrine",
        "0.5% Plain Bupivacaine",
        "0.5% Bupivacaine with Epinephrine",
        "1% Plain Lidocaine",
        "1% Lidocaine with Epinephrine",
        "2% Plain Lidocaine",
        "2% Lidocaine with Epinephrine"
]
if "anesthetics_options" not in st.session_state:
    st.session_state.anesthetics_options = anesthetics_list
if "input_weight" not in st.session_state:
    st.session_state.input_weight = random.randint(10, 80)
if "input_anesthetic" not in st.session_state:
    st.session_state.input_anesthetic = random.choice(st.session_state.anesthetics_options)

# Display variables
if "text" not in st.session_state:
    st.session_state.text = ""
if "show_formula" not in st.session_state:
    st.session_state.show_formula = False
if "show_table" not in st.session_state:
    st.session_state.show_table = False

# User tracking
if "user_differentials" not in st.session_state:
    st.session_state.user_differentials = []
if "user_times" not in st.session_state:
    st.session_state.user_times = []
if "_id" not in st.session_state:
    st.session_state._id = hash(time())
if "logger" not in st.session_state:
    st.session_state.logger = logging.getLogger()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # filename='habibi.log'
    st.session_state.logger.info(f'{{"time": "{time()}", "session_id": "{st.session_state._id}"}}')
if "session_start" not in st.session_state:
    st.session_state.session_start = time()


def clear_fields():
    st.session_state["text"] = ""


@st.cache_data
def get_data():
    """
    Will persist per session.
    """
    st.session_state["input_weight"] = random.randint(10, 80)
    st.session_state["input_anesthetic"] = random.choice(st.session_state.anesthetics_options)
    return


def calculate_safe_dose(weight, input):
    """
    Calculate the dosage. To-do, move the list to a config file.
    """
    safe_dose = {
        "0.25% Plain Lidocaine": 4,
        "0.25% Plain Bupivacaine": 2,
        "0.25% Lidocaine with Epinephrine": 7,
        "0.5% Plain Bupivacaine": 2,
        "0.5% Bupivacaine with Epinephrine": 3,
        "1% Plain Lidocaine": 4,
        "1% Lidocaine with Epinephrine": 7,
        "2% Plain Lidocaine": 4,
        "2% Lidocaine with Epinephrine": 7,
    }
    percent = float(input.split("%")[0])
    answer = weight * safe_dose[input] * (.1 / percent)  # 1mL/%*10mg
    answer = round(answer, 4)
    return answer, safe_dose[input], percent


if __name__ == "__main__":

    # Sidebar - Settings
    st.sidebar.markdown("# Settings")
    show_settings = st.sidebar.checkbox("Update Settings")
    if show_settings:
        st.markdown("""
            <style>
                .stMultiSelect [data-baseweb=select] span{
                    max-width: 250px;
                    font-size: 0.6rem;
                }
            </style>
            """, unsafe_allow_html=True)
        anesthetics_list  = st.sidebar.multiselect(
            label="Anesthetic Options",
            options=anesthetics_list,
            default=st.session_state.anesthetics_options,
        )
        save_settings = st.sidebar.button("Save")
        if save_settings:
            st.session_state.anesthetics_options = anesthetics_list
            st.sidebar.success("Updated!")

    # Sidebar - Progress
    show_progress = st.sidebar.checkbox("Show Progress")
    if show_progress:
        if not st.session_state.user_times:
            st.sidebar.warning('Progress tracking requires one or more submitted answers.')
            st.stop()
        st.sidebar.markdown("Tracking response time and accuracy. Data resets on a page refresh.")
        problem_index = [x for x in range(1, len(st.session_state.user_times)+1)]
        user_times = pd.DataFrame(
            {
                "Time (s)": st.session_state.user_times,
                "Problem": problem_index
            }
        )
        times_chart = alt.Chart(
            user_times,
            title=alt.Title(
                "User Response Time"
            )
        ).mark_line().encode(
            x=alt.X('Problem', axis=alt.Axis(values=problem_index, labelOverlap="greedy", grid=False)),
            y=alt.Y('Time (s)', axis=alt.Axis(tickCount=5, labelOverlap="greedy", grid=False))
        )
        st.sidebar.altair_chart(times_chart, use_container_width=True)
        user_differentials = pd.DataFrame(
            {
                "Differential (mL)": st.session_state.user_differentials,
                "Problem": problem_index
            }
        )
        differentials_chart = alt.Chart(
            user_differentials,
            title=alt.Title(
                "Differential"
            )
        ).mark_line().encode(
            x=alt.X('Problem', axis=alt.Axis(values=problem_index, labelOverlap="greedy", grid=False)),
            y=alt.Y('Differential (mL)', axis=alt.Axis(tickCount=5, labelOverlap="greedy", grid=False))
        )
        st.sidebar.altair_chart(differentials_chart, use_container_width=True)

    # Sidebar - Resources
    st.sidebar.markdown("# References")
    st.sidebar.markdown("## **Local Anesthetic Characteristics**")
    st.sidebar.markdown("Becker DE, Reed KL. Local anesthetics: review of pharmacological considerations. Anesth Prog. 2012 Summer;59(2):90-101; quiz 102-3. doi: 10.2344/0003-3006-59.2.90. PMID: 22822998; PMCID: PMC3403589.")
    st.sidebar.markdown("## **Easy Calculation**")
    st.sidebar.markdown("Ahmed OA. Local anaesthetics for surgeons: A simple method to calculate the safe volume of local anaesthetic for infiltration during surgical procedures. J Plast Reconstr Aesthet Surg. 2023 Aug;83:479-480. doi: 10.1016/j.bjps.2023.05.034. Epub 2023 May 19. PMID: 37356407.")
    st.sidebar.markdown("## **Injection Technique**")
    st.sidebar.markdown("Joukhadar N, Lalonde D. How to Minimize the Pain of Local Anesthetic Injection for Wide Awake Surgery. Plast Reconstr Surg Glob Open. 2021 Aug 4;9(8):e3730. doi: 10.1097/GOX.0000000000003730. PMID: 34367856; PMCID: PMC8337068")
    st.sidebar.markdown("Lalonde D, Wong A. Local Anesthetics: What's New in Minimal Pain Injection and Best Evidence in Pain Control. Plast Reconstr Surg. 2014 Oct;134(4 Suppl 2):40S-49S. doi: 10.1097/PRS.0000000000000679. PMID: 25255006.")
    st.sidebar.markdown("Gottlieb M, Penington A, Schraft E. Digital Nerve Blocks: A Comprehensive Review of Techniques. J Emerg Med. 2022 Oct;63(4):533-540. doi: 10.1016/j.jemermed.2022.07.002. Epub 2022 Oct 11. PMID: 36229322.")
    st.sidebar.markdown("Moskovitz JB, Sabatino F. Regional nerve blocks of the face. Emerg Med Clin North Am. 2013 May;31(2):517-27. doi: 10.1016/j.emc.2013.01.003. Epub 2013 Feb 18. PMID: 23601486.")
    st.sidebar.markdown("## **Toxicity Signs and Treatment**")
    st.sidebar.markdown("Gitman M, Fettiplace MR, Weinberg GL, Neal JM, Barrington MJ. Local Anesthetic Systemic Toxicity: A Narrative Literature Review and Clinical Update on Prevention, Diagnosis, and Management. Plast Reconstr Surg. 2019 Sep;144(3):783-795. doi: 10.1097/PRS.0000000000005989. PMID: 31461049.")
    st.sidebar.markdown("## **Education Theory**")
    st.sidebar.markdown("Gitman M, Fettiplace MR, Weinberg GL, Neal JM, Barrington MJ. Local Anesthetic Systemic Toxicity: A Narrative Literature Review and Clinical Update on Prevention, Diagnosis, and Management. Plast Reconstr Surg. 2019 Sep;144(3):783-795. doi: 10.1097/PRS.0000000000005989. PMID: 31461049.")

    # Main display
    st.markdown("### How much local can you inject?")
    st.text(f"Weight (kg): {st.session_state.input_weight}")
    st.text(f"Anesthetic: {st.session_state.input_anesthetic}")
    answer, dosage_amount, percent = calculate_safe_dose(
        st.session_state.input_weight,
        st.session_state.input_anesthetic
    )

    input_answer = st.text_input(
        label="Answer (mL)",
        value="",
        key="text"
    )
    col1, col2 = st.columns(2)
    check = col1.button("Check")
    next = col2.button("Next", on_click=clear_fields)

    # Control logic
    if input_answer or check:
        try:
            input_answer = float(input_answer)
        except:
            st.warning("Please input a number in decimal form.")
            st.stop()

        differential = round(abs(answer - input_answer), 4)
        rounded_differential = round(differential, 2)
        percent_differential = differential / answer

        # User tracking
        total_time = round(time() - st.session_state.session_start, 4)
        st.session_state.user_times.append(total_time)
        st.session_state.user_differentials.append(differential)
        st.session_state.logger.info(f'{{"time": "{time()}", "session_id": "{st.session_state._id}",'
                                     f' "differential": "{differential}", "time"="{total_time}"}}')

        # Results display
        st.success(f"{answer} mL")
        if percent_differential < .05:
            st.success(f"Off by: {rounded_differential} mL")
        elif percent_differential < .10:
            st.warning(f"Off by {rounded_differential} mL")
        else:
            st.error(f"Off by {rounded_differential} mL")

    # Display variables
    show_formula = st.checkbox("Show Formula")
    if show_formula:
        st.latex(rf'''
                    {st.session_state.input_weight} kg \times  ({dosage_amount} \frac{{mg}}{{kg}}) \times 
                    (\frac{{1 ml}}{{{percent} \times 10 mg}})

        ''')

    show_table = st.checkbox("Show Conversion Table", value=st.session_state.show_table)
    if show_table:
        safe_dose = {
            "Plain Lidocaine": 4,
            "Lidocaine with Epinephrine": 7,
            "Plain Bupivacaine": 2,
            "Bupivacaine with Epinephrine": 3,
        }
        df = pd.DataFrame({"Anesthetic": safe_dose.keys(), "Safe Dosage (mg/kg)": safe_dose.values()})
        st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    if next:
        input_answer = None
        st.session_state["input_weight"] = random.randint(10, 80)
        try:
            st.session_state.input_anesthetic = random.choice(st.session_state.anesthetics_options)
        except:
            st.warning("You must select at least one anesthetic in Settings.")
            st.stop()
        st.session_state.session_start = time()
        st.rerun()
