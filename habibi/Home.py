import streamlit as st

import pandas as pd
import random

# Global variables
medications_list = [
    "0.25% Plain Lidocaine",
    "0.25% Lidocaine with Epinephrine",
    "1% Plain Lidocaine",
    "1% Lidocaine with Epinephrine",
    "2% Plain Lidocaine",
    "2% Lidocaine with Epinephrine"
]

if "input_weight" not in st.session_state:
    st.session_state.input_weight = random.randint(10, 80)
if "input_anesthetic" not in st.session_state:
    st.session_state.input_anesthetic = random.choice(medications_list)
if "text" not in st.session_state:
    st.session_state.text = ""
if "show_formula" not in st.session_state:
    st.session_state.show_formula = False
if "show_table" not in st.session_state:
    st.session_state.show_table = False


def clear_fields():
    st.session_state["text"] = ""


@st.cache_data
def get_data(shuffle=None):
    shuffle = None
    st.session_state["input_weight"] = random.randint(10, 80)
    st.session_state["input_anesthetic"] = random.choice(medications_list)
    return


def calculate_safe_dose(weight, input):
    """

    @param weight:
    @param input:
    @return:
    """
    safe_dose = {
        "0.25% Plain Lidocaine": 4,
        "0.25% Lidocaine with Epinephrine": 7,
        "1% Plain Lidocaine": 4,
        "1% Lidocaine with Epinephrine": 7,
        "2% Plain Lidocaine": 4,
        "2% Lidocaine with Epinephrine": 7,
    }
    percent = float(input.split("%")[0])
    answer = weight * safe_dose[input] * (.1 / percent)  # 1mL/%*10mg
    answer = round(answer, 2)
    return answer, safe_dose[input], percent


if __name__ == "__main__":

    # Sidebar - Settings
    st.sidebar.markdown("# Settings")
    configure = st.sidebar.checkbox("Show Settings")
    if configure:
        list = st.sidebar.multiselect(
            label="Anesthetics",
            options=medications_list,
            default=medications_list
        )

    # Sidebar - Resources
    st.sidebar.markdown("# References")
    st.sidebar.markdown("## **Local Anesthetic Characteristics**")
    st.sidebar.write(
        "Becker DE, Reed KL. Local anesthetics: review of pharmacological considerations. Anesth Prog. 2012 Summer;59(2):90-101; quiz 102-3. doi: 10.2344/0003-3006-59.2.90. PMID: 22822998; PMCID: PMC3403589.")

    st.sidebar.markdown("## **Easy Calculation**")
    st.sidebar.markdown("Ahmed OA. Local anaesthetics for surgeons: A simple method to calculate the safe volume of local anaesthetic for infiltration during surgical procedures. J Plast Reconstr Aesthet Surg. 2023 Aug;83:479-480. doi: 10.1016/j.bjps.2023.05.034. Epub 2023 May 19. PMID: 37356407.")

    st.sidebar.markdown("## **Injection Technique**")
    st.sidebar.markdown(
        "Joukhadar N, Lalonde D. How to Minimize the Pain of Local Anesthetic Injection for Wide Awake Surgery. Plast Reconstr Surg Glob Open. 2021 Aug 4;9(8):e3730. doi: 10.1097/GOX.0000000000003730. PMID: 34367856; PMCID: PMC8337068")
    st.sidebar.markdown(
        "Lalonde D, Wong A. Local Anesthetics: What's New in Minimal Pain Injection and Best Evidence in Pain Control. Plast Reconstr Surg. 2014 Oct;134(4 Suppl 2):40S-49S. doi: 10.1097/PRS.0000000000000679. PMID: 25255006.")
    st.sidebar.markdown(
        "Gottlieb M, Penington A, Schraft E. Digital Nerve Blocks: A Comprehensive Review of Techniques. J Emerg Med. 2022 Oct;63(4):533-540. doi: 10.1016/j.jemermed.2022.07.002. Epub 2022 Oct 11. PMID: 36229322.")
    st.sidebar.markdown(
        "Moskovitz JB, Sabatino F. Regional nerve blocks of the face. Emerg Med Clin North Am. 2013 May;31(2):517-27. doi: 10.1016/j.emc.2013.01.003. Epub 2013 Feb 18. PMID: 23601486.")

    st.sidebar.markdown("## **Toxicity Signs and Treatment**")
    st.sidebar.markdown(
        "Gitman M, Fettiplace MR, Weinberg GL, Neal JM, Barrington MJ. Local Anesthetic Systemic Toxicity: A Narrative Literature Review and Clinical Update on Prevention, Diagnosis, and Management. Plast Reconstr Surg. 2019 Sep;144(3):783-795. doi: 10.1097/PRS.0000000000005989. PMID: 31461049.")



    # Main display
    st.markdown("### How much local can you inject?")
    st.text(f"Weight (kg): {st.session_state.input_weight}")
    st.text(f"Anesthetic: {st.session_state.input_anesthetic}")
    answer, dosage_amount, percent = calculate_safe_dose(
        st.session_state.input_weight,
        st.session_state.input_anesthetic
    )

    input_answer = st.text_input(
        label="Answer",
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

        differential = round(abs(answer - input_answer))
        st.markdown(f"Correct answer: {answer} mL")
        st.markdown(f"Differential: {differential} mL")  # weight * safe_dose[medicine] * (1ml / percent*10mg )

        if check and differential < 5:
            st.balloons()
        if check and differential > 10:
            st.warning("Nice try idiot")

    if next:
        input_answer = None
        st.session_state["input_weight"] = random.randint(10, 80)
        st.session_state["input_anesthetic"] = random.choice(medications_list)
        st.rerun()

    # Display variables
    st.session_state.show_formula = st.checkbox("Show Formula", value=st.session_state.show_formula)
    if st.session_state.show_formula:
        st.latex(rf'''
                    {st.session_state.input_weight} kg \times  ({dosage_amount} \frac{{mg}}{{kg}}) \times 
                    (\frac{{1 ml}}{{{percent} \times 10 mg}})

                    ''')
    st.session_state.show_table = st.checkbox("Show Conversion Table", value=st.session_state.show_table)
    if st.session_state.show_table:
        st.image("table.png", width=400)

