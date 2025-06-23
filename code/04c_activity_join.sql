CREATE VIEW activity_track_data AS
SELECT
    row_number() OVER () AS fid,
    at.*,
    ad.*
FROM
    activity_track at
JOIN
    activity_data ad
    ON at.activity_id = ad."Activity ID";


