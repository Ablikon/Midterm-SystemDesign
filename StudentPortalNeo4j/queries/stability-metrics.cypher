// Запрос для расчета метрик стабильности компонентов
// Этот запрос рассчитывает fan-in, fan-out и instability для каждого компонента

// Основной запрос для расчета метрик
MATCH (c:Component)
OPTIONAL MATCH (c)<-[:DEPENDS_ON]-(in:Component)
WITH c, COLLECT(in) AS inComponents
OPTIONAL MATCH (c)-[:DEPENDS_ON]->(out:Component)
WITH c, inComponents, COLLECT(out) AS outComponents
WITH c, 
     SIZE(inComponents) AS fanIn,
     SIZE(outComponents) AS fanOut
WITH c, fanIn, fanOut,
     CASE WHEN fanIn + fanOut = 0 THEN 0 ELSE toFloat(fanOut) / (fanIn + fanOut) END AS instability
RETURN c.name AS Component,
       c.type AS Type,
       fanIn AS FanIn,
       fanOut AS FanOut,
       instability AS Instability
ORDER BY instability;

// Сохранение результатов в формате Markdown таблицы
MATCH (c:Component)
OPTIONAL MATCH (c)<-[:DEPENDS_ON]-(in:Component)
WITH c, COLLECT(in) AS inComponents
OPTIONAL MATCH (c)-[:DEPENDS_ON]->(out:Component)
WITH c, inComponents, COLLECT(out) AS outComponents
WITH c, 
     SIZE(inComponents) AS fanIn,
     SIZE(outComponents) AS fanOut
WITH c, fanIn, fanOut,
     CASE WHEN fanIn + fanOut = 0 THEN 0 ELSE toFloat(fanOut) / (fanIn + fanOut) END AS instability
RETURN "| " + c.name + " | " + c.type + " | " + toString(fanIn) + " | " + toString(fanOut) + " | " + toString(round(1000 * instability) / 1000) + " |" AS MarkdownRow
ORDER BY instability;

// Анализ стабильности по типам компонентов
MATCH (c:Component)
OPTIONAL MATCH (c)<-[:DEPENDS_ON]-(in:Component)
WITH c, COLLECT(in) AS inComponents
OPTIONAL MATCH (c)-[:DEPENDS_ON]->(out:Component)
WITH c, inComponents, COLLECT(out) AS outComponents
WITH c, 
     SIZE(inComponents) AS fanIn,
     SIZE(outComponents) AS fanOut,
     CASE WHEN fanIn + fanOut = 0 THEN 0 ELSE toFloat(fanOut) / (fanIn + fanOut) END AS instability
RETURN c.type AS Type,
       AVG(instability) AS AverageInstability,
       COUNT(c) AS ComponentCount,
       SUM(fanIn) AS TotalFanIn,
       SUM(fanOut) AS TotalFanOut
ORDER BY AverageInstability; 