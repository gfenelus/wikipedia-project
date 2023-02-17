use deities

select * from openrowset (bulk 'C:\wikipedia-project\wiki-data\deity-profiles\greek-gods.json', Single_CLOB) as
imporrt;

Declare @JSON varchar(max)
SELECT @JSON=BulkColumn
FROM OPENROWSET (BULK 'C:\wikipedia-project\wiki-data\deity-profiles\greek-gods.json', SINGLE_CLOB) import
SELECT * FROM OPENJSON (@JSON)
WITH  (
   [name] varchar(20),  
   [god] varchar(max),  
   [abode] varchar(max),
   [symbol] varchar(max),
   [parent] varchar(max),
   [sibling] varchar(max),
   [children] varchar(max));