import sqlite3
import json
from db_manager import add_question, export_to_json, get_stats

chemistry_questions = [
    {
        "q_id": "IMU_2026_S1_CHEM_181",
        "question_number": 181,
        "question_text": "The values of Van't Hoff factor (i) for 50% dissociation of \\text{K}_4[\\text{Fe}(\\text{CN})_6] is:",
        "option_a": "5",
        "option_b": "1",
        "option_c": "3",
        "option_d": "2",
        "correct_option": "C",
        "explanation": "K4[Fe(CN)6] dissociates into 4 K^+ and 1 [Fe(CN)6]^(4-) ions, so n = 5. Degree of dissociation \\alpha = (i - 1) / (n - 1) => 0.5 = (i - 1) / 4 => i - 1 = 2 => i = 3.",
        "topic": "Solutions / Colligative Properties and Van't Hoff Factor",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_182",
        "question_number": 182,
        "question_text": "Which of the following represents the ground state electron configuration for the \\text{Mn}^{3+} ion? (Atomic number of Mn = 25):",
        "option_a": "1s^2 2s^2 2p^6 3s^2 3p^6 3d^4",
        "option_b": "1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^5",
        "option_c": "1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^2",
        "option_d": "1s^2 2s^2 2p^6 3s^2 3p^6 4s^1 3d^3",
        "correct_option": "A",
        "explanation": "Mn (Z = 25) configuration is [Ar] 3d^5 4s^2. For Mn^(3+), three electrons are removed (two from 4s, one from 3d), giving [Ar] 3d^4 = 1s^2 2s^2 2p^6 3s^2 3p^6 3d^4.",
        "topic": "Structure of Atom / Electronic Configuration",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_183",
        "question_number": 183,
        "question_text": "The secondary valence of Co in [\\text{Co}(\\text{en})_3]\\text{Cl}_3 is:",
        "option_a": "9",
        "option_b": "6",
        "option_c": "3",
        "option_d": "4",
        "correct_option": "B",
        "explanation": "Secondary valence equals the coordination number. Ethylenediamine ('en') is a bidentate ligand, so coordination number = 3 * 2 = 6.",
        "topic": "Coordination Compounds / Werner's Theory",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_184",
        "question_number": 184,
        "question_text": "Which is the correct order of acid strength from the following?:",
        "option_a": "\\text{C}_6\\text{H}_5\\text{OH} > \\text{ROH} > \\text{H}_2\\text{O}",
        "option_b": "\\text{ROH} > \\text{C}_6\\text{H}_5\\text{OH} > \\text{H}_2\\text{O}",
        "option_c": "\\text{H}_2\\text{O} > \\text{C}_6\\text{H}_5\\text{OH} > \\text{ROH}",
        "option_d": "\\text{C}_6\\text{H}_5\\text{OH} > \\text{H}_2\\text{O} > \\text{ROH}",
        "correct_option": "D",
        "explanation": "Phenol (C6H5OH) is more acidic than water due to resonance stabilization of phenoxide ion. Water is more acidic than aliphatic alcohol (ROH) due to the electron-donating +I effect of alkyl groups. Order: C6H5OH > H2O > ROH.",
        "topic": "Alcohols, Phenols and Ethers / Acidity",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_185",
        "question_number": 185,
        "question_text": "The IUPAC name for \\text{CH}_3\\text{-CH(OH)-CH}_2\\text{-CHO} is:",
        "option_a": "Butan-1-ol-3-one",
        "option_b": "3-Oxobutanol",
        "option_c": "2-Hydroxybutanal",
        "option_d": "3-Hydroxybutanal",
        "correct_option": "D",
        "explanation": "The principal functional group is aldehyde (-CHO) at C1. The -OH is a prefix substituent at C3 of the 4-carbon chain: 3-Hydroxybutanal.",
        "topic": "Aldehydes, Ketones and Carboxylic Acids / IUPAC Nomenclature",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_186",
        "question_number": 186,
        "question_text": "What is the mole fraction of a solute in a 1 molal aqueous solution? (Molar mass of \\text{H}_2\\text{O} = 18\\text{ g/mol}):",
        "option_a": "1.77",
        "option_b": "0.177",
        "option_c": "0.0177",
        "option_d": "0.0354",
        "correct_option": "C",
        "explanation": "1 molal aqueous solution contains 1 mol solute in 1000 g H2O (55.55 mol). Mole fraction = 1 / (1 + 55.55) = 1 / 56.55 = 0.0177.",
        "topic": "Solutions / Concentration Terms",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_187",
        "question_number": 187,
        "question_text": "Zr and Hf have almost equal atomic and ionic radii because of:",
        "option_a": "belonging to the same group",
        "option_b": "lanthanoid contraction",
        "option_c": "actinoid contraction",
        "option_d": "diagonal relationship",
        "correct_option": "B",
        "explanation": "Lanthanoid contraction (poor shielding by intervening 4f electrons before Hf) causes the atomic and ionic radii of Zr and Hf to be virtually identical.",
        "topic": "d and f Block Elements / Lanthanoid Contraction",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_188",
        "question_number": 188,
        "question_text": "Which of the following has highest freezing point?:",
        "option_a": "1 m KCl solution",
        "option_b": "1m \\text{C}_6\\text{H}_{12}\\text{O}_6 solution",
        "option_c": "1m \\text{AlCl}_3 solution",
        "option_d": "1 m NaCl solution",
        "correct_option": "B",
        "explanation": "Freezing point depression \\Delta T_f = i K_f m. For glucose, i = 1 (lowest), meaning minimum freezing point depression and therefore the highest freezing point.",
        "topic": "Solutions / Colligative Properties",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_189",
        "question_number": 189,
        "question_text": "Which of the following aqueous solution has minimum freezing point?:",
        "option_a": "0.005\\text{ m MgSO}_4",
        "option_b": "0.01\\text{ m NaCl}",
        "option_c": "0.005\\text{ m C}_2\\text{H}_5\\text{OH}",
        "option_d": "0.005\\text{ m MgI}_2",
        "correct_option": "B",
        "explanation": "Minimum freezing point corresponds to maximum i * m. For 0.01 m NaCl, i * m = 2 * 0.01 = 0.02 (highest among all choices).",
        "topic": "Solutions / Colligative Properties",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_190",
        "question_number": 190,
        "question_text": "If the solubility product (K_{sp}) of \\text{AgCl} is 1.6 \\times 10^{-10}, its solubility in water is:",
        "option_a": "1.6 \\times 10^{-5}\\text{ M}",
        "option_b": "0.8 \\times 10^{-5}\\text{ M}",
        "option_c": "1.26 \\times 10^{-5}\\text{ M}",
        "option_d": "4 \\times 10^{-5}\\text{ M}",
        "correct_option": "C",
        "explanation": "For AgCl (AB type salt), K_sp = S^2 => S = \\sqrt{K_sp} = \\sqrt{1.6 \\times 10^{-10}} \\approx 1.26 \\times 10^{-5} M.",
        "topic": "Ionic Equilibrium / Solubility Product",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_191",
        "question_number": 191,
        "question_text": "Which effect involves the complete transfer of a shared pair of \\pi-electrons to one of the atoms in the presence of an attacking reagent?:",
        "option_a": "Hyperconjugation",
        "option_b": "Resonance effect",
        "option_c": "Electromeric effect",
        "option_d": "Inductive effect",
        "correct_option": "C",
        "explanation": "The Electromeric effect involves the temporary complete transfer of a shared pair of \\pi-electrons to one of the bonded atoms on demand of an attacking reagent.",
        "topic": "General Organic Chemistry / Electronic Effects",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_192",
        "question_number": 192,
        "question_text": "For a reversible reaction at 298\\text{ K}, the equilibrium constant K is 200. What is the value of \\Delta G^\\circ at 298\\text{ K}?:",
        "option_a": "-0.13 kcal",
        "option_b": "-13.13 kcal",
        "option_c": "-3.158 kcal",
        "option_d": "-0.413 kcal",
        "correct_option": "C",
        "explanation": "\\Delta G^\\circ = -2.303 R T \\log(K) = -2.303 * (1.987e-3 kcal/K) * 298 * \\log(200) = -3.158 kcal.",
        "topic": "Chemical Thermodynamics / Free Energy and Equilibrium",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_193",
        "question_number": 193,
        "question_text": "Ethyl alcohol (\\text{C}_2\\text{H}_5\\text{OH}) has higher boiling point than dimethyl ether (\\text{CH}_3\\text{-O-CH}_3) although the molecular weight of both are same due to:",
        "option_a": "Lattice enthalpy",
        "option_b": "Intermolecular H- bonding",
        "option_c": "Intramolecular H- bonding",
        "option_d": "Dipole moment",
        "correct_option": "B",
        "explanation": "Ethanol possesses strong intermolecular hydrogen bonding between molecules, whereas dimethyl ether only exhibits weak dipole interactions.",
        "topic": "Alcohols, Phenols and Ethers / Physical Properties",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_194",
        "question_number": 194,
        "question_text": "Which of the following alkyl halides is hydrolysed by S_N1 mechanism?:",
        "option_a": "\\text{CH}_3\\text{CH}_2\\text{CH}_2\\text{Cl}",
        "option_b": "\\text{CH}_3\\text{CH}_2\\text{Cl}",
        "option_c": "(\\text{CH}_3)_3\\text{CCl}",
        "option_d": "\\text{CH}_3\\text{Cl}",
        "correct_option": "C",
        "explanation": "Tertiary alkyl halides like tert-butyl chloride ((CH3)3CCl) form highly stable tertiary carbocations, undergoing hydrolysis via S_N1 mechanism.",
        "topic": "Haloalkanes and Haloarenes / Reaction Mechanisms",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_195",
        "question_number": 195,
        "question_text": "Which one of the following compounds forms salt on reaction with \\text{NaNH}_2?:",
        "option_a": "\\text{C}_2\\text{H}_6",
        "option_b": "\\text{C}_2\\text{H}_4",
        "option_c": "\\text{C}_6\\text{H}_6",
        "option_d": "\\text{C}_2\\text{H}_2",
        "correct_option": "D",
        "explanation": "Acetylene (C2H2) contains acidic terminal hydrogens on sp-hybridized carbons which react with strong base NaNH2 to form sodium acetylide salt.",
        "topic": "Hydrocarbons / Alkynes",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_196",
        "question_number": 196,
        "question_text": "When the system does not exchange heat with the surroundings, the process is:",
        "option_a": "Thermal",
        "option_b": "Isothermal",
        "option_c": "Adiabatic",
        "option_d": "Isochoric",
        "correct_option": "C",
        "explanation": "An adiabatic process is characterized by zero heat exchange (q = 0) between the system and its surroundings.",
        "topic": "Chemical Thermodynamics / Thermodynamic Processes",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_197",
        "question_number": 197,
        "question_text": "A zero order reaction is one whose rate is independent of:",
        "option_a": "the concentration of the reactants",
        "option_b": "the concentration of the product",
        "option_c": "the material of the vessel in which reaction is carried out",
        "option_d": "the temperature of reaction",
        "correct_option": "A",
        "explanation": "By definition, the rate of a zero-order reaction is Rate = k [Reactant]^0 = k, independent of reactant concentration.",
        "topic": "Chemical Kinetics / Order of Reaction",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_198",
        "question_number": 198,
        "question_text": "At the same temperature which of the following aqueous solutions has maximum conducting power?:",
        "option_a": "HCl",
        "option_b": "Urea",
        "option_c": "\\text{CH}_3\\text{COOH}",
        "option_d": "NaCl",
        "correct_option": "A",
        "explanation": "HCl dissociates completely to produce H^+ ions, which have uniquely high molar ionic conductivity in water via the Grotthuss proton-hopping mechanism.",
        "topic": "Electrochemistry / Conductance of Electrolytic Solutions",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_199",
        "question_number": 199,
        "question_text": "Which of the following has the maximum number of atoms?:",
        "option_a": "1g Ag (s)",
        "option_b": "1g Mg (s)",
        "option_c": "1g Li (s)",
        "option_d": "1g of \\text{O}_2 (g)",
        "correct_option": "C",
        "explanation": "Number of atoms = (m / M) * N_A. 1g of Li has (1/7) N_A ≈ 0.143 N_A atoms, which is the highest because Lithium has the lowest atomic weight.",
        "topic": "Some Basic Concepts of Chemistry / Mole Concept",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S1_CHEM_200",
        "question_number": 200,
        "question_text": "Which of the following undergo aldol condensation?:",
        "option_a": "HCHO",
        "option_b": "\\text{CH}_3\\text{CHO}",
        "option_c": "\\text{C}_6\\text{H}_5\\text{CHO}",
        "option_d": "None of these",
        "correct_option": "B",
        "explanation": "Aldol condensation requires presence of \\alpha-hydrogens. Acetaldehyde (CH3CHO) has 3 \\alpha-hydrogens, whereas formaldehyde and benzaldehyde lack \\alpha-hydrogens.",
        "topic": "Aldehydes, Ketones and Carboxylic Acids / Aldol Condensation",
        "difficulty": "Easy"
    }
]

def run_import():
    year = 2026
    shift = "Shift 1"
    section = "Chemistry"
    print(f"Importing {len(chemistry_questions)} questions for {year} ({shift}) - {section}...")
    for q in chemistry_questions:
        add_question(
            year=year,
            shift=shift,
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
    print("Import complete! Current Stats across all years & shifts:")
    for stat in get_stats():
        print(f"Year: {stat['year']} | Shift: {stat['shift']} | Section: {stat['section']} | Questions: {stat['count']}")

if __name__ == "__main__":
    run_import()
