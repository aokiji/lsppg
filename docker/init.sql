DO $$ 
DECLARE
    pais TEXT;
    lista_paises TEXT[] := ARRAY[
        'Argentina', 'Brasil', 'Chile', 'Colombia', 'CostaRica', 'Cuba', 'Ecuador', 'España', 'EstadosUnidos', 
        'Francia', 'Guatemala', 'Honduras', 'Italia', 'Japon', 'Mexico', 'Panama', 'Paraguay', 
        'Peru', 'Uruguay', 'Venezuela'
    ];
BEGIN
    -- Iterar sobre la lista de países
    FOREACH pais IN ARRAY lista_paises
    LOOP
        -- Crear dinámicamente las tablas usando EXECUTE
        EXECUTE format('
            CREATE TABLE IF NOT EXISTS %I (
                id SERIAL,
                ciudad VARCHAR(100) NOT NULL,
                poblacion INT NOT NULL,
                fecha_creacion DATE DEFAULT CURRENT_DATE
            );
        ', pais);
    END LOOP;
END $$;
