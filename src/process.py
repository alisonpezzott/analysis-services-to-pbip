# Requires Python 3.8 or later

import re
import os
import json
import glob
import shutil

# Constants for input and output paths
# These paths should be set according to your directory structure
input_path = "workspace"
output_path = "PBIP"
default_report_path = "src/Default.Report"


def update_database_tmdl(file_path):
    """
    Updates the value of compatibilityLevel from 1500 to 1550 in the specified file.
    
    Parameters:
        file_path (str): Path to the database.tmdl file.
        
    Returns:
        str: Updated content of the file.
    """
    # Reads the content of the file
    try:
        with open(f"{file_path}/database.tmdl", "r", encoding="utf-8") as f:
            content = f.read()
    except IOError as e:
        print(f"Error reading the file: {e}")
        return None

    # Performs the substitution using a regular expression to find "compatibilityLevel: 1500"
    new_content = re.sub(r'(compatibilityLevel:\s*)1500', r'\g<1>1550', content)
    
    # Saves the modifications back to the same file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("File updated successfully.")
    except IOError as e:
        print(f"Error writing to the file: {e}")
        return None
    
    return new_content


def delete_definition_datasources(file_path):
    """
    Deletes the specified file.
    
    Parameters:
        file_path (str): Path of the file to delete.
    """
    try:
        os.remove(f"{file_path}/datasources.tmdl")
        print(f"File '{file_path}/datasources.tmdl' successfully deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}/datasources.tmdl' not found.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")


def clean_definition_model(file_path):
    """
    Reads a .tmdl file and filters its content to keep only lines that start with the allowed keywords.
    The allowed keywords are:
        - model
        - culture
        - defaultPowerBIDataSourceVersion
        - discourageImplicitMeasures
        - ref
    
    Parameters:
        file_path (str): Path of the file to filter.
    
    The file is overwritten with the filtered content.
    """
    allowed_keywords = [
        "model",
        "culture",
        "defaultPowerBIDataSourceVersion",
        "discourageImplicitMeasures",
        "ref"
    ]
    
    try:
        # Read all lines from the file.
        with open(f"{file_path}/model.tmdl", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as e:
        print(f"Error reading file {file_path}/model.tmdl: {e}")
        return None
    
    # Filter lines: keep lines that start with any of the allowed keywords after stripping leading whitespace.
    filtered_lines = [
        line for line in lines
        if any(line.lstrip().startswith(keyword) for keyword in allowed_keywords)
    ]
    
    try:
        # Write the filtered lines back to the file.
        with open(f"file_path/model.tmdl", "w", encoding="utf-8") as file:
            file.writelines(filtered_lines)
        print(f"File '{file_path}/model.tmdl' successfully updated with filtered content.")
    except IOError as e:
        print(f"Error writing to file {file_path}/model.tmdl: {e}")
        return None
    
    return filtered_lines


def transform_table_file(file_path):
    """
    Transforms the .tmdl file by:
    
    1. Removing lines that start with "sourceProviderType".
    2. For each column, capturing the corresponding sourceColumn to create an SQL query columns string.
       Format: "[sourceColumn] AS [column]" for each column.
    3. Capturing in the dataSource line the text before the first space as the variable 'server'.
    4. Capturing from the annotation (TabularEditor_TableSchema) the keys:
         - "Name"  as variable table
         - "Schema" as variable schema
         - "Database" as variable database
    5. Deleting everything from the partition block until the end of the file.
    6. Appending a new partition block with the following template:
    
       partition <table> = m
           mode: import
           source =
               let
                   Source = Sql.Database("&<server>&", <database>, [Query = "SELECT <columns> FROM "["&<schema>&"]"."["&<table>&"]", CreateNavigationProperties=false])
               in
                   Source
    
    Parameters:
        file_path (str): Path to the .tmdl file.
    
    Returns:
        The new content of the file as a string.
    """
    # Read the file content
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Initialize variables to collect column mappings and header lines
    column_mappings = []  # Each element will be (sourceColumn, columnName)
    new_lines = []        # Lines to keep (everything before the partition block)
    current_column = None
    partition_start_index = None  # Index where the partition block starts

    # Process the file until the partition block is encountered
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        # Check if we have reached the partition block; if so, stop processing further
        if stripped.startswith("partition "):
            partition_start_index = i
            break
        
        # Delete lines starting with "sourceProviderType"
        if stripped.startswith("sourceProviderType"):
            continue
        
        # Capture column definitions
        if stripped.startswith("column "):
            # Expecting: "column ColumnName"
            parts = stripped.split()
            if len(parts) >= 2:
                current_column = parts[1].strip()
            else:
                current_column = None
        
        # Capture the sourceColumn for the current column block
        if stripped.startswith("sourceColumn:") and current_column:
            match = re.search(r'sourceColumn:\s*(\S+)', stripped)
            if match:
                source_col = match.group(1).strip()
                column_mappings.append((source_col, current_column))
        
        # Keep the current line (if it wasn’t filtered)
        new_lines.append(line)
    
    # Variables to capture server and table metadata from the partition block
    server = None
    table = None
    schema = None
    database = None
    
    # Process the partition block (if present)
    if partition_start_index is not None:
        partition_block = lines[partition_start_index:]
        for line in partition_block:
            # Look for the dataSource line and extract text between quotes
            if "dataSource:" in line:
                ds_match = re.search(r"dataSource:\s*'([^']+)'", line)
                if ds_match:
                    ds_value = ds_match.group(1)
                    # Get the text before the first space as server
                    server = ds_value.split()[0]
            # Look for the annotation for table schema
            if "annotation TabularEditor_TableSchema" in line:
                # Extract the JSON part (anything between the first '{' and the last '}')
                json_match = re.search(r'annotation TabularEditor_TableSchema\s*=\s*(\{.*\})', line)
                if json_match:
                    json_str = json_match.group(1)
                    try:
                        table_schema = json.loads(json_str)
                        table = table_schema.get("Name")
                        schema = table_schema.get("Schema")
                        database = table_schema.get("Database")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON in TableSchema: {e}")
    
    # Build the SQL columns string using the captured column mappings
    # Format each mapping as: [sourceColumn] AS [columnName]
    columns_parts = [f'[{src}] AS [{col}]' for src, col in column_mappings]
    columns_str = ", ".join(columns_parts)
    
    # At this point, new_lines holds all the lines before the partition block.
    # We now prepare the new partition block string.
    if not (server and table and schema and database):
        print("Error: Failed to extract all required metadata from partition block.")
        return None
    
    new_partition_block = f"""
    partition {table} = m
        mode: import
        source =
            let
                Source = Sql.Database("{server}", "{database}", [Query = "SELECT {columns_str} FROM [{schema}].[{table}]", CreateNavigationProperties=false])
            in
                Source
    """
    # Combine the header part (with columns, etc.) with the new partition block.
    header_content = "".join(new_lines).rstrip()  # Remove trailing whitespace/newlines
    new_content = header_content + "\n\n" + new_partition_block
    
    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("File transformed successfully.")
    return new_content


def process_all_table_files(base_path):
    """
    Processes all .tmdl files in the 'tables' subfolder located at base_path.
    
    Parameters:
        base_path (str): The base directory containing the 'tables' subfolder.
    """
    # Construct the full path to the 'tables' folder.
    tables_folder = os.path.join(base_path, "definition", "tables")
    
    # Find all .tmdl files in the tables folder.
    tmdl_files = glob.glob(os.path.join(tables_folder, "*.tmdl"))
    
    # Process each .tmdl file.
    for file_path in tmdl_files:
        print(f"Processing file: {file_path}")
        transform_table_file(file_path)


def copy_semanticmodel_directories(input_path, output_path):
    """
    Copies all directories ending with '.SemanticModel' from the input_path 
    to the output_path while preserving the relative directory structure.
    
    Parameters:
        input_path (str): Source directory.
        output_path (str): Destination directory.
    """
    # Pattern to match any folder that ends with '.SemanticModel' (recursively)
    pattern = os.path.join(input_path, '**', '*.SemanticModel')
    # Retrieve all matching directories
    directories = glob.glob(pattern, recursive=True)
    
    for directory in directories:
        # Ensure it is a directory
        if os.path.isdir(directory):
            # Compute the relative directory path from input_path
            relative_path = os.path.relpath(directory, input_path)
            # Construct the destination path preserving the structure
            dest_dir = os.path.join(output_path, relative_path)
            # Create destination directory if needed and copy the entire folder
            # Note: 'dirs_exist_ok=True' requires Python 3.8 or later
            shutil.copytree(directory, dest_dir, dirs_exist_ok=True)
            print(f"Copied directory: {directory} to {dest_dir}")


def copy_and_rename_reports(output_path, default_report_path):
    """
    For each directory in the output_path that ends with '.SemanticModel',
    capture the base name (i.e., the directory name before '.SemanticModel') and store it.
    Then copy the folder named 'Default.Report' from default_report_path and paste it into
    output_path with the new name '<base_name>.Report'.

    Parameters:
        output_path (str): Directory where the SemanticModel directories are located.
        default_report_path (str): Directory containing the 'Default.Report' folder.

    Returns:
        List[str]: The list of captured base names.
    """
    base_names = []
    # Construct the full path for the default report folder.
    default_report_dir = default_report_path
    
    if not os.path.isdir(default_report_dir):
        print(f"Default report folder not found at: {default_report_dir}")
        return base_names
    
    # Iterate over all items in the output_path.
    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        # Check if the item is a directory and its name ends with '.SemanticModel'.
        if os.path.isdir(item_path) and item.endswith(".SemanticModel"):
            # Capture the base name (the part before '.SemanticModel').
            base_name = item[:-len(".SemanticModel")]
            base_names.append(base_name)
            
            # Define the destination report folder name.
            dest_report_dir = os.path.join(output_path, f"{base_name}.Report")
            
            # If the destination already exists, remove it to allow copying.
            if os.path.exists(dest_report_dir):
                shutil.rmtree(dest_report_dir)
            
            # Copy the entire default report folder to the destination folder.
            shutil.copytree(default_report_dir, dest_report_dir)
            print(f"Copied report folder from '{default_report_dir}' to '{dest_report_dir}'")
    
    return base_names


def update_definition_and_platform_in_reports(output_path):
    """
    For each directory in output_path that ends with '.Report',
    update the following:
    
    1. In 'definition.pbir', update the "datasetReference.byPath.path" property by replacing the placeholder
       with the actual semantic model name. The new path will be in the format:
       "../<semantic_model_name>.SemanticModel"
       
    2. In '.platform', update the "metadata.displayName" property with the semantic model name.
    
    Parameters:
        output_path (str): The folder containing subdirectories ending with '.Report'.
    """
    # Iterate over each item in the output folder.
    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        # Process only directories that end with ".Report"
        if os.path.isdir(item_path) and item.endswith(".Report"):
            # Extract the semantic model name by removing the ".Report" suffix.
            semantic_model_name = item[:-len(".Report")]
            
            # Update definition.pbir
            pbir_file = os.path.join(item_path, "definition.pbir")
            if os.path.isfile(pbir_file):
                try:
                    with open(pbir_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    # Construct the new path using the semantic model name
                    new_path = f"../{semantic_model_name}.SemanticModel"
                    
                    # Update the path in the nested structure if keys exist
                    if ("datasetReference" in data and 
                        "byPath" in data["datasetReference"] and 
                        "path" in data["datasetReference"]["byPath"]):
                        data["datasetReference"]["byPath"]["path"] = new_path
                    else:
                        print(f"Warning: Expected keys not found in {pbir_file}")
                    
                    with open(pbir_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                    
                    print(f"Updated {pbir_file} with semantic model name '{semantic_model_name}'")
                except Exception as e:
                    print(f"Error updating {pbir_file}: {e}")
            else:
                print(f"'definition.pbir' not found in {item_path}")
            
            # Update .platform
            platform_file = os.path.join(item_path, ".platform")
            if os.path.isfile(platform_file):
                try:
                    with open(platform_file, "r", encoding="utf-8") as f:
                        platform_data = json.load(f)
                    
                    # Update the displayName in the metadata if present
                    if "metadata" in platform_data and "displayName" in platform_data["metadata"]:
                        platform_data["metadata"]["displayName"] = semantic_model_name
                    else:
                        print(f"Warning: Expected keys not found in {platform_file}")
                    
                    with open(platform_file, "w", encoding="utf-8") as f:
                        json.dump(platform_data, f, indent=2)
                    
                    print(f"Updated {platform_file} with displayName '{semantic_model_name}'")
                except Exception as e:
                    print(f"Error updating {platform_file}: {e}")
            else:
                print(f"'.platform' not found in {item_path}")


def process_all_semantic_models(output_path):
    """
    Iterates over every directory in output_path that ends with '.SemanticModel'
    and processes it using process_semantic_model().
    
    Parameters:
        output_path (str): The base folder that contains semantic model directories.
    """
    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        # Check if it is a directory and its name ends with '.SemanticModel'
        if os.path.isdir(item_path) and item.endswith(".SemanticModel"):
            print(f"Processing semantic model: {item_path}")
            update_database_tmdl(item_path) 
            delete_definition_datasources(item_path)
            clean_definition_model(item_path)  
            process_all_table_files(item_path)  


if __name__ == "__main__":
    # Ensure the output path exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Process the semantic model directories and reports
    # Copy the semantic model directories from input_path to output_path
    copy_semanticmodel_directories(input_path, output_path)
    
    # Copy and rename the reports
    # Copy the Default.Report folder to each semantic model directory
    # and rename it to match the semantic model name
    copy_and_rename_reports(output_path, default_report_path)
    
    # Update the definition.pbir and .platform files in the reports
    # with the semantic model name
    update_definition_and_platform_in_reports(output_path)
    
    # Process all semantic model directories
    # by updating the database.tmdl, deleting datasources.tmdl,
    # cleaning the model.tmdl, and transforming the table files
    # in each semantic model directory
    process_all_semantic_models(output_path)
