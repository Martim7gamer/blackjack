input_string = "{}"

# Step 1: Remove the curly braces and split by commas to get each record
records = input_string.strip('{}').split('},{')

# Step 2: Initialize a list to hold all dictionaries
all_dicts = []

# Step 3: Process each record
for record in records:
    # Step 4: Split by semicolons to get key-value pairs
    pairs = record.split(';')
    # Step 5: Create a dictionary for the current record
    record_dict = {}
    for pair in pairs:
        # Step 6: Split by colon to get the key and value
        key, value = pair.split(':')
        # Store the key-value pair in the dictionary
        record_dict[key] = value
    # Add the current record dictionary to the list
    all_dicts.append(record_dict)

# Now `all_dicts` contains all the records as dictionaries
print(all_dicts)