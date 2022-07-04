SELECT * FROM mybank_schema.questions;

UPDATE questions
SET status = 'Pending'
WHERE id = 3;