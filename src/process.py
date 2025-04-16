from utils import *


# Constants for input and output paths
# These paths should be set according to your directory structure
input_path = "input_as"
output_path = "output_pbip"
default_report_path = "src/Default.Report"

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
