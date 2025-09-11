-- SQL for creating and seeding the disruptions table
CREATE TABLE IF NOT EXISTS disruptions (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    affected_flights JSONB NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO disruptions (type, severity, title, description, affected_flights, timestamp) VALUES
('foreseen', 'medium', 'Weather Delay', 'Thunderstorms expected at destination airport.', '["6E123", "6E456"]', NOW() - INTERVAL '2 hours'),
('unforeseen', 'high', 'Technical Issue', 'Aircraft maintenance required unexpectedly.', '["6E789"]', NOW() - INTERVAL '1 hour'),
('foreseen', 'low', 'ATC Restriction', 'Air traffic control slot restriction.', '["6E321"]', NOW() - INTERVAL '30 minutes');
