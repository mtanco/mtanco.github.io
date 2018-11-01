Outdated tools like SQL Assistant and Teradata Administrator made it easier to know the hierarchical location of a given database. In Teradata Studio, it is harder to find a database if you know it's owner(s). This is an issue for loading data with Smart Loader which requires navigating to the database which will store the new tables.

Using the DBC views, we will get the database location paths of all databases.

## Connect to Teradata


```sql
%connect vantage19085
```

    Password ·····
    

    Success: 'vantage19085' connection established
    

## Using DBC.DatabasesV

The DBC views store important information about various objects in a Vantage system. Using DBC.DatabasesV, we can find the owner of a database. We can then look at the owner of _that_ database continuously. The root would be a database that is it's own owner, for example, DBC.



```sql
select top 10 *
from dbc.DatabasesV
```


## Recursive Queries

With this logic in mind, we can use a recursive query to navigate the ownership path of each database.


```sql
WITH RECURSIVE DATABASE_HIREARCHY (DB_NODE,DB_NAME,DB_OWNER,LVL) AS (

    --INITIAL CASE
    SELECT
        DB.DATABASENAME AS DB_NODE
        ,DB.DATABASENAME AS DB_NAME
        ,DB.OWNERNAME DB_OWNER
        , 1 AS LVL
    FROM DBC.DATABASESV AS DB

    UNION ALL


    SELECT
        DH.DB_NODE 
        ,DH.DB_OWNER AS DB_NAME
        ,DB.OWNERNAME AS DB_OWNER
        ,DH.LVL + 1
    FROM DATABASE_HIREARCHY AS DH --CALLS SELF RECURSIVELY
    INNER JOIN DBC.DATABASESV AS DB
        ON DH.DB_OWNER = DB.DATABASENAME
    WHERE DB.DATABASENAME <> DB.OWNERNAME --BASE CASE, DB IS IT'S OWN OWNER

) 
SELECT * 
FROM DATABASE_HIREARCHY
ORDER BY DB_NODE, LVL;
```






## nPath for Cleaner Output

We could stop here and say this output is good enough for answer our question. But for very deeply nested databases this is not easy to read. We'll next take advantage of nPath's ability to accumulate paths of events. 

### Translate to Latin

By default, the text columns in DBC views are unicode. The nPath function requires latin characters in the accumulate clauses, so we translate these in our select.


```sql
WITH RECURSIVE DATABASE_HIREARCHY (DB_NODE,DB_NAME,DB_OWNER,LVL) AS (

    --INITIAL CASE
    SELECT
        TRANSLATE(DB.DATABASENAME USING UNICODE_TO_LATIN) AS DB_NODE
        ,TRANSLATE(DB.DATABASENAME USING UNICODE_TO_LATIN) AS DB_NAME
        ,TRANSLATE(DB.OWNERNAME USING UNICODE_TO_LATIN) DB_OWNER
        , 1 AS LVL
    FROM DBC.DATABASESV AS DB

    UNION ALL


    SELECT
        DH.DB_NODE 
        ,DH.DB_OWNER AS DB_NAME
        ,TRANSLATE(DB.OWNERNAME USING UNICODE_TO_LATIN) AS DB_OWNER
        ,DH.LVL + 1
    FROM DATABASE_HIREARCHY AS DH --CALLS SELF RECURSIVELY
    INNER JOIN DBC.DATABASESV AS DB
        ON DH.DB_OWNER = DB.DATABASENAME
    WHERE DB.DATABASENAME <> DB.OWNERNAME --BASE CASE, DB IS IT'S OWN OWNER

) 
SELECT * 
FROM DATABASE_HIREARCHY
ORDER BY DB_NODE, LVL;
```






### Recursive View

We cannot use a recursive query as a derived table, so we will create the same output as a recursive view which we can then call from our nPath function.


```sql
REPLACE RECURSIVE VIEW DATABASE_HIREARCHY (DB_NODE,DB_NAME,DB_OWNER,LVL) AS (

    --INITIAL CASE
    SELECT
        TRANSLATE(DB.DATABASENAME USING UNICODE_TO_LATIN) AS DB_NODE
        ,TRANSLATE(DB.DATABASENAME USING UNICODE_TO_LATIN) AS DB_NAME
        ,TRANSLATE(DB.OWNERNAME USING UNICODE_TO_LATIN) DB_OWNER
        , 1 AS LVL
    FROM DBC.DATABASESV AS DB

    UNION ALL


    SELECT
        DH.DB_NODE 
        ,DH.DB_OWNER AS DB_NAME
        ,TRANSLATE(DB.OWNERNAME USING UNICODE_TO_LATIN) AS DB_OWNER
        ,DH.LVL + 1
    FROM DATABASE_HIREARCHY AS DH --CALLS SELF RECURSIVELY
    INNER JOIN DBC.DATABASESV AS DB
        ON DH.DB_OWNER = DB.DATABASENAME
    WHERE DB.DATABASENAME <> DB.OWNERNAME --BASE CASE, DB IS IT'S OWN OWNER

) ;
```





```sql
SELECT * FROM DATABASE_HIREARCHY WHERE DB_NODE = 'MT_TEST2';
```



### Accumulate Paths


```sql
SELECT 
    DB_NAME
    ,CAST(OWNER_PATH AS VARCHAR(1000)) AS OWNER_PATH
    ,PATH_LENGTH + 1 AS PATH_LENGTH
FROM NPATH(
    ON (
        SELECT * 
        FROM DATABASE_HIREARCHY
    )
    PARTITION BY DB_NODE
    ORDER BY LVL DESC
    USING
        MODE(NONOVERLAPPING)
        SYMBOLS(TRUE AS A)
        PATTERN('A*')
        RESULT(
            FIRST(DB_NODE OF A) AS DB_NAME
            ,ACCUMULATE(DB_OWNER OF A) AS OWNER_PATH
            ,COUNT(* OF A) AS PATH_LENGTH
        )
) AS X
ORDER BY PATH_LENGTH DESC;
```



## Wrapping It Up

Now that we've accomplished each piece, we'll wrap this up in a parameterized stored procedure. This will take a a database name as input and return a single row with that name, ownership path, and path length.

_In the current version of this Jupyter Kernal we cannot build or call stored procedures. You can use this code in your second favorite SQL editor for ease of finding databases :)_


```sql
REPLACE PROCEDURE MT_DB_LKUP (IN DB_NAME VARCHAR(4000))
DYNAMIC RESULT SETS 1
BEGIN

    --VARIABLES WE USE IN THIS PROCEDURE
    DECLARE statement1_str VARCHAR(500);
    DECLARE result_set CURSOR WITH RETURN ONLY FOR stmt1;

    --CREATE RECURSIVE VIEW THAT WILL BE USED IN NPATH
    --ONLY ON THE DB WE CARE ABOUT
    REPLACE RECURSIVE VIEW DATABASE_HIREARCHY (CHILD,DATABASENAME,OWNERNAME,ORDR) AS (

        --Start at each DB
        SELECT
            TRANSLATE(DB.DATABASENAME USING UNICODE_TO_LATIN) AS CHILD
            ,TRANSLATE(DB.DATABASENAME USING UNICODE_TO_LATIN) AS DATABASENAME
            ,TRANSLATE(DB.OWNERNAME USING UNICODE_TO_LATIN) AS OWNERNAME
            , 1 AS ORDR
        FROM DBC.DATABASESV AS DB

        UNION ALL

        --Recursive on DB owner
        SELECT
            DH.CHILD AS CHILD
            ,DH.OWNERNAME
            ,TRANSLATE(DB.OWNERNAME USING UNICODE_TO_LATIN) AS OWNERNAME
            ,DH.ORDR + 1
        FROM DATABASE_HIREARCHY AS DH
        INNER JOIN DBC.DATABASESV AS DB
            ON DH.OWNERNAME = DB.DATABASENAME
        WHERE DB.DATABASENAME <> DB.OWNERNAME --Root Case, stop if DB owns itself

    ) ;
                                                 
    --COMMIT THE VIEW SO WE CAN SELCT FROM IT
    COMMIT WORK;

    --Using parameter in the where clause of the on clause
    SET statement1_str = 

        'SELECT 
            DATABASENAME
            ,CAST(HIERARCHY AS VARCHAR(1000)) AS HIERARCHY
            ,PATH_LENGTH + 1 AS PATH_LENGTH
        FROM NPATH(
            ON (

                SELECT * 
                FROM DATABASE_HIREARCHY
                WHERE CHILD = ?
                                                 
            )
            PARTITION BY CHILD
            ORDER BY ORDR DESC
            USING
                MODE(NONOVERLAPPING)
                SYMBOLS(TRUE AS A)
                PATTERN(''A*'')
                RESULT(
                    FIRST(CHILD OF A) AS DATABASENAME
                    ,ACCUMULATE(OWNERNAME OF A) AS HIERARCHY
                    ,COUNT(* OF A) AS PATH_LENGTH
                )
        ) AS X;';


    --SET UP AND RUN OUR NPATH QUERY
    PREPARE stmt1 FROM statement1_str;
    OPEN result_set USING DB_NAME;
    DEALLOCATE PREPARE stmt1;

    --REMOVE VIEW
    --We don't need it any more
    DROP VIEW DATABASE_HIREARCHY;

END;

```


```sql
CALL MT_DB_LKUP('MT_TEST2');
```



## Disconnect from the Database


```sql
%disconnect vantage19085
```

    Success: 'vantage19085' disconnected


