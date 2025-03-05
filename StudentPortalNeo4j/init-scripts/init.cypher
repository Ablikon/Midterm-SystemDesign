// Очистка базы данных перед инициализацией
MATCH (n) DETACH DELETE n;

// Создание индексов для ускорения запросов
CREATE INDEX component_name IF NOT EXISTS FOR (c:Component) ON (c.name);
CREATE INDEX component_type IF NOT EXISTS FOR (c:Component) ON (c.type);

// Создание компонентов, сгруппированных по типам
// Клиентский уровень
CREATE (WebApp:Component {name: "WebApp", type: "Client", description: "Веб-приложение (React)"});
CREATE (MobileApp:Component {name: "MobileApp", type: "Client", description: "Мобильное приложение (React Native)"});
CREATE (ThirdParty:Component {name: "ThirdParty", type: "Client", description: "Интеграции третьих сторон (API)"});

// Компоненты уровня API Gateway
CREATE (APIGateway:Component {name: "APIGateway", type: "Gateway", description: "API Gateway"});
CREATE (Auth:Component {name: "Auth", type: "Gateway", description: "Компонент аутентификации API Gateway"});
CREATE (RateLimit:Component {name: "RateLimit", type: "Gateway", description: "Компонент ограничения запросов API Gateway"});
CREATE (Routing:Component {name: "Routing", type: "Gateway", description: "Компонент маршрутизации API Gateway"});
CREATE (Logging:Component {name: "Logging", type: "Gateway", description: "Компонент логирования API Gateway"});

// Сервисный уровень
CREATE (AuthService:Component {name: "AuthService", type: "Service", description: "Сервис аутентификации"});
CREATE (CoreAPIs:Component {name: "CoreAPIs", type: "Service", description: "Основные API"});
CREATE (IntegrationServices:Component {name: "IntegrationServices", type: "Service", description: "Интеграционные сервисы"});

// Уровень микросервисов - Академические сервисы
CREATE (AcademicManagement:Component {name: "AcademicManagement", type: "Academic", description: "Управление академическими программами"});
CREATE (CourseManagement:Component {name: "CourseManagement", type: "Academic", description: "Управление курсами"});
CREATE (Grading:Component {name: "Grading", type: "Academic", description: "Система оценок"});
CREATE (Scheduling:Component {name: "Scheduling", type: "Academic", description: "Расписание"});

// Уровень микросервисов - Административные сервисы
CREATE (AdminPanel:Component {name: "AdminPanel", type: "Admin", description: "Административная панель"});
CREATE (ReportingAnalytics:Component {name: "ReportingAnalytics", type: "Admin", description: "Отчетность и аналитика"});
CREATE (TenantManagement:Component {name: "TenantManagement", type: "Admin", description: "Управление учреждениями"});

// Уровень микросервисов - Студенческие сервисы
CREATE (StudentProfile:Component {name: "StudentProfile", type: "Student", description: "Профиль студента"});
CREATE (Enrollment:Component {name: "Enrollment", type: "Student", description: "Зачисление"});
CREATE (Attendance:Component {name: "Attendance", type: "Student", description: "Посещаемость"});
CREATE (FinancialAid:Component {name: "FinancialAid", type: "Student", description: "Финансовая помощь"});

// Уровень микросервисов - Вспомогательные сервисы
CREATE (Communication:Component {name: "Communication", type: "Support", description: "Коммуникации"});
CREATE (Library:Component {name: "Library", type: "Support", description: "Библиотека"});
CREATE (ExchangeProgram:Component {name: "ExchangeProgram", type: "Support", description: "Программы обмена"});
CREATE (EventManagement:Component {name: "EventManagement", type: "Support", description: "Управление мероприятиями"});

// Уровень данных - Реляционные БД
CREATE (PostgreSQL:Component {name: "PostgreSQL", type: "Database", description: "PostgreSQL (Мульти-тенантная)"});
CREATE (ReadReplicas:Component {name: "ReadReplicas", type: "Database", description: "Реплики для чтения"});

// Уровень данных - Кэширование
CREATE (Redis:Component {name: "Redis", type: "Cache", description: "Redis кластер"});

// Уровень данных - Файловое хранилище
CREATE (S3:Component {name: "S3", type: "Storage", description: "Объектное хранилище (S3)"});

// Уровень данных - Аналитика
CREATE (DataWarehouse:Component {name: "DataWarehouse", type: "Analytics", description: "Хранилище данных"});
CREATE (ElasticSearch:Component {name: "ElasticSearch", type: "Analytics", description: "ElasticSearch"});

// Общие компоненты
CREATE (Security:Component {name: "Security", type: "Common", description: "Безопасность"});
CREATE (Monitoring:Component {name: "Monitoring", type: "Common", description: "Мониторинг"});
CREATE (Logging2:Component {name: "Logging2", type: "Common", description: "Логирование приложений"});
CREATE (i18n:Component {name: "i18n", type: "Common", description: "Интернационализация"});

// Фронтенд компоненты
CREATE (UI:Component {name: "UI", type: "Frontend", description: "UI компоненты"});
CREATE (StateManagement:Component {name: "StateManagement", type: "Frontend", description: "Управление состоянием (Redux)"});
CREATE (RouteManagement:Component {name: "RouteManagement", type: "Frontend", description: "Управление маршрутами"});
CREATE (FormValidation:Component {name: "FormValidation", type: "Frontend", description: "Валидация форм"});
CREATE (I18NComponent:Component {name: "I18NComponent", type: "Frontend", description: "Интернационализация"});
CREATE (APIClient:Component {name: "APIClient", type: "Frontend", description: "API клиент"});
CREATE (PWAComponents:Component {name: "PWAComponents", type: "Frontend", description: "PWA компоненты"});

// Сервисы аутентификации
CREATE (AuthAPI:Component {name: "AuthAPI", type: "Auth", description: "Auth API"});
CREATE (OAuthProvider:Component {name: "OAuthProvider", type: "Auth", description: "OAuth Provider"});
CREATE (TokenService:Component {name: "TokenService", type: "Auth", description: "Сервис токенов"});
CREATE (MFAService:Component {name: "MFAService", type: "Auth", description: "MFA сервис"});
CREATE (UserIdentity:Component {name: "UserIdentity", type: "Auth", description: "Управление идентификацией"});

// Академические сервисы
CREATE (ProgramAPI:Component {name: "ProgramAPI", type: "Academic", description: "API программ обучения"});
CREATE (CourseAPI:Component {name: "CourseAPI", type: "Academic", description: "API курсов"});
CREATE (ScheduleAPI:Component {name: "ScheduleAPI", type: "Academic", description: "API расписания"});
CREATE (EnrollmentAPI:Component {name: "EnrollmentAPI", type: "Academic", description: "API зачисления"});
CREATE (GradeAPI:Component {name: "GradeAPI", type: "Academic", description: "API оценок"});
CREATE (AttendanceAPI:Component {name: "AttendanceAPI", type: "Academic", description: "API посещаемости"});

// Студенческие сервисы
CREATE (ProfileAPI:Component {name: "ProfileAPI", type: "Student", description: "API профиля"});
CREATE (FinanceAPI:Component {name: "FinanceAPI", type: "Student", description: "API финансов"});
CREATE (DocumentAPI:Component {name: "DocumentAPI", type: "Student", description: "API документов"});
CREATE (ApplicationAPI:Component {name: "ApplicationAPI", type: "Student", description: "API заявлений"});

// Административные сервисы
CREATE (TenantAPI:Component {name: "TenantAPI", type: "Admin", description: "API учреждений"});
CREATE (UserManagementAPI:Component {name: "UserManagementAPI", type: "Admin", description: "API управления пользователями"});
CREATE (ConfigAPI:Component {name: "ConfigAPI", type: "Admin", description: "API конфигурации"});
CREATE (AuditAPI:Component {name: "AuditAPI", type: "Admin", description: "API аудита"});
CREATE (ReportingAPI:Component {name: "ReportingAPI", type: "Admin", description: "API отчетности"});

// Интеграционные компоненты
CREATE (Integration:Component {name: "Integration", type: "Integration", description: "Интеграционный слой"});
CREATE (EventBus:Component {name: "EventBus", type: "Integration", description: "Шина событий"});
CREATE (Webhooks:Component {name: "Webhooks", type: "Integration", description: "Webhooks"});
CREATE (DataImport:Component {name: "DataImport", type: "Integration", description: "Импорт данных"});
CREATE (DataExport:Component {name: "DataExport", type: "Integration", description: "Экспорт данных"});

// Сервисы хранения данных
CREATE (DBServices:Component {name: "DBServices", type: "Data", description: "Сервисы базы данных"});
CREATE (CachingServices:Component {name: "CachingServices", type: "Data", description: "Сервисы кэширования"});
CREATE (StorageServices:Component {name: "StorageServices", type: "Data", description: "Сервисы хранения файлов"});
CREATE (SearchServices:Component {name: "SearchServices", type: "Data", description: "Сервисы поиска"});

// Создание связей между компонентами
// API Gateway связи
MATCH (a:Component {name: "APIGateway"}), (b:Component {name: "Auth"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIGateway"}), (b:Component {name: "RateLimit"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIGateway"}), (b:Component {name: "Routing"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIGateway"}), (b:Component {name: "Logging"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Основные сервисные связи
MATCH (a:Component {name: "AuthService"}), (b:Component {name: "Security"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "CoreAPIs"}), (b:Component {name: "AcademicManagement"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "CoreAPIs"}), (b:Component {name: "StudentProfile"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "CoreAPIs"}), (b:Component {name: "AdminPanel"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "CoreAPIs"}), (b:Component {name: "Communication"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Связи с базами данных
MATCH (a:Component {name: "AcademicManagement"}), (b:Component {name: "PostgreSQL"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "CourseManagement"}), (b:Component {name: "PostgreSQL"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Grading"}), (b:Component {name: "PostgreSQL"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "AdminPanel"}), (b:Component {name: "PostgreSQL"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "StudentProfile"}), (b:Component {name: "PostgreSQL"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Enrollment"}), (b:Component {name: "PostgreSQL"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Library"}), (b:Component {name: "S3"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Communication"}), (b:Component {name: "Redis"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Реплики и кэширование
MATCH (a:Component {name: "PostgreSQL"}), (b:Component {name: "ReadReplicas"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ReadReplicas"}), (b:Component {name: "PostgreSQL"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "AcademicManagement"}), (b:Component {name: "Redis"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ReportingAnalytics"}), (b:Component {name: "DataWarehouse"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ReportingAnalytics"}), (b:Component {name: "ElasticSearch"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Логирование и мониторинг
MATCH (a:Component {name: "Logging"}), (b:Component {name: "Monitoring"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Logging2"}), (b:Component {name: "Monitoring"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Фронтенд зависимости
MATCH (a:Component {name: "UI"}), (b:Component {name: "APIClient"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "StateManagement"}), (b:Component {name: "APIClient"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIClient"}), (b:Component {name: "AuthAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIClient"}), (b:Component {name: "ProgramAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIClient"}), (b:Component {name: "ProfileAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIClient"}), (b:Component {name: "TenantAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Сервисы аутентификации
MATCH (a:Component {name: "AuthAPI"}), (b:Component {name: "UserIdentity"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "UserIdentity"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Академические API
MATCH (a:Component {name: "ProgramAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "CourseAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ScheduleAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "EnrollmentAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "GradeAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "AttendanceAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Студенческие API
MATCH (a:Component {name: "ProfileAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "FinanceAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "DocumentAPI"}), (b:Component {name: "StorageServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ApplicationAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Административные API
MATCH (a:Component {name: "TenantAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "UserManagementAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ConfigAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "AuditAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ReportingAPI"}), (b:Component {name: "DBServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Кэширование
MATCH (a:Component {name: "ProgramAPI"}), (b:Component {name: "CachingServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "CourseAPI"}), (b:Component {name: "CachingServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ProfileAPI"}), (b:Component {name: "CachingServices"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Интеграционные компоненты
MATCH (a:Component {name: "Integration"}), (b:Component {name: "EventBus"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "EventBus"}), (b:Component {name: "AuthAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "EventBus"}), (b:Component {name: "ProgramAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "EventBus"}), (b:Component {name: "ProfileAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "EventBus"}), (b:Component {name: "TenantAPI"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Integration"}), (b:Component {name: "Webhooks"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Integration"}), (b:Component {name: "DataImport"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "Integration"}), (b:Component {name: "DataExport"})
CREATE (a)-[:DEPENDS_ON]->(b);

// Web и Mobile приложения зависят от API Gateway
MATCH (a:Component {name: "WebApp"}), (b:Component {name: "APIGateway"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "MobileApp"}), (b:Component {name: "APIGateway"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "ThirdParty"}), (b:Component {name: "APIGateway"})
CREATE (a)-[:DEPENDS_ON]->(b);

// API Gateway зависит от сервисного уровня
MATCH (a:Component {name: "APIGateway"}), (b:Component {name: "AuthService"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIGateway"}), (b:Component {name: "CoreAPIs"})
CREATE (a)-[:DEPENDS_ON]->(b);

MATCH (a:Component {name: "APIGateway"}), (b:Component {name: "IntegrationServices"})
CREATE (a)-[:DEPENDS_ON]->(b); 