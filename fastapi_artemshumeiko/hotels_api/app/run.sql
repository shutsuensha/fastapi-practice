SELECT * 
FROM hotels
WHERE id IN (
SELECT 
    r1.hotel_id
FROM 
    (SELECT hotel_id, COUNT(*) AS room_count
     FROM rooms
     GROUP BY hotel_id) AS r1
LEFT JOIN 
    (SELECT hotel_id, COUNT(*) AS booked_rooms
     FROM rooms
     WHERE id IN (
         SELECT room_id
         FROM bookings
         WHERE date_from BETWEEN '2024-11-05' AND '2024-11-18'
            OR date_to BETWEEN '2024-11-05' AND '2024-11-18'
         GROUP BY room_id
     )
     GROUP BY hotel_id) AS r2
ON r1.hotel_id = r2.hotel_id
WHERE (r1.room_count - COALESCE(r2.booked_rooms, 0)) != 0);