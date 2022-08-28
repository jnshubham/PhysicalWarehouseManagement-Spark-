CREATE TABLE `deposits` (
  `DepositNumber` int NOT NULL AUTO_INCREMENT,
  `Grain` varchar(50) DEFAULT NULL,
  `BagsQuantity` int DEFAULT NULL,
  `PricePerBag` decimal(18,5) DEFAULT NULL,
  `PartyName` varchar(500) DEFAULT NULL,
  `DepositDate` datetime DEFAULT NULL,
  `Stack` varchar(100) DEFAULT NULL,
  `MarketPrice` int DEFAULT NULL,
  `RecieptProcessed` tinyint(1) DEFAULT NULL,
  `CreatedBy` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`DepositNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE warehouse.reciepts (
  `RecieptNumber` int NOT NULL AUTO_INCREMENT,
  `DepositNumber` varchar(100) DEFAULT NULL,
  `PartyNameReciept` varchar(100) DEFAULT NULL,
  `RecieptDate` datetime DEFAULT NULL,
  `generatedBy` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`RecieptNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

select * from warehouse.deposits;
select * from warehouse.reciepts;
select r.RecieptNumber, 
r.DepositNumber,
r.PartyNameReciept, 
r.RecieptDate, 
max(d.Grain), sum(d.BagsQuantity), max(d.PricePerBag), group_concat(d.Stack), max(d.MarketPrice) from (select * from warehouse.reciepts where recieptNumber=2) r left join (select * from warehouse.deposits where find_in_set(depositNumber, (select depositNumber from warehouse.reciepts where recieptNumber=2))!=0) d on 1=1 group by 1,2,3,4;


select find_in_set(depositNumber, '5,6') from warehouse.deposits;


CREATE TABLE warehouse.stacks (
  `StackID` int NOT NULL AUTO_INCREMENT,
  `StackName` varchar(50) DEFAULT NULL,
  `Capacity` int DEFAULT NULL,
  `UsedCapacity` decimal(18,5) DEFAULT NULL,
  `UnusedCapacity` decimal(18,5) DEFAULT NULL,
  PRIMARY KEY (`StackID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


insert into warehouse.stacks(StackName, Capacity, UsedCapacity, UnusedCapacity) values
('A1', 1500, 750, 750),
('A2', 1500, 100, 1400),
('A3', 1500, 200, 1300),
('A4', 1500, 300, 1200),
('A5', 1500, 400, 1100),
('A6', 1500, 500, 1000),
('A7', 1500, 600, 900),
('A8', 1500, 700, 800),
('A9', 1500, 800, 700),
('A10', 1500, 900, 600),
('B1', 1500, 1000, 500),
('B2', 1500, 1500, 0),
('B3', 1500, 100, 1400),
('B4', 1500, 100, 1400),
('B5', 1500, 100, 1400)
