import codecs

# Function to read a file and return its contents as a string
def read_file(path):
    with codecs.open(path, "r", encoding="utf-8-sig") as f:
        # Read and return the text content from the file
        text = f.read()
        return text


# Function to write the result (encrypted or decrypted text) to a new file
def write_result_file(path: str, string, encrypt=True):
    # Determine the file extension based on encryption or decryption
    extension = "enc" if encrypt else "dec"

    # Generate the new file path by replacing the original file's extension with '.enc' or '.dec'
    new_path = f"{path.rsplit('.', 1)[0]}.{extension}"

    # Open the new file in write mode and save the result
    with open(f'{new_path}', "w", encoding='utf-8') as file:
        file.write(string)
        # Print a success message with the file's path
        print(f"{extension}ryption Successfully wrote to {new_path}")
