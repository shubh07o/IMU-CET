import sqlite3
import json
from db_manager import add_question, export_to_json, get_stats

chemistry_questions = [
    {
        "q_id": "IMU_2025_CHEM_181",
        "question_number": 181,
        "question_text": "Among the species \\text{K}^+, \\text{Cl}^-, \\text{S}^{2-}, \\text{Ca}^{2+}, which has the largest size?",
        "option_a": "\\text{S}^{2-}",
        "option_b": "\\text{Ca}^{2+}",
        "option_c": "\\text{Cl}^-",
        "option_d": "\\text{K}^+",
        "correct_option": "A",
        "explanation": "All these species are isoelectronic having 18 electrons. In isoelectronic species, size increases with increasing negative charge and decreasing nuclear charge (Z_eff). S^(2-) has Z=16, which is the smallest nuclear charge, hence it has the largest ionic radius.",
        "topic": "Periodic Classification / Periodic Properties",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_182",
        "question_number": 182,
        "question_text": "In Apollo spacecraft, the fuel cell used was:",
        "option_a": "\\text{H}_2\\text{-O}_2 fuel cell",
        "option_b": "\\text{CH}_4\\text{-O}_2 fuel cell",
        "option_c": "Both A & B",
        "option_d": "None",
        "correct_option": "A",
        "explanation": "The hydrogen-oxygen (H2-O2) fuel cell was used in the Apollo space programme for providing electrical power and drinking water for astronauts.",
        "topic": "Electrochemistry / Fuel Cells",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_183",
        "question_number": 183,
        "question_text": "Nitrogenous bases found in RNA are:",
        "option_a": "Cytosine, Adenine, Guanine, Uracil",
        "option_b": "Cytosine, Adenine, Uracil, Guanine",
        "option_c": "Cytosine, Adenine, Thymine, Guanine",
        "option_d": "Cytosine, Adenine, Thymine, Uracil",
        "correct_option": "A",
        "explanation": "RNA contains Adenine, Guanine, Cytosine, and Uracil. Thymine is found in DNA, not RNA.",
        "topic": "Biomolecules / Nucleic Acids",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_184",
        "question_number": 184,
        "question_text": "Formaldehyde reacts with which compound to give urotropine?:",
        "option_a": "Ammonia",
        "option_b": "Ammonium hydroxide",
        "option_c": "Methylamine",
        "option_d": "Ammonium chloride",
        "correct_option": "A",
        "explanation": "Formaldehyde reacts with ammonia to form hexamethylenetetramine (urotropine): 6HCHO + 4NH3 -> (CH2)6N4 + 6H2O. Urotropine is an important urinary antiseptic.",
        "topic": "Aldehydes and Ketones",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2025_CHEM_185",
        "question_number": 185,
        "question_text": "The number of co-ordinated water molecules in \\text{CuSO}_4 \\cdot 5\\text{H}_2\\text{O} is:",
        "option_a": "4",
        "option_b": "3",
        "option_c": "2",
        "option_d": "1",
        "correct_option": "A",
        "explanation": "In copper sulfate pentahydrate, the formula is [Cu(H2O)4]SO4 · H2O. Four water molecules are coordinated directly to the Cu^(2+) ion, while the fifth is hydrogen bonded to the sulfate ion.",
        "topic": "Coordination Compounds / Chemical Bonding",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2025_CHEM_186",
        "question_number": 186,
        "question_text": "\\text{O}_2^- ion is:",
        "option_a": "Paramagnetic and having bond order 1.5",
        "option_b": "Diamagnetic and having bond order 1",
        "option_c": "Paramagnetic and having bond order 2",
        "option_d": "Paramagnetic and having bond order 2.5",
        "correct_option": "A",
        "explanation": "Superoxide ion O2^- has 17 electrons. According to Molecular Orbital theory, Bond Order = (10 - 7)/2 = 1.5. It has one unpaired electron in a π* antibonding orbital, so it is paramagnetic.",
        "topic": "Chemical Bonding / Molecular Orbital Theory",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2025_CHEM_187",
        "question_number": 187,
        "question_text": "The quantity of electricity needed to reduce 1 mol of \\text{Cr}_2\\text{O}_7^{2-} is:",
        "option_a": "12F",
        "option_b": "4F",
        "option_c": "6F",
        "option_d": "2F",
        "correct_option": "C",
        "explanation": "The half reaction is Cr2O7^(2-) + 14H^+ + 6e^- -> 2Cr^(3+) + 7H2O. Each mole of Cr2O7^(2-) requires 6 moles of electrons, which equals 6 Faradays (6F).",
        "topic": "Electrochemistry / Faraday's Laws",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_188",
        "question_number": 188,
        "question_text": "The \\text{p}K_a of an acid and \\text{p}K_b of a base are 4.28 and 4.27 respectively. The pH of corresponding salt formed is:",
        "option_a": "6.995",
        "option_b": "7.005",
        "option_c": "11.775",
        "option_d": "7.050",
        "correct_option": "B",
        "explanation": "For a salt of weak acid and weak base: pH = 7 + (1/2)(pKa - pKb) = 7 + 0.5 * (4.28 - 4.27) = 7 + 0.005 = 7.005.",
        "topic": "Ionic Equilibrium / Salt Hydrolysis",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_189",
        "question_number": 189,
        "question_text": "The conjugate base of \\text{NH}_3 is:",
        "option_a": "\\text{NH}_4\\text{OH}",
        "option_b": "\\text{NH}_4^+",
        "option_c": "\\text{NH}_2^-",
        "option_d": "\\text{N}_2\\text{H}_4",
        "correct_option": "C",
        "explanation": "A conjugate base is formed by removal of a proton (H^+) from an acid: NH3 - H^+ -> NH2^- (amide ion).",
        "topic": "Ionic Equilibrium / Acids and Bases",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_190",
        "question_number": 190,
        "question_text": "The value of K_c for the reaction 2\\text{NOCl}(g) \\rightleftharpoons 2\\text{NO}(g) + \\text{Cl}_2(g) at 500K where K_p = 1.8 \\times 10^{-2} is:",
        "option_a": "8.3 \\times 10^{-4} \\text{ mol L}^{-1}",
        "option_b": "0.43 \\times 10^{-4} \\text{ mol L}^{-1}",
        "option_c": "2.15 \\times 10^{-4} \\text{ mol L}^{-1}",
        "option_d": "4.3 \\times 10^{-4} \\text{ mol L}^{-1}",
        "correct_option": "D",
        "explanation": "Δn_g = (2+1) - 2 = 1. K_p = K_c (RT)^1 => K_c = K_p / (RT). With R = 0.0831 L bar K^(-1) mol^(-1) and T = 500 K: RT = 41.55. K_c = (1.8e-2) / 41.55 = 4.33e-4 mol L^(-1).",
        "topic": "Chemical Equilibrium",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2025_CHEM_191",
        "question_number": 191,
        "question_text": "32g of methanol contains as many molecules as contained in:",
        "option_a": "32g of ammonia",
        "option_b": "32g of water",
        "option_c": "32g of sulphuric acid",
        "option_d": "32g of oxygen gas",
        "correct_option": "D",
        "explanation": "Molar mass of methanol (CH3OH) = 32 g/mol, so 32 g is 1 mole (N_A molecules). Molar mass of O2 = 32 g/mol, so 32 g of O2 is also 1 mole (N_A molecules).",
        "topic": "Some Basic Concepts of Chemistry / Mole Concept",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_192",
        "question_number": 192,
        "question_text": "The IUPAC name of [\\text{Co}(\\text{NH}_3)_5\\text{Cl}]\\text{Cl}_2 is:",
        "option_a": "Pentaamminechloridocobaltate(III) chloride",
        "option_b": "Chloridopentaamminecobalt(III) chloride",
        "option_c": "Pentaamminechloridocobalt(III) chloride",
        "option_d": "Pentaamminechloridocobalt(III) dichloride",
        "correct_option": "C",
        "explanation": "Cation is complex: Pentaamminechloridocobalt(III), and anion is simple: chloride. Hence, Pentaamminechloridocobalt(III) chloride.",
        "topic": "Coordination Compounds / IUPAC Nomenclature",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_193",
        "question_number": 193,
        "question_text": "Which shows the correct order of increasing boiling point?:",
        "option_a": "Methoxymethane < propanal < propan-1-ol",
        "option_b": "Methoxymethane < propan-1-ol < propanal",
        "option_c": "Propanal < methoxymethane < propan-1-ol",
        "option_d": "Propanal < propan-1-ol < methoxymethane",
        "correct_option": "A",
        "explanation": "Propan-1-ol has intermolecular hydrogen bonding (highest b.p.). Propanal has dipole-dipole attractions. Methoxymethane has weak dipole attractions. Therefore: Methoxymethane < propanal < propan-1-ol.",
        "topic": "Alcohols, Phenols and Ethers / Organic Chemistry",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2025_CHEM_194",
        "question_number": 194,
        "question_text": "The spin-only magnetic moment of \\text{M}^{2+} ion (Z = 28) is:",
        "option_a": "2.87 B.M.",
        "option_b": "0 B.M.",
        "option_c": "5.37 B.M.",
        "option_d": "3.87 B.M.",
        "correct_option": "A",
        "explanation": "For Z = 28 (Ni), M^(2+) configuration is [Ar] 3d^8 with 2 unpaired electrons (n = 2). Spin-only magnetic moment μ = √(n(n+2)) = √(2 * 4) = √8 ≈ 2.83 - 2.87 B.M.",
        "topic": "d and f Block Elements / Coordination Chemistry",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_195",
        "question_number": 195,
        "question_text": "On hydrogenation, ethene gives:",
        "option_a": "Ethyne",
        "option_b": "Butane",
        "option_c": "Methane",
        "option_d": "Ethane",
        "correct_option": "D",
        "explanation": "Hydrogenation of ethene (C2H4 + H2) in presence of Ni/Pt catalyst gives ethane (C2H6).",
        "topic": "Hydrocarbons / Alkenes",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_196",
        "question_number": 196,
        "question_text": "The correct value of wavelength of light wave having period of 2.0 \\times 10^{-10} s is:",
        "option_a": "6.0 \\times 10^{-2} m",
        "option_b": "6.0 \\times 10^{-4} m",
        "option_c": "6.0 \\times 10^{-1} m",
        "option_d": "6.0 \\times 10^{-5} m",
        "correct_option": "A",
        "explanation": "Wavelength λ = c * T = (3.0 * 10^8 m/s) * (2.0 * 10^(-10) s) = 6.0 * 10^(-2) m.",
        "topic": "Structure of Atom / Wave Nature of Light",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_197",
        "question_number": 197,
        "question_text": "The value of Van't Hoff factor (i) in case of complete dissociation of \\text{AlCl}_3 is:",
        "option_a": "2",
        "option_b": "4",
        "option_c": "8",
        "option_d": "3",
        "correct_option": "B",
        "explanation": "AlCl3 dissociates into 1 Al^(3+) ion and 3 Cl^- ions, total 4 ions. For 100% dissociation, i = 4.",
        "topic": "Solutions / Colligative Properties",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_198",
        "question_number": 198,
        "question_text": "Haloalkanes react with \\text{AgCN} to form:",
        "option_a": "Alkyl isocyanide",
        "option_b": "Alkyl aryl isocyanide",
        "option_c": "Alkyl aryl cyanide",
        "option_d": "Alkyl cyanide",
        "correct_option": "A",
        "explanation": "AgCN is predominantly covalent, so nitrogen atom attacks with its lone pair, forming alkyl isocyanide (R-NC).",
        "topic": "Haloalkanes and Haloarenes",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2025_CHEM_199",
        "question_number": 199,
        "question_text": "Chloroform on decomposition in the presence of air or light gives hydrogen chloride gas along with a poisonous gas having chemical formula:",
        "option_a": "\\text{CO}",
        "option_b": "\\text{COCl}_3",
        "option_c": "\\text{COCl}_2",
        "option_d": "\\text{CH}_3\\text{NC}",
        "correct_option": "C",
        "explanation": "Oxidation of chloroform (CHCl3) produces phosgene gas (carbonyl chloride, COCl2): 2CHCl3 + O2 -> 2COCl2 + 2HCl.",
        "topic": "Haloalkanes and Haloarenes",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2025_CHEM_200",
        "question_number": 200,
        "question_text": "Glucose is oxidised into Gluconic acid by Tollen's reagent. This can be identified through:",
        "option_a": "Evolution of a gas",
        "option_b": "Formation of yellow precipitate",
        "option_c": "Formation of red precipitate",
        "option_d": "Formation of silver mirror",
        "correct_option": "D",
        "explanation": "Tollen's reagent is reduced to metallic silver by the aldehyde group of glucose, forming a shiny silver mirror on the test tube wall.",
        "topic": "Biomolecules / Carbohydrates",
        "difficulty": "Easy"
    }
]

def run_import():
    year = 2025
    section = "Chemistry"
    print(f"Importing {len(chemistry_questions)} questions for {year} - {section}...")
    for q in chemistry_questions:
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
    print("Import complete! Current Stats across all years:")
    for stat in get_stats():
        print(f"Year: {stat['year']} | Section: {stat['section']} | Questions: {stat['count']}")

if __name__ == "__main__":
    run_import()
