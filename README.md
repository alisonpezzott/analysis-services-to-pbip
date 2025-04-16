[![Convert AS Models to PBIP](https://github.com/alisonpezzott/analysis-services-to-pbip/actions/workflows/process.yml/badge.svg)](https://github.com/alisonpezzott/analysis-services-to-pbip/actions/workflows/process.yml)

## Objective

Map the structure of a semantic model resulting from the deployment of Analysis Services (On-premises) and create a script to modify it, adapting into a Power BI (PBIP) project.


## Contents

```
.
├──── workspace                    -- Analysis Services Semantic Models
│     ├ Sample_1500.SemanticModel
│     └ Sample_1600.SemanticModel
│ 
├──── src.md                       
│     ├ Default.Report              -- Blank Report to open in PBI Desktop
│     ├ utils.py                    -- Code parts to compose the main script
│     └ process.py                  -- The main code
│
├──── PBIP                          -- Projects folder output of conversion
│     ├ Sample_1500.SemanticModel
│     ├ Sample_1500.Report
│     ├ Sample_1600.SemanticModel
│     └ Sample_1600.Report
│
├──── .gitignore                    -- Ensure not version of data
└──── README.md                     -- Guidelines
```


## Instructions  

- Fork the repo;
- Sync Power BI Workspace with the Git in the folder `workspace`;  
- The Action `process.yml` runs;
- Enjoy your files in the `PBIP` folder!  


## Diff by file  

Below we see the differences between the semantic models and the logic to handle each file to achieve the objective.  


### .platform

#### Analysis Services  
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "SemanticModel",
    "displayName": "analysis_services"
  },
  "config": {
    "version": "2.0",
    "logicalId": "3de0bed6-9bc4-988d-4a22-c0102de10fe6"
  }
}
```

#### Power BI Project  
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "SemanticModel",
    "displayName": "pbip"
  },
  "config": {
    "version": "2.0",
    "logicalId": "d34c8837-9caf-4f05-92d9-4aabcbadf3ee"
  }
}
```  

#### Actions   
Nothing to do.  

---




### definition.pbism


#### Analysis Services  
```json
{
  "version": "4.0",
  "settings": {}
}
```

#### Power BI Project  
```json
{
  "version": "4.0",
  "settings": {}
}
```

#### Actions   
Nothing to do.  

---


### definition/database.tmdl  

#### Analysis Services  

```yml
database
	compatibilityLevel: 1500
```

#### Power BI Project

```yml
database
	compatibilityLevel: 1550
```  

#### Actions    
In the `definition/database.tmdl` set compatibilityLevel to 1550

---  


### definition/dataSources.tmdl  

#### Analysis Services  
```yml
dataSource 'BOOK-PROIJR07F2 AdventureWorksDW-PRD' = provider
	connectionString: Data Source=BOOK-PROIJR07F2;Initial Catalog=AdventureWorksDW-PRD;User ID=fabric
	impersonationMode: impersonateServiceAccount
	provider: System.Data.SqlClient

```

#### Power BI Project  
Not exists  

#### Actions  
Delete the file `definition/dataSources.tmdl`  

---

### definition/model.tmdl  

#### Analysis Services  
```yml
model Model
	culture: en-US
	defaultPowerBIDataSourceVersion: powerBI_V3
	discourageImplicitMeasures

annotation TabularEditor_SerializeOptions = {"IgnoreInferredObjects":true,"IgnoreInferredProperties":true,"IgnoreTimestamps":true,"SplitMultilineStrings":true,"PrefixFilenames":false,"LocalTranslations":false,"LocalPerspectives":false,"LocalRelationships":false,"Levels":["Data Sources","Perspectives","Relationships","Roles","Shared Expressions","Tables","Tables/Calculation Items","Tables/Columns","Tables/Hierarchies","Tables/Measures","Tables/Partitions","Translations"]}

annotation __TEdtr = 1

ref table DimCustomer
ref table DimDate
ref table DimProduct
ref table FactSales
ref table TemporalIntelligence

ref role User
ref role Admin


```

#### Power BI Project  
```yml
model Model
	culture: en-US
	defaultPowerBIDataSourceVersion: powerBI_V3
	discourageImplicitMeasures
	sourceQueryCulture: pt-BR
	dataAccessOptions
		legacyRedirects
		returnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 0

annotation PBIDesktopVersion = 2.141.1558.0 (25.03)+75b5f06a991f8f8a8a4d6b6fcd0f66e1ec2d6fdc

annotation PBI_QueryOrder = ["DimCustomer","DimDate","DimProduct","FactSales"]

annotation PBI_ProTooling = ["DevMode","CalcGroup"]

ref table DimCustomer
ref table DimDate
ref table DimProduct
ref table FactSales
ref table TemporalIntelligence

ref role Admin
ref role User

ref cultureInfo en-US







```

#### Actions  
Keep just the rows that starts with following keywords:
  - model
  - culture
  - defaultPowerBIDataSourceVersion
  - discourageImplicitMeasures
  - ref


--- 

### definition/relationships.tmdl

#### Analysis Services  
```yml
relationship 21c08ca7-46aa-4b83-8722-cbb6691a4da2
	fromColumn: FactSales.CustomerKey
	toColumn: DimCustomer.CustomerKey

relationship 430c151e-5782-4a65-b9af-037c6edd9df5
	fromColumn: FactSales.ProductKey
	toColumn: DimProduct.ProductKey

relationship 2bcd9698-e44d-447e-8d70-a299e88efe24
	fromColumn: FactSales.OrderDateKey
	toColumn: DimDate.Date


```

#### Power BI Project  
```yml
relationship AutoDetected_ff4c7c9a-49b3-414c-84a0-350b1d9097fe
	fromColumn: FactSales.ProductKey
	toColumn: DimProduct.ProductKey

relationship 5d469f69-5fce-3cfe-0c6c-4960cedb932a
	fromColumn: FactSales.CustomerKey
	toColumn: DimCustomer.CustomerKey

relationship ff705d28-ca0c-d767-885b-eb125fbacb79
	fromColumn: FactSales.OrderDateKey
	toColumn: DimDate.Date

```

#### Actions
Nothing to do.

---  


### diagramLayout.json

#### Analysis Services  
Not Exists

#### Power BI Project  
```tmdl
{
  "version": "1.1.0",
  "diagrams": [
    {
      "ordinal": 0,
      "scrollPosition": {
        "x": 0,
        "y": 3
      },
      "nodes": [
        {
          "location": {
            "x": 661,
            "y": 8
          },
          "nodeIndex": "DimCustomer",
          "nodeLineageTag": "2aaacdc9-87e5-4b42-b280-f70427c52fc9",
          "size": {
            "height": 300,
            "width": 234
          },
          "zIndex": 0
        },
        {
          "location": {
            "x": 389.20000076293945,
            "y": 0
          },
          "nodeIndex": "DimDate",
          "nodeLineageTag": "ad311096-377a-4d06-bcc3-6a0e02242c6a",
          "size": {
            "height": 300,
            "width": 234
          },
          "zIndex": 0
        },
        {
          "location": {
            "x": 5,
            "y": 0
          },
          "nodeIndex": "DimProduct",
          "nodeLineageTag": "c7cfcdd9-6ba1-4b6a-b8ae-ad9212c16096",
          "size": {
            "height": 104,
            "width": 234
          },
          "zIndex": 0,
          "expandedHeight": 300
        },
        {
          "location": {
            "x": 96,
            "y": 176
          },
          "nodeIndex": "vFactSales",
          "nodeLineageTag": "5ce89cf1-74d6-427b-8932-ccef1ad9f410",
          "size": {
            "height": 300,
            "width": 234
          },
          "zIndex": 0
        }
      ],
      "name": "All tables",
      "zoomValue": 100,
      "pinKeyFieldsToTop": false,
      "showExtraHeaderInfo": false,
      "hideKeyFieldsWhenCollapsed": false,
      "tablesLocked": false
    }
  ],
  "selectedDiagram": "All tables",
  "defaultDiagram": "All tables"
}
```  

#### Actions
Nothing to do. The Power BI Desktop creates a new in the first run.  

---  

### definition/cultures/en-US.tmdl

#### Analysis Services  
Not Exists

#### Power BI Project  
```yml
cultureInfo en-US

	linguisticMetadata =
			{
			  "Version": "1.0.0",
			  "Language": "en-US"
			}
		contentType: json

```

#### Actions  
Nothing to do.  The Power BI Desktop creates a new in the first run.  

---  

### definition/tables/DimDate.tmdl (Table Sample)

#### Analysis Services  
```yml
table DimDate

	column CalendarYear
		dataType: int64
		sourceProviderType: smallint
		sourceColumn: CalendarYear

	column Date
		dataType: int64
		sourceProviderType: int
		sourceColumn: DateKey

	column Day
		dataType: int64
		sourceProviderType: tinyint
		sourceColumn: DayNumberOfMonth

	column MonthName
		dataType: string
		sourceProviderType: nvarchar
		sourceColumn: EnglishMonthName
		sortByColumn: MonthNumber

	column MonthNumber
		dataType: int64
		sourceProviderType: tinyint
		sourceColumn: MonthNumberOfYear

	partition DimDate = query
		source
			query =
				SELECT
					*
				FROM
					[dbo].[DimDate]
			dataSource: 'BOOK-PROIJR07F2 AdventureWorksDW-PRD'

		annotation TabularEditor_TableSchema = {"Name":"DimDate","Schema":"dbo","Database":"AdventureWorksDW-PRD","IncludedColumns":["DateKey","FullDateAlternateKey","DayNumberOfWeek","EnglishDayNameOfWeek","SpanishDayNameOfWeek","FrenchDayNameOfWeek","DayNumberOfMonth","DayNumberOfYear","WeekNumberOfYear","EnglishMonthName","SpanishMonthName","FrenchMonthName","MonthNumberOfYear","CalendarQuarter","CalendarYear","CalendarSemester","FiscalQuarter","FiscalYear","FiscalSemester"],"SelectAll":true}




```

#### Power BI Project  
```yml
table DimDate
	lineageTag: ad311096-377a-4d06-bcc3-6a0e02242c6a

	column CalendarYear
		dataType: int64
		formatString: 0
		lineageTag: 8be3abce-d885-4853-b422-98c34d6b024d
		summarizeBy: none
		sourceColumn: CalendarYear

		annotation SummarizationSetBy = Automatic

	column Date
		dataType: int64
		formatString: 0
		lineageTag: eace8971-bd89-4e56-b559-5b4a21dc5edc
		summarizeBy: none
		sourceColumn: Date

		annotation SummarizationSetBy = Automatic

	column Day
		dataType: int64
		formatString: 0
		lineageTag: 260e6c34-39c2-426c-920b-2bf9c80f8c4c
		summarizeBy: none
		sourceColumn: Day

		annotation SummarizationSetBy = Automatic

	column MonthName
		dataType: string
		lineageTag: 96ce8628-0331-4f66-929d-340a885a073e
		summarizeBy: none
		sourceColumn: MonthName
		sortByColumn: MonthNumber

		changedProperty = SortByColumn

		annotation SummarizationSetBy = Automatic

	column MonthNumber
		dataType: int64
		formatString: 0
		lineageTag: f7ad5b09-83d1-4b26-a6ed-2d365557791a
		summarizeBy: none
		sourceColumn: MonthNumber

		annotation SummarizationSetBy = Automatic

	partition DimDate = m
		mode: import
		source =
				let
				    Source = Sql.Database("BOOK-PROIJR07F2", "AdventureWorksDW-PRD", [Query="SELECT CalendarYear, DateKey AS Date, DayNumberOfMonth AS Day, EnglishMonthName AS MonthName, MonthNumberOfYear AS MonthNumber FROM [dbo].[DimDate]", CreateNavigationProperties=false])
				in
				    Source

	annotation PBI_NavigationStepName = Navigation

	annotation PBI_ResultType = Table




```

#### Actions  
- Delete rows that starts with `sourceProviderType`  

- For each `column` capture the corresponding `sourceColumn` and create a string variable called `columns` to use in the query SQL for example: "[sourceColumn1] AS [column1], [sourceColumn2] AS [column2], [sourceColumnN] AS [columnN]"

- Capture in the key `dataSource` the text before first space and put in the variable called `server`.  

- Capture no %_TableSchema the following key and bring the value:
  - `Name` as variable `table`  
  - `Schema` as variable `schema`  
  - `Database` as variable `database`  

- Delete from the text `partition` until the end.

- Create the following string in the end:

```
partition <table_name> = m
	mode: import
	source =
		let
			Source = Sql.Database("<server>, <database>, [Query = "SELECT <columns> FROM [<schema>].[<table>]", CreateNavigationProperties=false])
		in
			Source

```

---  


### definition/tables/TemporalIntelligence.tmdl  

#### Analysis Services

```yml
table TemporalIntelligence

	calculationGroup

		calculationItem Default = SELECTEDMEASURE()

		calculationItem PY =
				CALCULATE (
				    SELECTEDMEASURE (),
				    SAMEPERIODLASTYEAR ( DimDate[Date] )
				)

	column Name
		dataType: string
		sourceColumn: Name
		sortByColumn: Ordinal

	column Ordinal
		dataType: int64
		isHidden
		sourceColumn: Ordinal


```  

#### Power BI Project  

```yml
table TemporalIntelligence
	lineageTag: 87f6f91c-5d5c-46c4-a0f1-24df3cd2532a

	calculationGroup

		calculationItem Default = SELECTEDMEASURE()

		calculationItem PY =
				
				CALCULATE (
				    SELECTEDMEASURE (),
				    SAMEPERIODLASTYEAR ( DimDate[Date] )
				)

	column Name
		dataType: string
		lineageTag: ffdc050c-68c2-421d-afac-1cfa56d4bc4e
		summarizeBy: none
		sourceColumn: Name
		sortByColumn: Ordinal

		annotation SummarizationSetBy = Automatic

	column Ordinal
		dataType: int64
		formatString: 0
		lineageTag: 99358b02-a03b-4ebc-9d10-44129ef6bb54
		summarizeBy: sum
		sourceColumn: Ordinal

		annotation SummarizationSetBy = Automatic


```

### Actions  
Nothing to do.  

---  

### definition/roles/User.tmdl

#### Analysis Services  
```tmdl
role User
	modelPermission: read

	tablePermission DimCustomer = [FirstName] = USERPRINCIPALNAME()


```

#### Power BI Project  
```tmdl
role User
	modelPermission: read

	tablePermission DimCustomer = [FirstName] == USERPRINCIPALNAME()

	annotation PBI_Id = 0eef766a0c624dbb9fb89921d5d3c0a8

```

### Actions  
Nothing to do.   

---  