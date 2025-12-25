# List of example questions and their matching SQL queries to guide the model
few_shots = [
    {'Question': "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer': "There are 91 Nike t-shirts in XS size and white color."},
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': "The total price for all S-size t-shirts is 22,292."},
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?",
     'SQLQuery': "SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi' group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id",
     'SQLResult': "Result of the SQL query",
     'Answer': "The total revenue for Levi's t-shirts after discounts is 16,725.4."},
    {'Question': "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
     'SQLResult': "Result of the SQL query",
     'Answer': "The total revenue for Levi's t-shirts without discounts is 17,462."},
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer': "You have 50 white Levi's shirts."}
]