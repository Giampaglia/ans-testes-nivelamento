def replace_abbreviations(data):
    """Substitui as abreviações 'OD' e 'AMB' pelas descrições completas."""
    for i, row in enumerate(data):
        if 'OD' in row:
            row[row.index('OD')] = 'Odontologia'
        if 'AMB' in row:
            row[row.index('AMB')] = 'Ambulatório'
    return data
