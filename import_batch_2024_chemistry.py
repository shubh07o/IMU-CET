import sqlite3
import json
from db_manager import add_question, export_to_json, get_stats

questions = [
    {
        "q_id": "IMU_2024_CHEM_181",
        "question_number": 181,
        "question_text": "Colloidal solution commonly used in the treatment of skin disease is:",
        "option_a": "Colloidal Gold",
        "option_b": "Colloidal Antimony",
        "option_c": "Colloidal Sulphur",
        "option_d": "Colloidal Silver",
        "correct_option": "C",
        "explanation": "Colloidal sulphur is widely used as an effective medicine for treating skin ailments.",
        "topic": "Surface Chemistry / Colloids",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_182",
        "question_number": 182,
        "question_text": "Reaction between aldehyde and alcohol forms:",
        "option_a": "Glycol",
        "option_b": "Acetate",
        "option_c": "Ester",
        "option_d": "Acetal",
        "correct_option": "D",
        "explanation": "Aldehydes react with alcohols in dry HCl gas to produce hemiacetals, which further react with alcohol to yield stable acetals.",
        "topic": "Aldehydes, Ketones and Carboxylic Acids",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_183",
        "question_number": 183,
        "question_text": "Which hydride is electron deficient?:",
        "option_a": "CH_4",
        "option_b": "B_2H_6",
        "option_c": "NaH",
        "option_d": "CaH_2",
        "correct_option": "B",
        "explanation": "Diborane (B2H6) has 12 valence electrons across 8 bonds with 3-center-2-electron banana bonds, making it electron deficient.",
        "topic": "p-Block Elements / Group 13",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_184",
        "question_number": 184,
        "question_text": "In fuel cells, catalyst used is:",
        "option_a": "Zinc - Mercury",
        "option_b": "Lead - Manganese",
        "option_c": "Platinum - Palladium",
        "option_d": "Nickel - Cadmium",
        "correct_option": "C",
        "explanation": "Finely divided Platinum (Pt) and Palladium (Pd) are widely used catalysts embedded into electrodes in fuel cells.",
        "topic": "Electrochemistry / Fuel Cells",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_185",
        "question_number": 185,
        "question_text": "Hexamine platinum (IV) chloride gives ______ number of ions on ionization:",
        "option_a": "3",
        "option_b": "2",
        "option_c": "5",
        "option_d": "4",
        "correct_option": "C",
        "explanation": "[Pt(NH3)6]Cl4 ionizes to give 1 complex cation [Pt(NH3)6]^{4+} and 4 chloride anions Cl^-, giving 5 total ions.",
        "topic": "Coordination Compounds",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_186",
        "question_number": 186,
        "question_text": "Test to differentiate pentan-2-one and pentan-3-one:",
        "option_a": "Fehling's test",
        "option_b": "Iodoform test",
        "option_c": "Baeyer's test",
        "option_d": "Benedict's test",
        "correct_option": "B",
        "explanation": "Pentan-2-one contains a methyl ketone group (-COCH3) and gives a positive yellow precipitate in the iodoform test, while pentan-3-one does not.",
        "topic": "Aldehydes and Ketones",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_187",
        "question_number": 187,
        "question_text": "Aqueous solution of 18g water and 414g ethyl alcohol. Mole fraction of water is:",
        "option_a": "0.7",
        "option_b": "0.9",
        "option_c": "0.1",
        "option_d": "0.4",
        "correct_option": "C",
        "explanation": "Moles of water = 18/18 = 1. Moles of ethanol = 414/46 = 9. Mole fraction of water = 1 / (1 + 9) = 0.1.",
        "topic": "Solutions / Concentration Terms",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_188",
        "question_number": 188,
        "question_text": "Correct IUPAC name of cis-platin:",
        "option_a": "Diammine dichloride platinum (O)",
        "option_b": "Dichlorido diammine platinum (IV)",
        "option_c": "Diammine dichlorido platinum (II)",
        "option_d": "Diammine dichloride platinum (IV)",
        "correct_option": "C",
        "explanation": "Cis-platin has formula cis-[Pt(NH3)2Cl2], named Diammine dichlorido platinum (II) in IUPAC nomenclature.",
        "topic": "Coordination Compounds / IUPAC",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_189",
        "question_number": 189,
        "question_text": "C_7H_8O gives tribromo derivative C_7H_5OBr_3 with bromine:",
        "option_a": "m-Cresol",
        "option_b": "p-Cresol",
        "option_c": "Benzyl alcohol",
        "option_d": "o-Cresol",
        "correct_option": "A",
        "explanation": "In m-cresol (3-methylphenol), positions 2, 4, and 6 are activated and unhindered/open for electrophilic bromination, forming a tribromo derivative.",
        "topic": "Alcohols, Phenols and Ethers",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2024_CHEM_190",
        "question_number": 190,
        "question_text": "Ethanol heated with excess conc. H_2SO_4 at 443K gives:",
        "option_a": "ethane",
        "option_b": "methane",
        "option_c": "ethene",
        "option_d": "ethyne",
        "correct_option": "C",
        "explanation": "Acid-catalyzed dehydration of ethanol at 443K (170°C) yields ethene via beta-elimination.",
        "topic": "Alcohols, Phenols and Ethers",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_191",
        "question_number": 191,
        "question_text": "Anisole + HI gives:",
        "option_a": "Benzene + Methanol",
        "option_b": "Phenol + Methane",
        "option_c": "Phenol + Iodomethane",
        "option_d": "Sodium phenate + Methanol",
        "correct_option": "C",
        "explanation": "The phenyl-oxygen bond has partial double bond character due to resonance and does not cleave; iodide attacks the methyl group, producing phenol and iodomethane (CH3I).",
        "topic": "Alcohols, Phenols and Ethers",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_192",
        "question_number": 192,
        "question_text": "Reacting substances in Kolbe's reaction:",
        "option_a": "Sodium phenate and CCl_4",
        "option_b": "Phenol and CHCl_3",
        "option_c": "Sodium phenate and CO_2",
        "option_d": "Phenol and CCl_4",
        "correct_option": "C",
        "explanation": "In Kolbe's reaction, sodium phenoxide reacts with CO2 under pressure followed by acidification to produce salicylic acid.",
        "topic": "Alcohols, Phenols and Ethers / Named Reactions",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_193",
        "question_number": 193,
        "question_text": "Ethanoic acid undergoes HVZ reaction but Methanoic acid does not because of:",
        "option_a": "absence of \\alpha-H in ethanoic acid",
        "option_b": "higher acidity",
        "option_c": "presence of \\alpha-H in methanoic acid",
        "option_d": "presence of \\alpha-H in ethanoic acid",
        "correct_option": "D",
        "explanation": "The Hell-Volhard-Zelinsky (HVZ) reaction requires an alpha-hydrogen atom, which is present in ethanoic acid (CH3COOH) but absent in methanoic acid (HCOOH).",
        "topic": "Carboxylic Acids / Named Reactions",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_194",
        "question_number": 194,
        "question_text": "Vacant space in body centered cubic (BCC) lattice unit cell:",
        "option_a": "23%",
        "option_b": "46%",
        "option_c": "32%",
        "option_d": "10%",
        "correct_option": "C",
        "explanation": "Packing efficiency of BCC is 68%, therefore percentage of vacant space = 100% - 68% = 32%.",
        "topic": "Solid State / Unit Cells",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_195",
        "question_number": 195,
        "question_text": "Wavelength 2.2 \\times 10^{-11} m, h = 6.6 \\times 10^{-34} Js, momentum of photon is:",
        "option_a": "1.452 \\times 10^{-44}",
        "option_b": "6.89 \\times 10^{43}",
        "option_c": "3 \\times 10^{-23} kg ms^{-1}",
        "option_d": "3.33 \\times 10^{-22}",
        "correct_option": "C",
        "explanation": "Momentum p = h / \\lambda = 6.6e-34 / 2.2e-11 = 3e-23 kg m/s.",
        "topic": "Structure of Atom / Dual Nature",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_196",
        "question_number": 196,
        "question_text": "Products A and B in R-X + AgCN -> A and R-X + KCN -> B:",
        "option_a": "A = RNC; B = RCN",
        "option_b": "A = RNC; B = RNC",
        "option_c": "A = R-CN; B = RCN",
        "option_d": "A = RCN; B = RNC",
        "correct_option": "A",
        "explanation": "AgCN is predominantly covalent giving alkyl isocyanide (RNC); KCN is ionic giving alkyl cyanide (RCN).",
        "topic": "Haloalkanes and Haloarenes",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_197",
        "question_number": 197,
        "question_text": "Work done when 2 moles ideal gas expands reversibly & isothermally 1L to 10L at 300K (R=0.0083 kJ K^{-1}mol^{-1}):",
        "option_a": "0.115 kJ",
        "option_b": "58.5 kJ",
        "option_c": "11.5 kJ",
        "option_d": "5.8 kJ",
        "correct_option": "C",
        "explanation": "W = 2.303 * n * R * T * log10(V2/V1) = 2.303 * 2 * 0.0083 * 300 * 1 = 11.47 kJ \\approx 11.5 kJ.",
        "topic": "Chemical Thermodynamics",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_198",
        "question_number": 198,
        "question_text": "First order reaction t_{1/2} = 45 min. Time for 99.9% completion:",
        "option_a": "10 Hours",
        "option_b": "20 Hours",
        "option_c": "5 Hours",
        "option_d": "7.5 Hours",
        "correct_option": "D",
        "explanation": "t(99.9%) = 10 * t(1/2) = 10 * 45 min = 450 min = 7.5 Hours.",
        "topic": "Chemical Kinetics",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_199",
        "question_number": 199,
        "question_text": "For spontaneity of a cell, correct condition is:",
        "option_a": "\\Delta G = +ve, E = +ve",
        "option_b": "\\Delta G = -ve",
        "option_c": "\\Delta G = 0, E = 0",
        "option_d": "\\Delta G = -ve, E = 0",
        "correct_option": "B",
        "explanation": "The criterion for thermodynamic spontaneity of an electrochemical process is Delta G < 0 (negative).",
        "topic": "Electrochemistry / Thermodynamics",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2024_CHEM_200",
        "question_number": 200,
        "question_text": "Solubility of a gas in a liquid increases with:",
        "option_a": "increase of P and decrease of T",
        "option_b": "decrease of P and decrease of T",
        "option_c": "increase of P and increase of T",
        "option_d": "decrease of P and increase of T",
        "correct_option": "A",
        "explanation": "Henry's Law states gas solubility increases with pressure; dissolution of gas in liquid is exothermic, so lower temperature favors higher solubility.",
        "topic": "Solutions / Henry's Law",
        "difficulty": "Easy"
    }
]

def run_import():
    year = 2024
    section = "Chemistry"
    print(f"Importing {len(questions)} questions for {year} - {section}...")
    for q in questions:
        add_question(
            year=year,
            section=section,
            question_text=q["question_text"],
            option_a=q["option_a"],
            option_b=q["option_b"],
            option_c=q["option_c"],
            option_d=q["option_d"],
            correct_option=q["correct_option"],
            explanation=q["explanation"],
            topic=q["topic"],
            difficulty=q["difficulty"],
            question_number=q["question_number"],
            q_id=q["q_id"]
        )
    export_to_json(year)
    print("Import complete! Current Stats:")
    for stat in get_stats():
        print(f"Year: {stat['year']} | Section: {stat['section']} | Questions: {stat['count']}")

if __name__ == "__main__":
    run_import()
