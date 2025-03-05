// Запрос для просмотра всех зависимостей компонентов
// Этот запрос показывает все компоненты и их зависимости

// Просмотр всех компонентов
MATCH (c:Component)
RETURN c.name AS Component, c.type AS Type, c.description AS Description
ORDER BY c.type, c.name;

// Просмотр всех зависимостей между компонентами
MATCH (a:Component)-[:DEPENDS_ON]->(b:Component)
RETURN a.name AS SourceComponent, a.type AS SourceType, 
       b.name AS TargetComponent, b.type AS TargetType
ORDER BY a.type, a.name, b.type, b.name;

// Просмотр зависимостей по типам компонентов
MATCH (a:Component)-[:DEPENDS_ON]->(b:Component)
RETURN a.type AS SourceType, b.type AS TargetType, count(*) AS DependencyCount
ORDER BY DependencyCount DESC; 