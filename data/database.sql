CREATE TABLE query ( `query_id` INT UNSIGNED NOT NULL, `ip_id` INT UNSIGNED NOT NULL, `domain_id` INT UNSIGNED NOT NULL, `source_id` INT UNSIGNED NOT NULL, `threat_id` INT UNSIGNED NOT NULL, `creation_time` VARCHAR(10) NOT NULL, PRIMARY KEY (`query_id`), INDEX (`ip_id`,`source_id`,`threat_id`) ) ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE source ( source_id INT UNSIGNED NOT NULL, source_name VARCHAR(20) NOT NULL, PRIMARY KEY (`source_id`) ) ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE threat ( threat_id INT UNSIGNED NOT NULL, threat_type VARCHAR(20) NOT NULL, threat_desc VARCHAR(80) NOT NULL, PRIMARY KEY (`threat_id`) ) ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE domain ( domain_id INT UNSIGNED NOT NULL, domain_name VARCHAR(50) NOT NULL, PRIMARY KEY (`domain_id`) ) ENGINE = InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
CREATE TABLE ip (ip_id INT UNSIGNED NOT NULL, begin_ip VARCHAR(20), end_ip VARCHAR(20), begin_ip_int BIGINT, end_ip_int BIGINT, offset INT, PRIMARY KEY (ip_id)) ENGINE = InnoDB;
CREATE TABLE query (queryid INT UNSIGNED NOT NULL, sourceid INT UNSIGNED NOT NULL, threatid INT UNSIGNED NOT NULL, ipid INT UNSIGNED NOT NULL, domainid INT UNSIGNED NOT NULL, creationtime VARCHAR(15), PRIMARY KEY(queryid), INDEX(sourceid, threatid, ipid, domainid), FOREIGN KEY (sourceid) REFERENCES source(source_id),FOREIGN KEY (ipid) REFERENCES ip(ip_id), FOREIGN KEY (threatid) REFERENCES threat(threat_id),FOREIGN KEY (domainid) REFERENCES domain(domain_id)) ENGINE=INNODB;