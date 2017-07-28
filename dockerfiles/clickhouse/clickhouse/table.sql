CREATE TABLE domains(
    QueryDate Date,
    QueryDateTime DateTime,
    DomainName String,
)
ENGINE = MergeTree(QueryDate, cityHash64(DomainName), (DomainName), 8192);



SELECT t, groupArray((domain_name, c)) as groupArr
FROM (
    SELECT (intDiv(toUInt32(timestamp), 10) * 10) * 1000 as t, domain_name, count(*) as c
    FROM TestDB.domains WHERE query_date >= toDate(1501266533) AND timestamp >= toDateTime(1501266533) GROUP BY t, domain_name ORDER BY c LIMIT 5
) GROUP BY t ORDER BY t


SELECT t, groupArray((domain_name, c)) as groupArr
FROM (
    SELECT (intDiv(toUInt32(toStartOfMinute(timestamp)), 10) * 10) * 1000 as t, domain_name, count(*) as c
    FROM TestDB.domains
    WHERE $timeFilter GROUP BY t, domain_name ORDER BY t
)
GROUP BY t limit 5 by t



