class Carnivore:
    def parse_input(file_path):
        entries = []

        with open(file_path, 'r') as file:

            for line in file:
                if line.strip():
                    date, name, amount, price = line.strip().split(';')
                    entries.append((date, name, float(amount), float(price)))
                    
        return entries