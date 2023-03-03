use deities

select * from openrowset (bulk 'C:\wikipedia-project\wiki-data\deity-profiles\deities.json', Single_CLOB) as
import;

Declare @JSON varchar(max)
SELECT @JSON=BulkColumn
FROM OPENROWSET (BULK 'C:\wikipedia-project\wiki-data\deity-profiles\deities.json', SINGLE_CLOB) import
SELECT * INTO deity_table FROM OPENJSON (@JSON)
WITH  (
   [type] varchar(20),
   [name] varchar(20),  
   [god] varchar(max),  
   [abode] varchar(max),
   [symbol] varchar(max),
   [parent] varchar(max),
   [sibling] varchar(max),
   [children] varchar(max));

   Select *  from deity_table;

   /* All of Zeus's children */

Select * from deity_table
Where parent like '%Zeus%'

/* all Dieties abiding in the underworld that have the parent Eris*/ 

Select * from deity_table
where abode like '%underworld%' and parent like '%Eris%'