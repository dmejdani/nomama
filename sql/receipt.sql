/* 
CREATE TABLE item(
    receiptid INTEGER,
    name TEXT,
    price FLOAT,
    quantity INTEGER,
    catagory TEXT
);

INSERT INTO item VALUES(1, "LANDSCHINKEN", 1.59, 1, "MEAT");
INSERT INTO item VALUES(1, "VOLLKORNTOAST", 0.57, 1, "GRAIN PRODUCT");
INSERT INTO item VALUES(1, "ORANGEN", 2.71, 1, "FRUIT");
INSERT INTO item VALUES(1, "APFELSNACKAPFEL", 2.64, 2, "FRUIT");
INSERT INTO item VALUES(1, "ESLMILCH 1.5%", 0.68, 1, "DAIRY PRODUCT");
INSERT INTO item VALUES(1, "KNUSPER MUESLI", 1.73, 1, "MUESLI");
INSERT INTO item VALUES(1, "RIEGEL SCHOKO ZU", 0.96, 1, "SNACK");
INSERT INTO item VALUES(1, "EIERPLAETZCHEN", 1.15, 1, "SNACK");


INSERT INTO item VALUES(2, "STAPELCHIPS SORT", 1.15, 1, "SNACK");
INSERT INTO item VALUES(2, "FRISCHK. NAT", 0.96, 1, "DAIRY PRODUCT");
INSERT INTO item VALUES(2, "GRA.PUD.M.SAHNE", 0.24, 1, "SNACK");
INSERT INTO item VALUES(2, "SUPPENFLEISH 500G", 2.93, 1, "MEAT"); 



CREATE TABLE receipt(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    shop TEXT,
    location TEXT,
    totprice FLOAT,
    payer TEXT
);

INSERT INTO receipt (date, shop, location, payer) VALUES('2020-10-08', "REWE", "hemmstr", "H");
INSERT INTO receipt (date, shop, location, payer) VALUES('2020-10-09', "NETTO", "admiralstr", "D");





UPDATE receipt
    SET totprice = (SELECT SUM(price*quantity) FROM item WHERE item.receiptid = receipt.id);
 */

SELECT * FROM receipt;
SELECT * FROM item;
/*
SELECT * FROM item, receipt
    WHERE item.receiptid = receipt.id;

*/



