# Function to trim leading and trailing whitespace from a string
trim() {
    local var="$*"
    # remove leading whitespace characters
    var="${var#"${var%%[![:space:]]*}"}"
    # remove trailing whitespace characters
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <csv_file>"
    exit 1
fi

csv_file=$1

# Read the CSV file line by line
while IFS=, read -r pdf_url save_path
do
    # Skip the header line
    if [[ "$pdf_url" == "pdf_url" && "$save_path" == "save_path" ]]; then
        continue
    fi

    # Trim leading and trailing whitespace from pdf_url and save_path
    pdf_url=$(trim "$pdf_url")
    save_path=$(trim "$save_path")

    # Create the directory if it does not exist
    dir=$(dirname "$save_path")
    mkdir -p "$dir"

    # Download the PDF
    curl -o "$save_path" "$pdf_url"

    # Check if the download was successful
    if [ $? -ne 0 ]; then
        echo "Failed to download $pdf_url"
    else
        echo "Successfully downloaded $pdf_url to $save_path"
    fi

done < "$csv_file"
