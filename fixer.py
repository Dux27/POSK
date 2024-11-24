file_name = "calculator.py"

with open(file_name, "r") as file:
    lines = file.readlines()

# Replace tabs with 4 spaces
with open(file_name, "w") as file:
    for line in lines:
        file.write(line.replace("\t", "    "))