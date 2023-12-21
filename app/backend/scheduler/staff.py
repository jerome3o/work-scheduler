from models import TaskType

SKILLSET_MAP = {
    "Doctors": [TaskType.DOCTOR],
    "Pharmacy": [TaskType.PHARMACY],
    "Vanessa": [TaskType.NURSE, TaskType.PORTACATH, TaskType.PAEDS_PORT, TaskType.SPIRO, TaskType.SPUTUM, TaskType.CYTOTOXIC, TaskType.JAIPUR, TaskType.BREEZING, TaskType.INFUSION, TaskType.MISSION, TaskType.DOMINO_SPIRO],
    "Angelo": [TaskType.NURSE, TaskType.PORTACATH, TaskType.PAEDS_PORT, TaskType.SPIRO, TaskType.SPUTUM, TaskType.CYTOTOXIC, TaskType.JAIPUR, TaskType.OSPREY, TaskType.BREEZING, TaskType.INFUSION, TaskType.MISSION_ECG, TaskType.DOMINO_SPIRO],
    "Florence": [TaskType.NURSE, TaskType.PAEDS_PORT, TaskType.SPIRO, TaskType.SPUTUM, TaskType.JAIPUR, TaskType.OSPREY, TaskType.BREEZING, TaskType.INFUSION, TaskType.MISSION_ECG, TaskType.DOMINO_SPIRO],
    "Lila": [TaskType.NURSE, TaskType.PAEDS_PORT, TaskType.SPIRO, TaskType.SPUTUM, TaskType.JAIPUR, TaskType.BREEZING, TaskType.INFUSION],
    "Spyke": [TaskType.NURSE, TaskType.ANY],
    "Candice": [TaskType.NURSE, TaskType.ANY],
    "Caroline": [TaskType.NURSE, TaskType.ANY],
    "Diana": [TaskType.NURSE, TaskType.ANY, TaskType.SPUTUM],
    "Annabel": [TaskType.NURSE, TaskType.ANY],
    "Jane": [TaskType.NURSE, TaskType.ANY],
    "Joevily": [TaskType.NURSE, TaskType.ANY],
    "Klaudinne": [TaskType.NURSE, TaskType.ANY],
    "Marlies": [TaskType.NURSE, TaskType.ANY],
    "Mary-Anne": [TaskType.NURSE, TaskType.ANY],
    "Robynne": [TaskType.NURSE, TaskType.ANY],
    "Ting": [TaskType.NURSE, TaskType.ANY, TaskType.SPIRO],
    "Perry": [TaskType.NURSE, TaskType.ANY],
    "Rachel": [TaskType.NURSE, TaskType.ANY],
    "Sian": [TaskType.NURSE, TaskType.ANY],
    "Jhon": [TaskType.NURSE, TaskType.ANY],
    "Sam": [TaskType.NURSE, TaskType.ANY],
    "Esther": [TaskType.NURSE, TaskType.ANY],
    "Saumi": [TaskType.NURSE, TaskType.ANY],
    "Jules": [TaskType.NURSE, TaskType.ANY],
    "Janine": [TaskType.NURSE, TaskType.ANY],
    "Alvin": [TaskType.NURSE, TaskType.ANY],
    "McKayla": [TaskType.NURSE, TaskType.ANY],
    "Ed": [TaskType.NURSE, TaskType.ANY],
    "Maricar": [TaskType.NURSE, TaskType.ANY],
    "Vanne": [TaskType.NURSE, TaskType.ANY],
    "Tim": [TaskType.NURSE, TaskType.ANY],
    "Gie": [TaskType.NURSE, TaskType.ANY],
    "Gaile": [TaskType.NURSE, TaskType.ANY],
    "Christina": [TaskType.CRT, TaskType.ANY],
    "Daissny": [TaskType.CRT, TaskType.ANY],
    "Ephraim": [TaskType.CRT, TaskType.ANY],
    "Gaps": [TaskType.CRT, TaskType.ANY],
    "Joys": [TaskType.CRT, TaskType.ANY],
    "Nathan": [TaskType.CRT, TaskType.ANY, TaskType.PHLEBOTOMY],
    "Quennie": [TaskType.CRT, TaskType.ANY],
    "Renee": [TaskType.CRT, TaskType.ANY],
    "Sami": [TaskType.CRT, TaskType.ANY],
    "Shameel": [TaskType.CRT, TaskType.ANY],
    "Tia": [TaskType.CRT, TaskType.ANY],
    "Hannah": [TaskType.CRT, TaskType.ANY, TaskType.PHLEBOTOMY],
    "MJ": [TaskType.CRT, TaskType.ANY],
    "Cris": [TaskType.CRT, TaskType.ANY],
    "Acima": [TaskType.CRT, TaskType.ANY],
    "Kirtesh": [TaskType.CRT, TaskType.ANY],
    "Mele": [TaskType.CRT, TaskType.ANY],
    "Pinal": [TaskType.CRT, TaskType.ANY],
    "Shella": [TaskType.CRT, TaskType.ANY],
    "Olivia": [TaskType.ANY],
}