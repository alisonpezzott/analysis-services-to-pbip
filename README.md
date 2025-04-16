[![Convert AS Models to PBIP](https://github.com/alisonpezzott/analysis-services-to-pbip/actions/workflows/process.yml/badge.svg)](https://github.com/alisonpezzott/analysis-services-to-pbip/actions/workflows/process.yml)

## Objective

Map the structure of a semantic model resulting from the deployment of Analysis Services (On-premises) and create a script to modify it, adapting into a Power BI (PBIP) project.


## Contents

```
.
├──── input_as                         -- Analysis Services Semantic Models
│     ├ Sample_1500.SemanticModel
│     └ Sample_1600.SemanticModel
│ 
├──── src                       
│     ├ Default.Report                 -- Blank Report to open in PBI Desktop
│     ├ utils.py                       -- Code parts to compose the main script
│     └ process.py                     -- The main code
│
├──── output_pbip                      -- Projects folder output of conversion
│     ├ Sample_1500.SemanticModel
│     ├ Sample_1500.Report
│     ├ Sample_1600.SemanticModel
│     └ Sample_1600.Report
│
├──── .gitignore                       -- Ensure not version of data
└──── README.md                        -- Guidelines
```


## Instructions  

- Fork the repo;
- Sync your PBI/Fabric Workspace with the Git in the folder `input_as`;  
- The Action `process.yml` will runs after sync;
- Enjoy your files in the `PBIP` folder!  
- If you want, you can sync the `output_pbip` with other PBI/Fabric Workspace 😉
- You can clone to your local PC and make your changes to the transformed new reports.


