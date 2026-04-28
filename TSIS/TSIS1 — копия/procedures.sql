-- procedures.sql
-- Функция расширенного поиска (Task 3.4)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT, 
    first_name VARCHAR, 
    last_name VARCHAR, 
    email VARCHAR, 
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.contact_id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.first_name;
END;
$$ LANGUAGE plpgsql;

-- Процедура добавления телефона (Task 3.4)
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR, 
    p_phone VARCHAR, 
    p_type VARCHAR
)
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    -- Поиск контакта по полному имени
    SELECT id INTO v_contact_id 
    FROM contacts 
    WHERE first_name || ' ' || COALESCE(last_name, '') = p_contact_name
       OR first_name = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    -- Добавление телефона
    INSERT INTO phones (contact_id, phone, type) 
    VALUES (v_contact_id, p_phone, p_type);
    
    RAISE NOTICE 'Phone % added to contact %', p_phone, p_contact_name;
END;
$$ LANGUAGE plpgsql;

-- Процедура перемещения в группу (Task 3.4)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR, 
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_contact_id INT;
    v_group_id INT;
BEGIN
    -- Поиск контакта
    SELECT id INTO v_contact_id 
    FROM contacts 
    WHERE first_name || ' ' || COALESCE(last_name, '') = p_contact_name
       OR first_name = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    -- Создание группы если не существует
    INSERT INTO groups (name) VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;
    
    -- Получение ID группы
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    -- Обновление группы контакта
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    
    RAISE NOTICE 'Contact % moved to group %', p_contact_name, p_group_name;
END;
$$ LANGUAGE plpgsql;

-- Функция для пагинации с сортировкой
CREATE OR REPLACE FUNCTION get_paginated_sorted(
    p_limit INT, 
    p_offset INT,
    p_sort_by VARCHAR DEFAULT 'first_name'
)
RETURNS TABLE(
    id INT, 
    first_name VARCHAR, 
    last_name VARCHAR, 
    email VARCHAR, 
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.contact_id = p.contact_id
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY 
        CASE WHEN p_sort_by = 'first_name' THEN c.first_name END,
        CASE WHEN p_sort_by = 'birthday' THEN c.birthday END,
        CASE WHEN p_sort_by = 'created_at' THEN c.created_at END,
        c.first_name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Функция фильтрации по группе
CREATE OR REPLACE FUNCTION filter_by_group(p_group_name VARCHAR)
RETURNS TABLE(
    id INT, 
    first_name VARCHAR, 
    last_name VARCHAR, 
    email VARCHAR, 
    birthday DATE,
    phones TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.contact_id = p.contact_id
    WHERE g.name = p_group_name
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday
    ORDER BY c.first_name;
END;
$$ LANGUAGE plpgsql;