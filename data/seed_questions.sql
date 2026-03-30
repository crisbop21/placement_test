-- Schema and seed data for the Sustainability Diagnostic Tool

-- Questions table
CREATE TABLE IF NOT EXISTS questions (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_num    int NOT NULL,
  axis         text NOT NULL CHECK (axis IN ('governance','environmental','social','reporting','economic')),
  block        text NOT NULL,
  text_es      text NOT NULL,
  text_en      text NOT NULL,
  option_a_es  text NOT NULL,
  option_a_en  text NOT NULL,
  option_b_es  text NOT NULL,
  option_b_en  text NOT NULL,
  option_c_es  text NOT NULL,
  option_c_en  text NOT NULL,
  option_d_es  text NOT NULL,
  option_d_en  text NOT NULL,
  score_a      int NOT NULL DEFAULT 1,
  score_b      int NOT NULL DEFAULT 2,
  score_c      int NOT NULL DEFAULT 3,
  score_d      int NOT NULL DEFAULT 4,
  weight       float NOT NULL DEFAULT 1.0,
  is_active    boolean NOT NULL DEFAULT true
);

-- Responses table
CREATE TABLE IF NOT EXISTS responses (
  id                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at            timestamptz DEFAULT now(),
  language              text,
  company_name          text,
  sector                text,
  company_size          text,
  respondent_name       text,
  respondent_role       text,
  answers               jsonb,
  score_governance      float,
  score_environmental   float,
  score_social          float,
  score_reporting       float,
  score_economic        float,
  overall_score         float,
  maturity_stage        int,
  recommended_courses   jsonb,
  pdf_generated         boolean DEFAULT false
);

-- Course rules table (optional for v1)
CREATE TABLE IF NOT EXISTS course_rules (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stage        int NOT NULL,
  axis         text,
  course_name  text NOT NULL,
  priority     int NOT NULL,
  is_active    boolean DEFAULT true
);

-- Seed 25 questions (5 per axis)

-- GOVERNANCE (Block A)
INSERT INTO questions (order_num, axis, block, text_es, text_en, option_a_es, option_a_en, option_b_es, option_b_en, option_c_es, option_c_en, option_d_es, option_d_en) VALUES
(1, 'governance', 'A', '¿Su organización cuenta con una política formal de sostenibilidad?', 'Does your organization have a formal sustainability policy?', 'No tenemos ninguna política', 'We have no policy', 'Estamos en proceso de desarrollo', 'We are in the process of developing one', 'Tenemos una política básica documentada', 'We have a basic documented policy', 'Tenemos una política integral revisada periódicamente', 'We have a comprehensive policy reviewed periodically'),
(2, 'governance', 'A', '¿Existe un comité o responsable de sostenibilidad en su empresa?', 'Is there a sustainability committee or officer in your company?', 'No existe ningún responsable', 'There is no responsible person', 'Hay una persona asignada parcialmente', 'There is a partially assigned person', 'Existe un responsable dedicado', 'There is a dedicated officer', 'Existe un comité formal con reuniones periódicas', 'There is a formal committee with regular meetings'),
(3, 'governance', 'A', '¿Cómo integra su empresa la sostenibilidad en la toma de decisiones estratégicas?', 'How does your company integrate sustainability into strategic decision-making?', 'No se considera en las decisiones', 'It is not considered in decisions', 'Se considera ocasionalmente', 'It is considered occasionally', 'Es un factor en la planificación anual', 'It is a factor in annual planning', 'Está integrada en toda decisión estratégica', 'It is integrated into every strategic decision'),
(4, 'governance', 'A', '¿Su empresa realiza evaluaciones de riesgos ESG?', 'Does your company conduct ESG risk assessments?', 'No realizamos evaluaciones', 'We do not conduct assessments', 'Realizamos evaluaciones informales', 'We conduct informal assessments', 'Realizamos evaluaciones anuales estructuradas', 'We conduct structured annual assessments', 'Tenemos un sistema continuo de gestión de riesgos ESG', 'We have a continuous ESG risk management system'),
(5, 'governance', 'A', '¿Cómo gestiona su organización la ética y el cumplimiento normativo?', 'How does your organization manage ethics and regulatory compliance?', 'No tenemos procesos formales', 'We have no formal processes', 'Cumplimos con lo mínimo legal', 'We comply with the legal minimum', 'Tenemos un programa de compliance básico', 'We have a basic compliance program', 'Tenemos un programa integral de ética y compliance', 'We have a comprehensive ethics and compliance program');

-- ENVIRONMENTAL (Block B)
INSERT INTO questions (order_num, axis, block, text_es, text_en, option_a_es, option_a_en, option_b_es, option_b_en, option_c_es, option_c_en, option_d_es, option_d_en) VALUES
(6, 'environmental', 'B', '¿Su empresa mide su huella de carbono?', 'Does your company measure its carbon footprint?', 'No medimos emisiones', 'We do not measure emissions', 'Tenemos una estimación básica', 'We have a basic estimate', 'Medimos alcance 1 y 2 anualmente', 'We measure scope 1 and 2 annually', 'Medimos alcances 1, 2 y 3 con verificación externa', 'We measure scopes 1, 2, and 3 with external verification'),
(7, 'environmental', 'B', '¿Cuenta con una estrategia de gestión de residuos?', 'Do you have a waste management strategy?', 'No tenemos estrategia', 'We have no strategy', 'Separamos algunos residuos', 'We separate some waste', 'Tenemos un plan de reducción y reciclaje', 'We have a reduction and recycling plan', 'Aplicamos economía circular en nuestros procesos', 'We apply circular economy in our processes'),
(8, 'environmental', 'B', '¿Su empresa tiene metas de reducción de consumo energético?', 'Does your company have energy consumption reduction targets?', 'No tenemos metas', 'We have no targets', 'Tenemos metas informales', 'We have informal targets', 'Tenemos metas documentadas a corto plazo', 'We have documented short-term targets', 'Tenemos metas ambiciosas con seguimiento continuo', 'We have ambitious targets with continuous monitoring'),
(9, 'environmental', 'B', '¿Cómo gestiona su empresa el uso del agua?', 'How does your company manage water use?', 'No gestionamos el consumo de agua', 'We do not manage water consumption', 'Monitoreamos el consumo básico', 'We monitor basic consumption', 'Tenemos programa de eficiencia hídrica', 'We have a water efficiency program', 'Gestión integral con metas de reducción y reutilización', 'Comprehensive management with reduction and reuse targets'),
(10, 'environmental', 'B', '¿Su organización evalúa el impacto ambiental de su cadena de suministro?', 'Does your organization assess the environmental impact of its supply chain?', 'No evaluamos la cadena', 'We do not assess the chain', 'Evaluamos proveedores principales', 'We assess main suppliers', 'Tenemos criterios ambientales para proveedores', 'We have environmental criteria for suppliers', 'Gestión ambiental integral de toda la cadena', 'Comprehensive environmental management of the entire chain');

-- SOCIAL (Block C)
INSERT INTO questions (order_num, axis, block, text_es, text_en, option_a_es, option_a_en, option_b_es, option_b_en, option_c_es, option_c_en, option_d_es, option_d_en) VALUES
(11, 'social', 'C', '¿Su empresa tiene programas de diversidad e inclusión?', 'Does your company have diversity and inclusion programs?', 'No tenemos programas', 'We have no programs', 'Tenemos iniciativas informales', 'We have informal initiatives', 'Tenemos un programa estructurado', 'We have a structured program', 'Tenemos un programa integral con métricas y metas', 'We have a comprehensive program with metrics and targets'),
(12, 'social', 'C', '¿Cómo gestiona su empresa la salud y seguridad ocupacional?', 'How does your company manage occupational health and safety?', 'Cumplimos solo lo legal mínimo', 'We comply only with the legal minimum', 'Tenemos un programa básico', 'We have a basic program', 'Tenemos un sistema de gestión certificado', 'We have a certified management system', 'Cultura de seguridad integral con mejora continua', 'Comprehensive safety culture with continuous improvement'),
(13, 'social', 'C', '¿Su empresa invierte en desarrollo profesional de sus empleados?', 'Does your company invest in employee professional development?', 'No invertimos en capacitación', 'We do not invest in training', 'Ofrecemos capacitación básica', 'We offer basic training', 'Tenemos un plan anual de desarrollo', 'We have an annual development plan', 'Plan integral de carrera con mentoría y formación continua', 'Comprehensive career plan with mentoring and continuous training'),
(14, 'social', 'C', '¿Su organización realiza inversión social o comunitaria?', 'Does your organization make social or community investment?', 'No realizamos inversión social', 'We do not make social investment', 'Hacemos donaciones ocasionales', 'We make occasional donations', 'Tenemos un programa de responsabilidad social', 'We have a social responsibility program', 'Inversión social estratégica alineada con el negocio', 'Strategic social investment aligned with the business'),
(15, 'social', 'C', '¿Cómo gestiona su empresa las relaciones con grupos de interés?', 'How does your company manage stakeholder relations?', 'No identificamos grupos de interés', 'We do not identify stakeholders', 'Identificamos los principales grupos', 'We identify the main groups', 'Dialogamos periódicamente con stakeholders', 'We regularly dialogue with stakeholders', 'Gestión integral de stakeholders con impacto medible', 'Comprehensive stakeholder management with measurable impact');

-- REPORTING (Block D)
INSERT INTO questions (order_num, axis, block, text_es, text_en, option_a_es, option_a_en, option_b_es, option_b_en, option_c_es, option_c_en, option_d_es, option_d_en) VALUES
(16, 'reporting', 'D', '¿Su empresa publica un informe de sostenibilidad?', 'Does your company publish a sustainability report?', 'No publicamos informes', 'We do not publish reports', 'Publicamos información básica en la web', 'We publish basic information on our website', 'Publicamos un informe anual', 'We publish an annual report', 'Informe bajo estándares internacionales con verificación', 'Report under international standards with verification'),
(17, 'reporting', 'D', '¿Qué marcos de reporte utiliza su organización?', 'What reporting frameworks does your organization use?', 'Ninguno', 'None', 'Usamos un marco básico interno', 'We use a basic internal framework', 'Seguimos GRI o similar', 'We follow GRI or similar', 'Múltiples marcos (GRI, IFRS, CSRD) integrados', 'Multiple frameworks (GRI, IFRS, CSRD) integrated'),
(18, 'reporting', 'D', '¿Cómo comunica su empresa sus avances en sostenibilidad a inversores?', 'How does your company communicate sustainability progress to investors?', 'No comunicamos a inversores', 'We do not communicate to investors', 'Comunicación reactiva bajo demanda', 'Reactive communication on demand', 'Sección dedicada en el informe anual', 'Dedicated section in the annual report', 'Comunicación proactiva con métricas ESG integradas', 'Proactive communication with integrated ESG metrics'),
(19, 'reporting', 'D', '¿Su empresa realiza análisis de doble materialidad?', 'Does your company conduct double materiality analysis?', 'No sabemos qué es materialidad', 'We do not know what materiality is', 'Conocemos el concepto pero no lo aplicamos', 'We know the concept but do not apply it', 'Realizamos análisis de materialidad simple', 'We conduct simple materiality analysis', 'Realizamos doble materialidad con stakeholders', 'We conduct double materiality with stakeholders'),
(20, 'reporting', 'D', '¿Sus datos de sostenibilidad son verificados externamente?', 'Is your sustainability data externally verified?', 'No verificamos datos', 'We do not verify data', 'Verificación interna básica', 'Basic internal verification', 'Verificación externa parcial', 'Partial external verification', 'Verificación externa completa por tercero acreditado', 'Full external verification by accredited third party');

-- ECONOMIC (Block E)
INSERT INTO questions (order_num, axis, block, text_es, text_en, option_a_es, option_a_en, option_b_es, option_b_en, option_c_es, option_c_en, option_d_es, option_d_en) VALUES
(21, 'economic', 'E', '¿Su empresa integra criterios de sostenibilidad en su estrategia financiera?', 'Does your company integrate sustainability criteria into its financial strategy?', 'No los integramos', 'We do not integrate them', 'Consideramos algunos factores ESG', 'We consider some ESG factors', 'Los criterios ESG están en la planificación financiera', 'ESG criteria are in financial planning', 'Finanzas sostenibles integradas con productos verdes', 'Sustainable finance integrated with green products'),
(22, 'economic', 'E', '¿Su empresa mide el retorno de inversión de sus iniciativas de sostenibilidad?', 'Does your company measure the ROI of its sustainability initiatives?', 'No medimos ROI de sostenibilidad', 'We do not measure sustainability ROI', 'Estimamos beneficios cualitativos', 'We estimate qualitative benefits', 'Medimos ROI de algunas iniciativas', 'We measure ROI of some initiatives', 'Medición integral de ROI con KPIs financieros ESG', 'Comprehensive ROI measurement with ESG financial KPIs'),
(23, 'economic', 'E', '¿Cómo gestiona su empresa la innovación sostenible?', 'How does your company manage sustainable innovation?', 'No tenemos enfoque en innovación sostenible', 'We have no focus on sustainable innovation', 'Exploramos oportunidades ocasionalmente', 'We explore opportunities occasionally', 'Tenemos un programa de innovación con criterios ESG', 'We have an innovation program with ESG criteria', 'I+D integrado con sostenibilidad y economía circular', 'R&D integrated with sustainability and circular economy'),
(24, 'economic', 'E', '¿Su empresa evalúa riesgos financieros relacionados con el cambio climático?', 'Does your company assess financial risks related to climate change?', 'No evaluamos riesgos climáticos', 'We do not assess climate risks', 'Reconocemos los riesgos de forma general', 'We recognize risks in general terms', 'Evaluación de riesgos climáticos en planificación', 'Climate risk assessment in planning', 'Análisis TCFD con escenarios y estrategias de adaptación', 'TCFD analysis with scenarios and adaptation strategies'),
(25, 'economic', 'E', '¿Su organización busca activamente acceso a financiamiento verde o sostenible?', 'Does your organization actively seek access to green or sustainable financing?', 'No buscamos financiamiento verde', 'We do not seek green financing', 'Conocemos las opciones disponibles', 'We know the available options', 'Hemos accedido a algún instrumento verde', 'We have accessed some green instrument', 'Estrategia activa de financiamiento sostenible diversificado', 'Active strategy of diversified sustainable financing');
