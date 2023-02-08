CREATE OR REPLACE FUNCTION gen_short_code()
    RETURNS VARCHAR AS
$$
DECLARE
    my_chars      char array[65] := '{"0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"}';
    my_res        text;
    my_random_str text;
    dt_now        timestamp;
    hour_code     integer;
    day_code      integer;
    month_code    integer;
    year_code     integer;

BEGIN
    dt_now = now();
    hour_code := 98 + extract(hour from dt_now);
    day_code := 99 + extract(day from dt_now);
    month_code := 100 + extract(month from dt_now);
    year_code := 101 + extract(year from dt_now) - 2019;
    my_random_str :=
                        cast(my_chars[1 + random() * (array_length(my_chars, 1) - 1)] as char) ||
                        cast(my_chars[1 + random() * (array_length(my_chars, 1) - 1)] as char) ||
                        cast(my_chars[1 + random() * (array_length(my_chars, 1) - 1)] as char) ||
                        cast(my_chars[1 + random() * (array_length(my_chars, 1) - 1)] as char);



    my_res := chr(101 + cast(extract(year from dt_now) as integer) - 2019) ||
              chr(100 + cast(extract(month from dt_now) as integer)) ||
              my_chars[cast(extract(day from dt_now) as integer)] ||
              my_chars[cast(extract(hour from dt_now) as integer)] ||
              my_random_str;

    RETURN my_res;
END;
$$ LANGUAGE plpgsql;