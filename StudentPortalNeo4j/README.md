# Анализ стабильности компонентов Global Student Portal с использованием Neo4j


## Содержание

- [Обзор](#обзор)
- [Метрики стабильности](#метрики-стабильности)
- [Структура проекта](#структура-проекта)
- [Запуск проекта](#запуск-проекта)
- [Запросы для анализа](#запросы-для-анализа)
- [Результаты анализа](#результаты-анализа)

## Обзор

Архитектурная стабильность - это мера того, насколько вероятно изменение компонента в ответ на изменения в других компонентах системы. В этом проекте мы измеряем стабильность компонентов Global Student Portal, используя метрики из книги Роберта Мартина "Чистая архитектура".

Проект использует Neo4j - графовую базу данных, идеально подходящую для анализа зависимостей между компонентами.

## Метрики стабильности

Мы используем три ключевые метрики:

1. **Fan-in (Ca)** - количество входящих зависимостей. Это число компонентов, которые зависят от данного компонента.
2. **Fan-out (Ce)** - количество исходящих зависимостей. Это число компонентов, от которых зависит данный компонент.
3. **Нестабильность (I)** - рассчитывается как I = Ce / (Ca + Ce). Значение I колеблется от 0 до 1:
   - I = 0: максимально стабильный компонент (только входящие зависимости)
   - I = 1: максимально нестабильный компонент (только исходящие зависимости)

## Структура проекта

```
StudentPortalNeo4j/
├── README.md                  - Этот файл
├── docker-compose.yml         - Конфигурация для запуска Neo4j с помощью Docker
├── init-scripts/              - Скрипты для инициализации базы данных
│   └── init.cypher            - Cypher-запросы для создания графа зависимостей
├── queries/                   - Запросы для анализа стабильности
│   ├── component-dependencies.cypher  - Запрос для просмотра всех зависимостей
│   └── stability-metrics.cypher       - Запрос для расчета метрик стабильности
└── results/                   - Результаты анализа
    └── stability-metrics.md   - Таблица с метриками стабильности компонентов
```

## Запуск проекта

1. Убедитесь, что у вас установлен Docker и docker-compose
2. Клонируйте репозиторий
3. Запустите Neo4j с помощью docker-compose:

```bash
cd StudentPortalNeo4j
docker compose up -d
```

4. Откройте Neo4j Browser: http://localhost:7474
5. Войдите, используя следующие учетные данные:

   - Имя пользователя: `neo4j`
   - Пароль: `87017178180eE`

6. Импортируйте данные, выполнив запросы из файла `init-scripts/init.cypher`
7. Запустите анализ, выполнив запросы из директории `queries/`

> **Примечание**: Если вы хотите изменить пароль, отредактируйте переменную `NEO4J_AUTH` в файле `docker-compose.yml` перед запуском контейнера.

## Запросы для анализа

### Основной запрос для расчета метрик стабильности

```cypher
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
```

### Запрос для генерации таблицы в формате Markdown

```cypher
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
```

### Запрос для анализа стабильности по типам компонентов

```cypher
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
```

## Результаты анализа

Подробные результаты анализа представлены в файле [stability-metrics.md](results/stability-metrics.md).

### Ключевые выводы

1. **Наиболее стабильные компоненты** (I = 0):

   - DBServices (Data) - 15 компонентов зависят от него
   - Security (Common) - критически важный компонент безопасности
   - CachingServices (Data) - 3 компонента зависят от него
   - Redis, S3, ElasticSearch, DataWarehouse - компоненты хранения данных

2. **Наиболее нестабильные компоненты** (I = 1):

   - Клиентские приложения (WebApp, MobileApp, ThirdParty)
   - Специализированные API (CourseAPI, GradeAPI, FinanceAPI и др.)
   - Integration - интеграционный слой

3. **Анализ типов компонентов**:
   - Компоненты хранения данных (Analytics, Cache, Storage, Data) имеют самую низкую нестабильность
   - Компоненты клиентского уровня (Client) имеют максимальную нестабильность
   - Академические сервисы (Academic) имеют высокую нестабильность (0.794), что говорит о возможной необходимости дополнительных абстракций


- [Документация Neo4j](https://neo4j.com/docs/)
