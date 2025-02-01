import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

def q3ans():
    print('Question 3. Trip Segmentation Count:')
    q = '''SELECT 
	        COUNT(CASE WHEN trip_distance <= 1 THEN 1 END) AS "ans_1",
            COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END) AS "ans_2",
	        COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END) AS "ans_3",
	        COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END) AS "ans_4",
	        COUNT(CASE WHEN trip_distance > 10 THEN 1 END) AS "ans_5"
        FROM green_taxi_data
        WHERE lpep_dropoff_datetime >= '2019-10-01 00:00:00'
        AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
        '''
    q_values = pd.read_sql(q, con = engine).astype(str).values[0]
    answer = '; '.join(q_values)
    print(f'Answer: {answer}\n')

def q4ans():
    print('Question 4. Longest Trip:')
    q = '''SELECT DATE(lpep_pickup_datetime), trip_distance
        FROM green_taxi_data
        ORDER BY trip_distance desc
        LIMIT 1;
        '''
    q_values = pd.read_sql(q, con = engine).astype(str).values[0]
    answer = q_values[0]
    print(f'Answer: {answer}\n')

def q5ans():
    print('Question 5. Three biggest pickup zones')
    q = '''
    SELECT SUM(a.total_amount) as total_amount_sum, 
	    b."Zone"
    FROM green_taxi_data a
    INNER JOIN zones b
	    ON b."LocationID" = a."PULocationID"
    WHERE DATE(a.lpep_pickup_datetime) = '2019-10-18'
    GROUP BY b."Zone"
    HAVING SUM(total_amount) > 13000
        '''
    df = pd.read_sql(q, con = engine)
    answer = ', '.join(df['Zone'])
    print(f'Answer: {answer}\n')

def q6ans():
    print('Question 6.Largest tip') 
    q = '''
        SELECT MAX(a.tip_amount) as total_tip_amount, 
	        b."Zone"
        FROM green_taxi_data a
        INNER JOIN zones b
	        ON b."LocationID" = a."DOLocationID"
        WHERE EXTRACT(YEAR FROM a.lpep_pickup_datetime) = '2019'
	        AND EXTRACT(MONTH FROM a.lpep_pickup_datetime) = '10'
            AND a."PULocationID"=74
        GROUP BY b."Zone"
        ORDER BY total_tip_amount DESC
        LIMIT 10
        '''
    q_values = pd.read_sql(q, con = engine).values[:]
    answer = q_values[:]
    print(f'Answer: {answer}\n')

if __name__=='__main__':
    q3ans()
    q4ans()
    q5ans()
    q6ans()