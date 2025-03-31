import csv

def save_to_csv(data, output_path):
    """Salva os dados extraídos em um arquivo CSV."""
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
