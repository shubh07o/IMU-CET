import sqlite3
import json
from db_manager import add_question, export_to_json, get_stats

chemistry_questions = [
    {
        "q_id": "IMU_2026_S2_CHEM_181",
        "question_number": 181,
        "question_text": "Reaction of phenol with chloroform and sodium hydroxide followed by acidification gives salicylaldehyde. Which one of the following electrophile is involved?",
        "option_a": ":CCl₂ (Dichlorocarbene)",
        "option_b": "⁺CCl₂",
        "option_c": "⁺CHO",
        "option_d": ":CH₂",
        "correct_option": "A",
        "explanation": "In the Reimer-Tiemann reaction, chloroform reacts with NaOH via alpha-elimination to generate neutral dichlorocarbene (:CCl2), which acts as the electrophile attacking the phenoxide ring.",
        "topic": "Organic Chemistry / Phenols & Reimer-Tiemann Reaction",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_182",
        "question_number": 182,
        "question_text": "Which of the following elements has the highest negative electron gain enthalpy?",
        "option_a": "Fluorine",
        "option_b": "Chlorine",
        "option_c": "Oxygen",
        "option_d": "Sulfur",
        "correct_option": "B",
        "explanation": "Chlorine has the highest negative electron gain enthalpy (-349 kJ/mol) because fluorine's compact 2p subshell suffers strong interelectronic repulsions.",
        "topic": "Periodic Properties / Electron Gain Enthalpy",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_183",
        "question_number": 183,
        "question_text": "According to Bohr's theory, the angular momentum of an electron in 5th orbit is:",
        "option_a": "2.5 h / π",
        "option_b": "25 h / π",
        "option_c": "10 h / π",
        "option_d": "1.5 h / π",
        "correct_option": "A",
        "explanation": "Bohr's quantization postulate: L = nh/(2π). For n = 5: L = 5h/(2π) = 2.5h/π.",
        "topic": "Structure of Atom / Bohr Model",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_184",
        "question_number": 184,
        "question_text": "Which of the following statements is not true about glucose?",
        "option_a": "On heating with HI it forms n-hexane.",
        "option_b": "It does not give Schiff's test.",
        "option_c": "It exists in furanose form.",
        "option_d": "It is an aldohexose.",
        "correct_option": "C",
        "explanation": "Glucose predominantly exists in the six-membered cyclic pyranose form (glucopyranose), not furanose. Hence statement (C) is incorrect.",
        "topic": "Biomolecules / Carbohydrates & Glucose",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_185",
        "question_number": 185,
        "question_text": "Basic strength of different alkyl amines depends upon:",
        "option_a": "+I effect",
        "option_b": "steric effect",
        "option_c": "solvation effect",
        "option_d": "all of these",
        "correct_option": "D",
        "explanation": "In aqueous solution, the basicity of alkylamines is governed by an interplay of inductive (+I) effect, steric hindrance, and hydration/solvation energy.",
        "topic": "Organic Chemistry / Amines & Basic Strength",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_186",
        "question_number": 186,
        "question_text": "Which of the following will not undergo HVZ reaction?",
        "option_a": "ethanoic acid",
        "option_b": "propanoic acid",
        "option_c": "2-methylpropanoic acid",
        "option_d": "2,2-dimethylpropanoic acid",
        "correct_option": "D",
        "explanation": "Hell-Volhard-Zelinsky (HVZ) reaction requires an alpha-hydrogen atom. 2,2-dimethylpropanoic acid ((CH3)3CCOOH) has no alpha-hydrogen and cannot undergo this reaction.",
        "topic": "Carboxylic Acids / Hell-Volhard-Zelinsky Reaction",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_187",
        "question_number": 187,
        "question_text": "The unit of rate constant for the reaction \\(2\\text{H}_2 + 2\\text{NO} \\to 2\\text{H}_2\\text{O} + \\text{N}_2\\), which has \\(\\text{rate} = k[\\text{H}_2][\\text{NO}]^2\\), is:",
        "option_a": "mol L⁻¹",
        "option_b": "s⁻¹",
        "option_c": "mol⁻² L² s⁻¹",
        "option_d": "mol L⁻¹ s⁻¹",
        "correct_option": "C",
        "explanation": "Overall order is n = 1 + 2 = 3. Unit of rate constant k = (mol/L)^(1-3) s^-1 = mol^-2 L^2 s^-1.",
        "topic": "Chemical Kinetics / Rate Constant Units",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_188",
        "question_number": 188,
        "question_text": "If the heat of combustion of methane (\\(\\text{CH}_4\\)) is -890 kJ/mol, how much heat is released when 8g of methane is completely burned? (Molar mass of \\(\\text{CH}_4 = 16\\text{ g/mol}\\)):",
        "option_a": "-445 kJ",
        "option_b": "-225.5 kJ",
        "option_c": "-1780 kJ",
        "option_d": "-890 kJ",
        "correct_option": "A",
        "explanation": "Moles of CH4 = 8/16 = 0.5 mol. Heat released = 0.5 * (-890 kJ) = -445 kJ.",
        "topic": "Thermodynamics / Enthalpy of Combustion",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_189",
        "question_number": 189,
        "question_text": "The complex ions \\([\\text{Co}(\\text{NH}_3)_5(\\text{NO}_2)]^{2+}\\) and \\([\\text{Co}(\\text{NH}_3)_5(\\text{ONO})]^{2+}\\) are called:",
        "option_a": "Geometrical isomers",
        "option_b": "Ionization isomers",
        "option_c": "Linkage isomers",
        "option_d": "Co-ordination isomers",
        "correct_option": "C",
        "explanation": "Nitrite is an ambidentate ligand coordinating via N (-NO2) or O (-ONO). Complexes differing in this donor atom attachment are linkage isomers.",
        "topic": "Coordination Compounds / Isomerism",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_190",
        "question_number": 190,
        "question_text": "Mass of \\(\\text{CO}_2\\) is 88 g. The number of atoms of oxygen present in it, as:",
        "option_a": "1.2 × 10²³",
        "option_b": "1.4 × 10²³",
        "option_c": "2.41 × 10²⁴",
        "option_d": "2.41 × 10²³",
        "correct_option": "C",
        "explanation": "Moles of CO2 = 88/44 = 2 mol. Moles of oxygen atoms = 2 * 2 = 4 mol. Number of oxygen atoms = 4 * 6.022 * 10^23 = 2.4088 * 10^24 ≈ 2.41 * 10^24.",
        "topic": "Some Basic Concepts of Chemistry / Mole Concept",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_191",
        "question_number": 191,
        "question_text": "For the galvanic cell \\(\\text{Zn} / \\text{Zn}^{2+}(0.1\\text{M}) // \\text{Cu}^{2+}(1.0\\text{M}) / \\text{Cu}\\) the cell potential increases if:",
        "option_a": "Surface area of anode is increased",
        "option_b": "\\([\\text{Cu}^{2+}]\\) is decreased",
        "option_c": "\\([\\text{Cu}^{2+}]\\) is increased",
        "option_d": "\\([\\text{Zn}^{2+}]\\) is increased",
        "correct_option": "C",
        "explanation": "Nernst equation: E_cell = E°_cell - (0.0591/2)*log([Zn2+]/[Cu2+]). Increasing [Cu2+] reduces the reaction quotient Q, increasing E_cell.",
        "topic": "Electrochemistry / Nernst Equation",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_192",
        "question_number": 192,
        "question_text": "The number of radial nodes for a 3p orbital is:",
        "option_a": "2",
        "option_b": "1",
        "option_c": "0",
        "option_d": "3",
        "correct_option": "B",
        "explanation": "Radial nodes = n - l - 1. For 3p orbital (n = 3, l = 1): Radial nodes = 3 - 1 - 1 = 1.",
        "topic": "Structure of Atom / Radial Nodes",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_193",
        "question_number": 193,
        "question_text": "Which of the following cannot be made by using Williamson's synthesis?",
        "option_a": "Di-tert-butyl ether",
        "option_b": "Tert-butyl ethyl ether",
        "option_c": "Methoxybenzene",
        "option_d": "Allyl methyl ether",
        "correct_option": "A",
        "explanation": "Williamson ether synthesis involves SN2 displacement on an alkyl halide. 3° alkyl halides undergo E2 elimination instead of SN2 substitution, so di-tert-butyl ether cannot be prepared by Williamson synthesis.",
        "topic": "Organic Chemistry / Ethers & Williamson Synthesis",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_194",
        "question_number": 194,
        "question_text": "\\([\\text{EDTA}]^{4-}\\) is a:",
        "option_a": "quadridentate ligand",
        "option_b": "bidentate ligand",
        "option_c": "hexadentate ligand",
        "option_d": "monodentate ligand",
        "correct_option": "C",
        "explanation": "[EDTA]4- possesses six donor sites (two nitrogen atoms and four carboxylate oxygen atoms), making it a hexadentate chelating ligand.",
        "topic": "Coordination Compounds / Ligands & Denticity",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_195",
        "question_number": 195,
        "question_text": "The IUPAC name of 3-methylcyclohex-1-ene is:",
        "option_a": "1-methyl cyclohex-2-ene",
        "option_b": "1-methyl cyclohex-5-ene",
        "option_c": "6-methyl cyclohex-1-ene",
        "option_d": "3-Methyl cyclohex-1-ene",
        "correct_option": "D",
        "explanation": "The alkene double bond carbons get locants 1 and 2, numbering in the direction of the methyl group to give it the lower locant 3: 3-methylcyclohex-1-ene.",
        "topic": "Organic Chemistry / IUPAC Nomenclature",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_196",
        "question_number": 196,
        "question_text": "Lanthanoid contraction is due to:",
        "option_a": "Effective shielding of 4f electrons",
        "option_b": "Poor shielding of 4f electrons",
        "option_c": "Poor shielding of 5d electrons",
        "option_d": "Increase in nuclear charge only",
        "correct_option": "B",
        "explanation": "The imperfect and poor shielding effect of 4f electrons causes the increasing nuclear charge to exert a greater attraction on the outer 6s electrons, shrinking atomic and ionic radii.",
        "topic": "d and f Block Elements / Lanthanoid Contraction",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_197",
        "question_number": 197,
        "question_text": "Which of the following shows \\(dsp^2\\) hybridisation and a square planar geometry?",
        "option_a": "\\(\\text{SF}_6\\)",
        "option_b": "\\(\\text{PCl}_5\\)",
        "option_c": "\\([\\text{Ni}(\\text{CN})_4]^{2-}\\)",
        "option_d": "\\(\\text{BrF}_5\\)",
        "correct_option": "C",
        "explanation": "In [Ni(CN)4]2-, Ni2+ (3d8) pairs up under the strong crystal field of CN-, leaving one 3d orbital empty to form dsp2 hybrid orbitals with square planar geometry.",
        "topic": "Coordination Compounds / Valence Bond Theory",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_198",
        "question_number": 198,
        "question_text": "There are two beakers 'A' and 'B' containing \\(\\text{KCl}\\) and \\(\\text{CH}_3\\text{COOH}\\) solutions respectively. On adding water to beakers A and B, which of the following change in \\(\\Lambda_m\\) of the solutions will be correct?",
        "option_a": "It decreases in beaker A but no change in beaker B.",
        "option_b": "There is no change in beaker A but it decreases slowly in beaker B.",
        "option_c": "It increases slowly in beaker A and sharply in beaker B.",
        "option_d": "It increases sharply in beaker A and slowly in beaker B.",
        "correct_option": "C",
        "explanation": "KCl is a strong electrolyte whose molar conductivity increases slowly with dilution due to reduced interionic attractions. CH3COOH is a weak electrolyte whose degree of dissociation increases dramatically upon dilution, causing a sharp rise in molar conductivity.",
        "topic": "Electrochemistry / Molar Conductivity & Dilution",
        "difficulty": "Medium"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_199",
        "question_number": 199,
        "question_text": "Which of the following transition metal ions has highest magnetic moment?",
        "option_a": "\\(\\text{Cu}^{2+}\\)",
        "option_b": "\\(\\text{Ni}^{2+}\\)",
        "option_c": "\\(\\text{Co}^{2+}\\)",
        "option_d": "\\(\\text{Fe}^{2+}\\)",
        "correct_option": "D",
        "explanation": "Fe2+ (3d6) has 4 unpaired electrons (spin-only magnetic moment μ = sqrt(4*6) = sqrt(24) ≈ 4.90 BM), which is higher than Co2+ (3), Ni2+ (2), and Cu2+ (1).",
        "topic": "d and f Block Elements / Magnetic Moment",
        "difficulty": "Easy"
    },
    {
        "q_id": "IMU_2026_S2_CHEM_200",
        "question_number": 200,
        "question_text": "Which of the following cell is used in inverter?",
        "option_a": "Lead storage cell",
        "option_b": "Mercury cell",
        "option_c": "Fuel cell",
        "option_d": "Dry cell",
        "correct_option": "A",
        "explanation": "The lead storage battery is a rechargeable secondary cell that supplies heavy electrical currents and is universally used in domestic inverters and automobiles.",
        "topic": "Electrochemistry / Commercial Cells & Batteries",
        "difficulty": "Easy"
    }
]

def run_import():
    year = 2026
    shift = "Shift 2"
    section = "Chemistry"
    print(f"Importing {len(chemistry_questions)} questions for {year} ({shift}) - {section}...")
    
    # Check for ID collisions
    ids = [q["q_id"] for q in chemistry_questions]
    assert len(ids) == len(set(ids)), "Duplicate q_ids found in import list!"
    
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
    export_to_json(year, shift)
    print("Import complete! Current Stats across all years & shifts:")
    for stat in get_stats():
        print(f"Year: {stat['year']} | Shift: {stat['shift']} | Section: {stat['section']} | Questions: {stat['count']}")

if __name__ == "__main__":
    run_import()
