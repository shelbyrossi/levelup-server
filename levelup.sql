 SELECT 
    u.first_name,
    u.last_name,
    g.*,
    gr.user_id

   

FROM levelupapi_game g
JOIN auth_user u
    ON gr.user_id = u.id
INNER JOIN levelupapi_gamer gr
    ON gr.user_id = u.id
          