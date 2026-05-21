BEGIN;

-- ============================================================
-- EXTENSIONES
-- ============================================================

CREATE EXTENSION IF NOT EXISTS postgis;


-- ============================================================
-- OPCIONAL: LIMPIEZA DE DATOS
-- Usar solo en desarrollo local.
-- ============================================================

-- TRUNCATE TABLE
--     project_technologies,
--     project_locations,
--     dashboards,
--     notebooks,
--     contact_messages,
--     projects,
--     technologies
-- RESTART IDENTITY CASCADE;


-- ============================================================
-- TECHNOLOGIES
-- ============================================================

INSERT INTO technologies (name, category, icon_url)
VALUES
    ('Python', 'backend', NULL),
    ('FastAPI', 'backend', NULL),
    ('Django', 'backend', NULL),
    ('JavaScript', 'frontend', NULL),
    ('TypeScript', 'frontend', NULL),
    ('React', 'frontend', NULL),
    ('HTML', 'frontend', NULL),
    ('CSS', 'frontend', NULL),
    ('SQL', 'database', NULL),
    ('PostgreSQL', 'database', NULL),
    ('PostGIS', 'database', NULL),
    ('Elasticsearch', 'database', NULL),
    ('QGIS', 'gis', NULL),
    ('GeoServer', 'gis', NULL),
    ('GeoNetwork', 'gis', NULL),
    ('WMS', 'gis', NULL),
    ('WMTS', 'gis', NULL),
    ('TMS', 'gis', NULL),
    ('Leaflet', 'gis', NULL),
    ('MapLibre', 'gis', NULL),
    ('Power BI', 'data', NULL),
    ('Pandas', 'data', NULL),
    ('GeoPandas', 'data', NULL),
    ('Jupyter Notebook', 'data', NULL),
    ('Docker', 'devops', NULL),
    ('Git', 'devops', NULL),
    ('Alembic', 'backend', NULL),
    ('SQLAlchemy', 'backend', NULL)
ON CONFLICT (name) DO NOTHING;


-- ============================================================
-- PROFILE & EXPERIENCES (requiere migración 003)
-- ============================================================

INSERT INTO profiles (
    name,
    slug,
    title,
    subtitle,
    summary,
    location,
    linkedin_url,
    github_url,
    about_title,
    about_content,
    focus_areas,
    key_skills,
    is_active,
    sort_order
)
VALUES (
    'Patricio Pagano',
    'patricio-pagano',
    'Desarrollador Full Stack GIS | Licenciado en Ciencias Geológicas | Especialista en Ciencia de Datos',
    'GIS, Datos Espaciales, Backend, GeoServer, PostgreSQL/PostGIS, React y MapLibre',
    'Geólogo y Desarrollador Full Stack GIS con experiencia en desarrollo de aplicaciones web geoespaciales, APIs REST, bases de datos espaciales y publicación de servicios GIS.',
    'Argentina',
    'https://www.linkedin.com/in/patricio-pagano/',
    'https://github.com/ppagano91',
    'Perfil profesional',
    'Perfil orientado a GIS, datos, software, geociencias, minería, Oil & Gas y geomática, combinando desarrollo backend/frontend con análisis geoespacial.',
    '["GIS", "Geomática", "Ciencia de Datos", "PostgreSQL/PostGIS", "GeoServer", "APIs REST", "Minería", "Oil & Gas"]'::json,
    '["Python", "FastAPI", "SQL", "PostgreSQL/PostGIS", "GeoServer", "QGIS", "React", "Leaflet", "MapLibre", "Docker", "Git"]'::json,
    TRUE,
    0
)
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    title = EXCLUDED.title,
    subtitle = EXCLUDED.subtitle,
    summary = EXCLUDED.summary,
    location = EXCLUDED.location,
    linkedin_url = EXCLUDED.linkedin_url,
    github_url = EXCLUDED.github_url,
    about_title = EXCLUDED.about_title,
    about_content = EXCLUDED.about_content,
    focus_areas = EXCLUDED.focus_areas,
    key_skills = EXCLUDED.key_skills,
    is_active = EXCLUDED.is_active,
    sort_order = EXCLUDED.sort_order,
    updated_at = now();

INSERT INTO experiences (
    profile_id,
    company,
    position,
    start_date,
    end_date,
    is_current,
    summary,
    responsibilities,
    technologies,
    sort_order,
    published
)
SELECT
    p.id,
    v.company,
    v.position,
    v.start_date::date,
    v.end_date::date,
    v.is_current,
    v.summary,
    v.responsibilities::json,
    v.technologies::json,
    v.sort_order,
    v.published
FROM profiles p
CROSS JOIN (
    VALUES
        (
            'Geosystems SA',
            'Desarrollador Full Stack GIS',
            '2023-01-01',
            NULL,
            TRUE,
            'Desarrollo de soluciones web geoespaciales, APIs REST, integración con servicios GIS y bases de datos espaciales.',
            '["Desarrollo e implementación de soluciones web geoespaciales.", "Construcción de APIs REST orientadas a datos espaciales.", "Optimización de consultas espaciales y flujos de acceso a datos.", "Integración de GeoServer, servicios OGC y componentes frontend.", "Desarrollo de interfaces interactivas con React, Leaflet y MapLibre."]',
            '["Python", "FastAPI", "PostgreSQL/PostGIS", "GeoServer", "QGIS", "React", "Leaflet", "MapLibre", "Docker", "Git"]',
            1,
            TRUE
        ),
        (
            'Paradigma del Sur SA',
            'Desarrollador Full Stack Jr',
            '2022-01-01',
            '2023-12-31',
            FALSE,
            'Desarrollo y mantenimiento de aplicaciones web, funcionalidades frontend/backend y resolución de incidencias técnicas.',
            '["Desarrollo de nuevas funcionalidades y mantenimiento de aplicaciones web.", "Implementación de interfaces dinámicas.", "Corrección de errores y mejoras de rendimiento.", "Colaboración con equipos de diseño y backend."]',
            '["JavaScript", "React", "Python", "Django", "SQL", "Git"]',
            2,
            TRUE
        ),
        (
            'Universidad Nacional del Sur',
            'Auxiliar de Investigación',
            '2021-01-01',
            '2022-12-31',
            FALSE,
            'Análisis geológico y geoespacial aplicado a la Cuenca Neuquina.',
            '["Procesamiento e interpretación de datos georreferenciados.", "Visualización de información geológica y territorial.", "Uso de herramientas GIS y análisis de datos."]',
            '["QGIS", "GIS", "Python", "Datos georreferenciados"]',
            3,
            TRUE
        ),
        (
            'Tutor Académico Independiente',
            'Tutor de Geología General y Carteo Geológico',
            '2018-01-01',
            '2020-12-31',
            FALSE,
            'Dictado de clases personalizadas de Geología General y Carteo Geológico.',
            '["Preparación de contenidos técnicos.", "Acompañamiento académico orientado a objetivos concretos."]',
            '["Geología", "Cartografía", "GIS"]',
            4,
            TRUE
        )
) AS v(
    company,
    position,
    start_date,
    end_date,
    is_current,
    summary,
    responsibilities,
    technologies,
    sort_order,
    published
)
WHERE p.slug = 'patricio-pagano'
ON CONFLICT (profile_id, company, position) DO UPDATE SET
    start_date = EXCLUDED.start_date,
    end_date = EXCLUDED.end_date,
    is_current = EXCLUDED.is_current,
    summary = EXCLUDED.summary,
    responsibilities = EXCLUDED.responsibilities,
    technologies = EXCLUDED.technologies,
    sort_order = EXCLUDED.sort_order,
    published = EXCLUDED.published,
    updated_at = now();


-- ============================================================
-- PROJECTS
-- ============================================================

INSERT INTO projects (
    title,
    slug,
    summary,
    description,
    project_type,
    status,
    cover_image_url,
    repository_url,
    demo_url,
    documentation_url,
    featured,
    published
)
VALUES
(
    'Portfolio Backend API',
    'portfolio-backend-api',
    'API REST desarrollada con FastAPI para administrar proyectos, tecnologías, dashboards y notebooks del portfolio profesional.',
    'Backend modular para portfolio profesional, construido con FastAPI, SQLAlchemy, PostgreSQL/PostGIS y Alembic. El objetivo es exponer de forma ordenada proyectos web, GIS, dashboards, notebooks y casos de estudio técnicos.',
    'api',
    'published',
    NULL,
    'https://github.com/ppagano91/portfolio-backend',
    NULL,
    NULL,
    TRUE,
    TRUE
),
(
    'Portfolio Web Profesional',
    'portfolio-web-profesional',
    'Frontend del portfolio profesional para publicar proyectos web, GIS, dashboards, notebooks y casos de estudio.',
    'Aplicación web orientada a mostrar experiencia profesional, proyectos técnicos, tecnologías utilizadas y trabajos vinculados a desarrollo GIS, datos espaciales, minería, Oil & Gas y geomática.',
    'web',
    'published',
    NULL,
    'https://github.com/ppagano91/portfolio-frontend',
    NULL,
    NULL,
    TRUE,
    TRUE
),
(
    'Visualizador Web GIS con MapLibre',
    'visualizador-web-gis-maplibre',
    'Visualizador cartográfico web para consumir capas geográficas, mostrar información territorial y trabajar con mapas interactivos.',
    'Proyecto GIS orientado a la visualización de capas geoespaciales mediante MapLibre, integración con servicios OGC y consultas de información territorial. Representa experiencia en frontend geoespacial, mapas web y consumo de servicios cartográficos.',
    'gis',
    'published',
    NULL,
    NULL,
    NULL,
    NULL,
    TRUE,
    TRUE
),
(
    'API GIS con PostgreSQL y PostGIS',
    'api-gis-postgresql-postgis',
    'API REST para consulta, administración y exposición de datos espaciales usando PostgreSQL/PostGIS.',
    'Backend geoespacial orientado a exponer entidades territoriales, consultas espaciales, filtros por geometría y servicios consumibles desde aplicaciones web GIS. Enfocado en buenas prácticas backend, rendimiento de consultas y separación de responsabilidades.',
    'gis',
    'published',
    NULL,
    NULL,
    NULL,
    NULL,
    TRUE,
    TRUE
),
(
    'Publicación de Servicios GIS con GeoServer',
    'publicacion-servicios-gis-geoserver',
    'Caso de estudio sobre publicación y consumo de servicios WMS, WMTS y TMS usando GeoServer.',
    'Proyecto orientado a documentar flujos de publicación de capas geográficas, configuración de servicios OGC, caché con GeoWebCache y consumo desde visores web. Útil para demostrar conocimientos en infraestructura GIS y servicios cartográficos.',
    'gis',
    'published',
    NULL,
    NULL,
    NULL,
    NULL,
    FALSE,
    TRUE
),
(
    'Dashboard de Indicadores Geoespaciales',
    'dashboard-indicadores-geoespaciales',
    'Dashboard para visualizar indicadores territoriales y datos georreferenciados.',
    'Dashboard pensado para analizar información espacial mediante indicadores, filtros y visualizaciones. Puede integrarse con datos PostgreSQL/PostGIS, archivos geográficos o fuentes externas.',
    'dashboard',
    'draft',
    NULL,
    NULL,
    NULL,
    NULL,
    TRUE,
    TRUE
),
(
    'Notebook de Análisis Geoespacial',
    'notebook-analisis-geoespacial',
    'Notebook técnico para análisis exploratorio de datos espaciales usando Python.',
    'Notebook orientado a procesamiento, limpieza, análisis y visualización de datos georreferenciados con Python, Pandas, GeoPandas y herramientas GIS. Pensado para mostrar capacidad de análisis territorial y ciencia de datos aplicada.',
    'notebook',
    'draft',
    NULL,
    NULL,
    NULL,
    NULL,
    TRUE,
    TRUE
),
(
    'Análisis Geológico de Cuenca Neuquina',
    'analisis-geologico-cuenca-neuquina',
    'Caso de estudio de análisis geológico y geoespacial aplicado a la Cuenca Neuquina.',
    'Proyecto orientado a integrar formación geológica, análisis espacial y visualización de datos georreferenciados. Puede evolucionar hacia un caso de estudio vinculado a Oil & Gas, reservorios o análisis territorial.',
    'data',
    'draft',
    NULL,
    NULL,
    NULL,
    NULL,
    FALSE,
    TRUE
),
(
    'Caso de Estudio GIS para Minería',
    'caso-estudio-gis-mineria',
    'Proyecto conceptual para análisis espacial aplicado a exploración, infraestructura o gestión territorial minera.',
    'Caso de estudio orientado a mostrar capacidades GIS aplicadas al sector minero: integración de capas geológicas, infraestructura, áreas de interés, accesibilidad y visualización cartográfica.',
    'gis',
    'draft',
    NULL,
    NULL,
    NULL,
    NULL,
    FALSE,
    TRUE
),
(
    'Sistema de Rutas Alternativas ante Cortes',
    'sistema-rutas-alternativas-cortes',
    'Backend GIS para simular rutas alternativas frente a cortes o afectaciones en una red vial.',
    'Proyecto técnico basado en PostgreSQL/PostGIS y lógica de ruteo para evaluar desvíos frente a cortes de tránsito. Representa experiencia avanzada en consultas espaciales, redes, geometrías y APIs GIS.',
    'gis',
    'draft',
    NULL,
    NULL,
    NULL,
    NULL,
    TRUE,
    TRUE
)
ON CONFLICT (slug) DO NOTHING;


-- ============================================================
-- PROJECT_TECHNOLOGIES
-- ============================================================

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'Python',
    'FastAPI',
    'PostgreSQL',
    'PostGIS',
    'SQLAlchemy',
    'Alembic',
    'Docker',
    'Git'
)
WHERE p.slug = 'portfolio-backend-api'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'React',
    'TypeScript',
    'JavaScript',
    'HTML',
    'CSS',
    'Git'
)
WHERE p.slug = 'portfolio-web-profesional'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'React',
    'TypeScript',
    'MapLibre',
    'PostGIS',
    'GeoServer',
    'WMS',
    'WMTS',
    'TMS'
)
WHERE p.slug = 'visualizador-web-gis-maplibre'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'Python',
    'FastAPI',
    'PostgreSQL',
    'PostGIS',
    'SQL',
    'SQLAlchemy',
    'Docker'
)
WHERE p.slug = 'api-gis-postgresql-postgis'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'GeoServer',
    'GeoNetwork',
    'QGIS',
    'WMS',
    'WMTS',
    'TMS',
    'PostGIS'
)
WHERE p.slug = 'publicacion-servicios-gis-geoserver'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'Power BI',
    'PostgreSQL',
    'PostGIS',
    'SQL',
    'Python'
)
WHERE p.slug = 'dashboard-indicadores-geoespaciales'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'Python',
    'Pandas',
    'GeoPandas',
    'Jupyter Notebook',
    'QGIS',
    'PostGIS'
)
WHERE p.slug = 'notebook-analisis-geoespacial'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'Python',
    'QGIS',
    'PostGIS',
    'GeoPandas',
    'Jupyter Notebook'
)
WHERE p.slug = 'analisis-geologico-cuenca-neuquina'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'QGIS',
    'PostGIS',
    'GeoServer',
    'MapLibre',
    'Python',
    'GeoPandas'
)
WHERE p.slug = 'caso-estudio-gis-mineria'
ON CONFLICT DO NOTHING;

INSERT INTO project_technologies (project_id, technology_id)
SELECT p.id, t.id
FROM projects p
JOIN technologies t ON t.name IN (
    'Python',
    'FastAPI',
    'PostgreSQL',
    'PostGIS',
    'SQL',
    'MapLibre',
    'Docker'
)
WHERE p.slug = 'sistema-rutas-alternativas-cortes'
ON CONFLICT DO NOTHING;


-- ============================================================
-- DASHBOARDS
-- ============================================================

INSERT INTO dashboards (
    title,
    description,
    tool,
    embed_url,
    public_url,
    project_id
)
SELECT
    'Dashboard de Indicadores Geoespaciales',
    'Dashboard orientado a indicadores territoriales, análisis espacial y visualización de datos georreferenciados.',
    'powerbi',
    NULL,
    NULL,
    p.id
FROM projects p
WHERE p.slug = 'dashboard-indicadores-geoespaciales'
ON CONFLICT DO NOTHING;

INSERT INTO dashboards (
    title,
    description,
    tool,
    embed_url,
    public_url,
    project_id
)
SELECT
    'Dashboard GIS para Minería',
    'Dashboard conceptual para análisis de capas geológicas, infraestructura, accesibilidad y áreas de interés minero.',
    'powerbi',
    NULL,
    NULL,
    p.id
FROM projects p
WHERE p.slug = 'caso-estudio-gis-mineria'
ON CONFLICT DO NOTHING;


-- ============================================================
-- NOTEBOOKS
-- ============================================================

INSERT INTO notebooks (
    title,
    description,
    notebook_url,
    repository_url,
    project_id
)
SELECT
    'Análisis Exploratorio de Datos Espaciales con Python',
    'Notebook para limpieza, procesamiento, análisis y visualización de datos georreferenciados usando Python, Pandas y GeoPandas.',
    NULL,
    NULL,
    p.id
FROM projects p
WHERE p.slug = 'notebook-analisis-geoespacial'
ON CONFLICT DO NOTHING;

INSERT INTO notebooks (
    title,
    description,
    notebook_url,
    repository_url,
    project_id
)
SELECT
    'Análisis Geoespacial de la Cuenca Neuquina',
    'Notebook orientado a integrar datos geológicos y espaciales para análisis territorial aplicado a la Cuenca Neuquina.',
    NULL,
    NULL,
    p.id
FROM projects p
WHERE p.slug = 'analisis-geologico-cuenca-neuquina'
ON CONFLICT DO NOTHING;


-- ============================================================
-- PROJECT_LOCATIONS
-- Requiere tabla con geom geometry(Point, 4326)
-- ============================================================

INSERT INTO project_locations (
    project_id,
    name,
    description,
    geom
)
SELECT
    p.id,
    'Argentina',
    'Ubicación general asociada al portfolio profesional y proyectos GIS/datos.',
    ST_SetSRID(ST_MakePoint(-64.0, -34.0), 4326)
FROM projects p
WHERE p.slug = 'portfolio-web-profesional'
ON CONFLICT DO NOTHING;

INSERT INTO project_locations (
    project_id,
    name,
    description,
    geom
)
SELECT
    p.id,
    'Ciudad Autónoma de Buenos Aires',
    'Área de referencia para proyectos de visualización urbana, servicios GIS y datos territoriales.',
    ST_SetSRID(ST_MakePoint(-58.3816, -34.6037), 4326)
FROM projects p
WHERE p.slug = 'visualizador-web-gis-maplibre'
ON CONFLICT DO NOTHING;

INSERT INTO project_locations (
    project_id,
    name,
    description,
    geom
)
SELECT
    p.id,
    'Cuenca Neuquina',
    'Área de referencia para análisis geológico, geoespacial y casos vinculados a Oil & Gas.',
    ST_SetSRID(ST_MakePoint(-68.5, -38.5), 4326)
FROM projects p
WHERE p.slug = 'analisis-geologico-cuenca-neuquina'
ON CONFLICT DO NOTHING;

INSERT INTO project_locations (
    project_id,
    name,
    description,
    geom
)
SELECT
    p.id,
    'Argentina - Región Minera',
    'Ubicación conceptual para casos de estudio GIS aplicados a minería.',
    ST_SetSRID(ST_MakePoint(-66.0, -28.0), 4326)
FROM projects p
WHERE p.slug = 'caso-estudio-gis-mineria'
ON CONFLICT DO NOTHING;


-- ============================================================
-- CONTACT_MESSAGES
-- En general no conviene poblar mensajes reales.
-- Dejo uno de prueba para ambiente local.
-- ============================================================

INSERT INTO contact_messages (
    name,
    email,
    subject,
    message,
    read
)
VALUES
(
    'Usuario de prueba',
    'test@example.com',
    'Consulta sobre portfolio',
    'Mensaje de prueba para validar el endpoint de contacto.',
    FALSE
)
ON CONFLICT DO NOTHING;


COMMIT;