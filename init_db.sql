CREATE TABLE IF NOT EXISTS hotel_daily_activity (
    id SERIAL PRIMARY KEY,
    hotel_id TEXT NOT NULL,
    hotel_name TEXT,
    date_jour DATE NOT NULL,
    date_extraction DATE NOT NULL,
    segment_code TEXT NOT NULL,
    segment_label TEXT,
    pms_type TEXT,
    ca_ttc DOUBLE PRECISION,
    rooms_occupied INTEGER,
    pax INTEGER,
    enf INTEGER,
    arrivals INTEGER,
    ville TEXT,
    pays TEXT,
    devise TEXT,
    type_contrat TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    UNIQUE (hotel_id, date_jour, segment_code, date_extraction)
);

