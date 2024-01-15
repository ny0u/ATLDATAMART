-- Création de la table de dimension Location
CREATE TABLE Location (
    LocationID INT PRIMARY KEY,
    Borough VARCHAR(255),
    Zone VARCHAR(255)
);

-- Création de la table de dimension Vendor
CREATE TABLE Vendor (
    VendorID INT PRIMARY KEY,
    VendorName VARCHAR(255)
);

-- Création de la table de dimension Ratecode
CREATE TABLE Ratecode (
    RatecodeID INT PRIMARY KEY,
    RatecodeDescription VARCHAR(255)
);

-- Création de la table de dimension Time
CREATE TABLE Time (
    TimeID INT PRIMARY KEY,
    PickupHour INT,
    PickupDay INT,
    PickupMonth INT,
    PickupYear INT
);

-- Création de la table de dimension PaymentType
CREATE TABLE PaymentType (
    PaymentTypeID INT PRIMARY KEY,
    PaymentTypeName VARCHAR(255)
);

-- Création de la table de faits Trip
CREATE TABLE Trip (
    TripID INT PRIMARY KEY,
    VendorID INT,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance FLOAT,
    RatecodeID INT,
    store_and_fwd_flag VARCHAR(1),
    PULocationID INT,
    DOLocationID INT,
    payment_type INT,
    fare_amount FLOAT,
    extra FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    improvement_surcharge FLOAT,
    total_amount FLOAT,
    congestion_surcharge FLOAT,
    airport_fee FLOAT
);

-- Création des tables de sous-dimensions

CREATE TABLE LocationDetails (
    LocationID INT PRIMARY KEY,
    LocationType VARCHAR(255),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

CREATE TABLE VendorDetails (
    VendorID INT PRIMARY KEY,
    VendorType VARCHAR(255),
    FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID)
);

CREATE TABLE RatecodeDetails (
    RatecodeID INT PRIMARY KEY,
    RatecodeType VARCHAR(255),
    FOREIGN KEY (RatecodeID) REFERENCES Ratecode(RatecodeID)
);

CREATE TABLE TimeDetails (
    TimeID INT PRIMARY KEY,
    HolidayType VARCHAR(255),
    FOREIGN KEY (TimeID) REFERENCES Time(TimeID)
);

CREATE TABLE PaymentTypeDetails (
    PaymentTypeID INT PRIMARY KEY,
    CardNetwork VARCHAR(255),
    FOREIGN KEY (PaymentTypeID) REFERENCES PaymentType(PaymentTypeID)
);





