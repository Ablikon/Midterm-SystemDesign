# Архитектурные диаграммы системы Golden Address

## Общая архитектура решения

```mermaid
graph TB
    subgraph "Источники данных"
        BS[Биллинговая система]
        SS[Система доставки]
        MS[Маркетинговая система]
        CS[Система поддержки]
    end

    subgraph "MDM Система Golden Address"
        DI[Модуль интеграции данных]
        DQ[Модуль качества данных]
        MM[Модуль сопоставления]
        GA[Хранилище золотых адресов]
        HM[Управление историей изменений]
        RL[Модуль управления правилами]
        API[API слой]
    end

    subgraph "Потребители данных"
        PT[Система почтовых отправлений]
        RP[Система формирования отчетов]
        DA[Аналитические системы]
        UI[Пользовательский интерфейс]
    end

    BS --> DI
    SS --> DI
    MS --> DI
    CS --> DI

    DI --> DQ
    DQ --> MM
    MM --> GA
    GA --> HM
    RL --> MM

    GA --> API
    API --> PT
    API --> RP
    API --> DA
    API --> UI

    UI --> DI
```

## Процесс определения "золотого" адреса

```mermaid
flowchart TD
    A[Сбор адресов из всех систем] --> B[Нормализация и стандартизация]
    B --> C[Сопоставление и объединение]
    C --> D[Проверка качества и валидация]
    D --> E[Определение рейтинга достоверности]
    E --> F[Выбор адреса с наивысшим рейтингом]
    F --> G[Публикация золотого адреса]
    G --> H[Синхронизация с системами-источниками]
    G --> I[Запись в историю изменений]
```

## Модели интеграции

### 1. Централизованная (Hub-and-Spoke)

```mermaid
graph TD
    GAS[Golden Address System] --> BS[Биллинговая система]
    GAS --> SS[Система доставки]
    GAS --> MS[Маркетинговая система]
    GAS --> CS[Система поддержки]
    BS --> GAS
    SS --> GAS
    MS --> GAS
    CS --> GAS
```

### 2. Реестровая (Registry)

```mermaid
graph TD
    BS[Биллинговая система] --> |Идентификация| GAS[Golden Address System]
    SS[Система доставки] --> |Идентификация| GAS
    MS[Маркетинговая система] --> |Идентификация| GAS
    CS[Система поддержки] --> |Идентификация| GAS
    GAS --> |Ссылка на золотой адрес| BS
    GAS --> |Ссылка на золотой адрес| SS
    GAS --> |Ссылка на золотой адрес| MS
    GAS --> |Ссылка на золотой адрес| CS
```

### 3. Гибридная модель

```mermaid
graph TD
    BS[Биллинговая система] <--> |Двусторонняя синхронизация| GAS[Golden Address System]
    SS[Система доставки] --> |Только чтение| GAS
    GAS --> |Обновления| SS
    MS[Маркетинговая система] <--> |Двусторонняя синхронизация| GAS
    CS[Система поддержки] --> |Только чтение| GAS
    GAS --> |Обновления| CS
```

## Алгоритм оценки достоверности адреса

```mermaid
graph TD
    A[Оценка достоверности адреса] --> B[Актуальность]
    A --> C[Полнота]
    A --> D[Источник]
    A --> E[Верификация]
    A --> F[Частота использования]
    A --> G[Консистентность]

    B --> B1[Дата последнего обновления]
    B --> B2[Частота обновлений]

    C --> C1[Наличие всех компонентов]
    C --> C2[Детализация]

    D --> D1[Приоритет системы-источника]
    D --> D2[Надежность источника]

    E --> E1[Подтверждение по почтовым базам]
    E --> E2[Успешное геокодирование]
    E --> E3[Подтверждение доставкой]

    F --> F1[Использование для доставки]
    F --> F2[Использование для коммуникаций]

    G --> G1[Совпадение в разных системах]
    G --> G2[Стабильность во времени]
```

## Процесс обновления "золотого" адреса

```mermaid
sequenceDiagram
    actor User
    participant Source as Система-источник
    participant GAS as Golden Address System
    participant Other as Другие системы

    User->>Source: Обновление адреса
    Source->>GAS: Уведомление об изменении
    GAS->>GAS: Пересчет рейтинга достоверности
    GAS->>GAS: Обновление золотого адреса
    GAS->>Other: Синхронизация изменений
    GAS->>Source: Подтверждение обновления
```

## Техническая архитектура компонентов

```mermaid
graph TB
    subgraph "Фронтенд"
        UI[Веб-интерфейс]
        Mobile[Мобильные приложения]
    end

    subgraph "API слой"
        Gateway[API Gateway]
        Auth[Авторизация и аутентификация]
    end

    subgraph "Микросервисы"
        AddressService[Сервис управления адресами]
        ValidationService[Сервис валидации]
        ScoringService[Сервис рейтингования]
        IntegrationService[Сервис интеграции]
        NotificationService[Сервис уведомлений]
        HistoryService[Сервис истории]
        ReportingService[Сервис отчетности]
    end

    subgraph "Сервисы данных"
        DB[(PostgreSQL + PostGIS)]
        ElasticSearch[(Elasticsearch)]
        Redis[(Redis)]
        Kafka[(Apache Kafka)]
    end

    subgraph "Внешние сервисы"
        PostalDB[Почтовые базы данных]
        GeocodingAPI[API геокодирования]
        ExternalValidation[Внешние сервисы валидации]
    end

    UI --> Gateway
    Mobile --> Gateway
    Gateway --> Auth

    Gateway --> AddressService
    Gateway --> ValidationService
    Gateway --> ReportingService

    AddressService --> DB
    AddressService --> ElasticSearch
    AddressService --> Redis

    ValidationService --> PostalDB
    ValidationService --> GeocodingAPI
    ValidationService --> ExternalValidation

    ScoringService --> DB
    ScoringService --> ElasticSearch

    IntegrationService --> Kafka

    AddressService --> ScoringService
    AddressService --> IntegrationService
    AddressService --> NotificationService
    AddressService --> HistoryService

    NotificationService --> Kafka
    HistoryService --> DB
    ReportingService --> DB
    ReportingService --> ElasticSearch
```

## Этапы внедрения и развертывания

```mermaid
gantt
    title План внедрения системы Golden Address
    dateFormat  YYYY-MM-DD

    section Подготовка и пилот
    Анализ существующих систем                :a1, 2023-01-01, 30d
    Разработка архитектуры                    :a2, after a1, 20d
    Настройка алгоритма                       :a3, after a2, 15d
    Пилотное внедрение                        :a4, after a3, 25d

    section Базовая реализация
    Разработка основных компонентов           :b1, after a4, 40d
    Интеграция с критическими системами       :b2, after b1, 30d
    Настройка процессов                       :b3, after b2, 20d
    Разработка UI                             :b4, after b1, 25d
    Внедрение API                             :b5, after b1, 15d

    section Полное внедрение
    Интеграция со всеми системами             :c1, after b3, 45d
    Расширенная функциональность              :c2, after b3, 30d
    Оптимизация производительности            :c3, after c1, 20d
    Мониторинг и отчетность                   :c4, after c2, 15d
    Обучение пользователей                    :c5, after c2, 25d

    section Оптимизация
    Сбор и анализ метрик                      :d1, after c5, 30d
    Оптимизация процессов                     :d2, after d1, 20d
    Расширение функциональности               :d3, after d2, 30d
```
