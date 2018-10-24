
A feature of Aster and the new Vantage is that you can write custom, anlaytic functions. In this post we will walk through taking an existing custom Aster function and installing it on the new Teradata Vantage platform. 

We will walk through the process with the ID customer function which gets a unique id for every row.


```sql
%lsconnect
```

    Disconnected: NAME=vantage19085, USER=user8, HOST=sdt19085.labs.teradata.com
    


```sql
%connect vantage19085
```

    Success: 'vantage19085' connection established
    

## Prepare the Function
Often, the custom SLQ-MR function is a jar file saved inside of a zip file with the same name. The Teradata Analytics Platform requires that every function have a json file that explains how the function works. 

### Steps to Prepare
1. Unzip id.zip
2. Write id.json
3. Zip id.jar and id.json together

### Writing id.json
The following fields are required:
* function_name
* function_type: sqlmr, driver, or graph. non-driver can also be used, and is the same a sqlmr
* short_description: include to prevent json null error
* long_description: include to prevent json null error


```json
{
  "function_name": "id",
  "function_type": "sqlmr",
  "short_description": "Creates a unique id for every row",
  "long_description": "Creates a unique id for every row"
}
```

### JSON for Input Tables
Some functions require one or more input tables, or use parameters that refernce a column in an input table. This is where any partitioning is explained. For non-partitioned tables use "PartitionByAny".


```json
...
"input_tables": [
    {
      "requiredInputKind": [
        "PartitionByKey"
      ],
      "isOrdered": false,
      "partitionByOne": false,
      "name": "input",
      "alternateNames": [],
      "isRequired": true,
      "rDescription": "This table defining the input training data.",
      "description": "This table defining the input training data.",
      "datatype": "TABLE_ALIAS",
      "allowsLists": false
    }
  ],
  ...
```

### JSON for Arguements
Some functions take one or more agruements, these can be string literals, numbers, or refernces to an input table.


```json
"argument_clauses": [
    {
      "targetTable": [
        "input"
      ],
      "checkDuplicate": false,
      "allowedTypes": [],
      "allowedTypeGroups": [
        "STRING"
      ],
      "requiredLength": 1,
      "matchLengthOfArgument": "",
      "allowPadding": true,
      "name": "text_column",
      "isRequired": true,
      "rDescription": "Specifies the name of the input table column that contains the text.",
      "description": "Specifies the name of the input table column that contains the text.",
      "datatype": "COLUMNS",
      "allowsLists": false
    },
    {
      "name": "split_by",
      "isRequired": true,
      "rDescription": "Specifies how to split paragraphs.",
      "description": "Specifies how to split paragraphs.",
      "datatype": "STRING",
      "allowsLists": false
    }
  ]
```

## Permissions to Install Custom Functions
Many permissions are necessary to install files and functions. By default these are given to the user Alice. 


```sql
-- grant user foreign_server_ddl privileges
GRANT SELECT ON TD_SERVER_DB.coprocessor_ddl TO user with grant option;

-- grant user privileges needed to run other store procedures
-- used by custom UDF install/uninstall stored procedure
GRANT EXECUTE FUNCTION ON TD_SYSFNLIB.SCRIPT TO user;
GRANT EXECUTE ON SYSUIF.DEFAULT_AUTH TO user;
GRANT EXECUTE PROCEDURE ON SYSUIF.INSTALL_FILE TO user;
GRANT EXECUTE PROCEDURE ON SYSUIF.REPLACE_FILE TO user;
GRANT EXECUTE PROCEDURE ON SYSUIF.REMOVE_FILE TO user;

GRANT EXECUTE PROCEDURE ON SQLJ.INSTALL_JAR TO user;
GRANT EXECUTE PROCEDURE ON SQLJ.REPLACE_JAR TO user;
GRANT EXECUTE PROCEDURE ON SQLJ.REMOVE_JAR TO user;
GRANT EXECUTE PROCEDURE ON SQLJ.ALTER_JAVA_PATH TO user;
GRANT EXECUTE PROCEDURE ON SYSLIB.EXECUTEFOREIGNSQL TO user;
 
-- (option 1) grant user privileges to install/remove/download in user (private) schema
GRANT EXECUTE PROCEDURE on pm.install_afunction to user;
GRANT EXECUTE PROCEDURE on pm.remove_afunction to user;
GRANT EXECUTE PROCEDURE on pm.install_afile to user;
GRANT EXECUTE PROCEDURE on pm.remove_afile to user;
GRANT EXECUTE PROCEDURE on pm.download_afile to user;

-- (option 2) grant user privileges to install/remove/download in public schema (access to UDFs/Files is available to all users without additional grant privileges)
GRANT EXECUTE PROCEDURE on pm.install_afunction_to_public to user;
GRANT EXECUTE PROCEDURE on pm.remove_afunction_from_public to user;
GRANT EXECUTE PROCEDURE on pm.install_afile_to_public to user;
GRANT EXECUTE PROCEDURE on pm.remove_afile_from_public to user;
GRANT EXECUTE PROCEDURE on pm.download_afile_from_public to user;
```

## Remove id from Coprocessor and Teradata
This is if the function has been previously installed. The order is important, you cannot uninstall the function from the Aster engine if there is no longer a Teradata reference to it.


```sql
CALL PM.REMOVE_AFUNCTION_FROM_PUBLIC('id');
```


```sql
--Use 0 to check if the file is being used before removing it
--Use 1 to remove the file without checking if it's being used
CALL SYSUIF.REMOVE_FILE('id',0);
```

## Install id
We first create a reference to the file in Teradata, and then install it on the coprocessor.


```sql
--cz: file is on my local machine and it is a zip file
--This is jupyter labs so it don't know about my local machine :(
--I'm going to go run this is studio
CALL SYSUIF.INSTALL_FILE(
    'id' 
    ,'id.zip'
    ,'cz!C:\Users\mt186048\...\id.zip'
);
```


```sql
CALL PM.INSTALL_AFUNCTION_TO_PUBLIC('id');
```


```sql
--confirm funciton exists 
HELP FOREIGN SCHEMA "public"@coprocessor
```





