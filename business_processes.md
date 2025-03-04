# Бизнес-процессы - Глобальный Студенческий Портал (GSP)

## Содержание

1. [Основные бизнес-потоки](#основные-бизнес-потоки)
2. [Академический жизненный цикл](#академический-жизненный-цикл)
3. [Финансовые процессы](#финансовые-процессы)
4. [Административные процессы](#административные-процессы)
5. [Международное взаимодействие](#международное-взаимодействие)

## Основные бизнес-потоки

### Жизненный цикл студента

```mermaid
stateDiagram-v2
    [*] --> Поступление
    Поступление --> Зачисление: Заявка одобрена
    Поступление --> [*]: Заявка отклонена

    Зачисление --> Обучение: Регистрация на курсы

    state Обучение {
        [*] --> Семестр
        Семестр --> Оценивание
        Оценивание --> Семестр: Следующий семестр
        Оценивание --> [*]: Программа завершена
    }

    Обучение --> Выпуск: Выполнены все требования
    Обучение --> Отчисление: Академическая неуспеваемость/Другие причины

    Выпуск --> Выпускник
    Выпускник --> [*]

    Отчисление --> [*]
```

### Процесс регистрации на курсы

```mermaid
flowchart TD
    Start([Начало периода регистрации]) --> PriorityAssignment[Назначение приоритетных окон регистрации]
    PriorityAssignment --> PreReqCheck[Проверка предварительных требований]

    PreReqCheck --> RegistrationOpen[Открытие периода регистрации]
    RegistrationOpen --> StudentAccess[Доступ студента в системе]

    StudentAccess --> CourseSearch[Поиск курсов]
    CourseSearch --> CourseSelection[Выбор курсов]
    CourseSelection --> ScheduleValidation[Проверка конфликтов расписания]

    ScheduleValidation --> SeatsCheck{Есть свободные места?}
    SeatsCheck -->|Да| EnrollmentConfirmation[Подтверждение регистрации]
    SeatsCheck -->|Нет| WaitlistOption{Поставить в лист ожидания?}

    WaitlistOption -->|Да| AddToWaitlist[Добавление в лист ожидания]
    WaitlistOption -->|Нет| CourseSelection

    AddToWaitlist --> WaitlistNotification[Уведомление при освобождении места]
    WaitlistNotification --> SeatsCheck

    EnrollmentConfirmation --> FinancialCheck[Проверка финансовых обязательств]
    FinancialCheck --> PaymentRequired{Требуется оплата?}

    PaymentRequired -->|Да| PaymentProcess[Процесс оплаты]
    PaymentRequired -->|Нет| RegistrationComplete[Завершение регистрации]

    PaymentProcess --> PaymentSuccessful{Оплата успешна?}
    PaymentSuccessful -->|Да| RegistrationComplete
    PaymentSuccessful -->|Нет| PaymentError[Ошибка оплаты]

    PaymentError --> PaymentOptions[Предложение других способов оплаты]
    PaymentOptions --> PaymentProcess

    RegistrationComplete --> Notification[Отправка подтверждения]
    Notification --> End([Конец процесса регистрации])
```

## Академический жизненный цикл

### Процесс обучения и оценивания

```mermaid
flowchart TD
    CourseCreation[Создание курса] --> CurriculumDevelopment[Разработка учебной программы]
    CurriculumDevelopment --> CourseApproval[Утверждение курса]
    CourseApproval --> CourseScheduling[Планирование расписания]

    CourseScheduling --> CourseRegistration[Открытие регистрации на курс]
    CourseRegistration --> CourseDelivery[Проведение занятий]

    subgraph "Учебный процесс"
        CourseDelivery --> ContentAccess[Доступ к материалам]
        ContentAccess --> Assignments[Задания и проекты]
        Assignments --> Discussions[Обсуждения и взаимодействие]
        Discussions --> Assessments[Промежуточные оценивания]
        Assessments --> FinalExams[Итоговые экзамены]
    end

    FinalExams --> GradeSubmission[Выставление оценок]
    GradeSubmission --> GradeApproval[Утверждение оценок]
    GradeApproval --> GradePublishing[Публикация оценок]

    GradePublishing --> CourseCompletion[Завершение курса]
    CourseCompletion --> FeedbackCollection[Сбор обратной связи]
    FeedbackCollection --> CourseImprovement[Улучшение курса]
    CourseImprovement --> CourseCreation
```

### Процесс дипломной работы

```mermaid
sequenceDiagram
    actor Student as Студент
    participant Advisor as Научный руководитель
    participant Committee as Комитет
    participant System as GSP Система

    Student->>System: Выбор темы дипломной работы
    Student->>System: Запрос на назначение руководителя
    System->>Advisor: Уведомление о запросе
    Advisor->>System: Принятие/отклонение запроса

    alt Запрос принят
        System->>Student: Уведомление о принятии
        Student->>Advisor: Разработка плана исследования
        Advisor->>Student: Обратная связь по плану

        loop Процесс исследования
            Student->>System: Загрузка прогресса/глав
            System->>Advisor: Уведомление о новых материалах
            Advisor->>System: Загрузка комментариев/предложений
            System->>Student: Уведомление о комментариях
        end

        Student->>System: Отправка итогового варианта работы
        System->>Advisor: Уведомление о завершении работы
        Advisor->>System: Одобрение для защиты

        System->>Committee: Рассылка работы членам комитета
        Committee->>System: Предварительные отзывы
        System->>Student: Отзывы для подготовки к защите

        Student->>System: Планирование защиты
        System->>Committee: Организация заседания комитета

        Student->>Committee: Презентация и защита работы
        Committee->>System: Оценка и результаты защиты
        System->>Student: Итоговая оценка и комментарии
    else Запрос отклонен
        System->>Student: Уведомление об отклонении
        System->>Student: Предложение альтернативных руководителей
    end
```

## Финансовые процессы

### Процесс оплаты обучения

```mermaid
flowchart TD
    TuitionCalculation[Расчет стоимости обучения] --> FeeApplication[Применение дополнительных сборов]
    FeeApplication --> ScholarshipApplication[Применение стипендий/грантов]
    ScholarshipApplication --> FinancialAidApplication[Применение финансовой помощи]

    FinancialAidApplication --> InvoiceGeneration[Формирование счета]
    InvoiceGeneration --> InvoiceNotification[Уведомление студента о счете]

    InvoiceNotification --> PaymentOptions[Выбор способа оплаты]

    PaymentOptions --> InstallmentPlan[План рассрочки]
    PaymentOptions --> FullPayment[Полная оплата]
    PaymentOptions --> ThirdPartyPayment[Оплата третьей стороной]

    InstallmentPlan --> InstallmentAgreement[Соглашение о рассрочке]
    InstallmentAgreement --> FirstInstallment[Первый платеж]

    FullPayment --> PaymentMethod[Выбор метода оплаты]
    ThirdPartyPayment --> SponsorInvoice[Выставление счета спонсору]

    FirstInstallment --> PaymentProcessing[Обработка платежа]
    PaymentMethod --> PaymentProcessing
    SponsorInvoice --> SponsorPayment[Платеж от спонсора]
    SponsorPayment --> PaymentProcessing

    PaymentProcessing --> PaymentVerification[Проверка платежа]
    PaymentVerification --> ReceiptGeneration[Формирование квитанции]
    ReceiptGeneration --> AccountUpdate[Обновление финансового счета]

    AccountUpdate --> RegistrationHold{Есть задолженность?}
    RegistrationHold -->|Да| PlaceHold[Наложение финансового ограничения]
    RegistrationHold -->|Нет| ClearHold[Снятие ограничений]

    PlaceHold --> NotifyStudent[Уведомление о задолженности]
    ClearHold --> AllowRegistration[Разрешение регистрации]

    NotifyStudent --> Reminder[Напоминания о платеже]
    AllowRegistration --> CompletedProcess[Завершение финансового процесса]
```

### Процесс выделения финансовой помощи

```mermaid
sequenceDiagram
    actor Student as Студент
    participant FinAid as Отдел финансовой помощи
    participant System as GSP Система
    participant External as Внешние источники

    Student->>System: Заявка на финансовую помощь
    System->>FinAid: Передача заявки на рассмотрение

    FinAid->>External: Проверка внешних источников финансирования
    External->>FinAid: Результаты проверки

    FinAid->>System: Определение потребности в помощи

    alt Соответствие критериям
        FinAid->>System: Расчет суммы помощи
        System->>Student: Предложение финансовой помощи

        Student->>System: Принятие/отклонение предложения

        alt Предложение принято
            System->>FinAid: Подтверждение принятия
            FinAid->>System: Выделение средств
            System->>Student: Уведомление о выделении
        else Предложение отклонено
            System->>FinAid: Уведомление об отклонении
            FinAid->>System: Закрытие заявки
        end
    else Не соответствует критериям
        FinAid->>System: Отклонение заявки
        System->>Student: Уведомление об отклонении
        System->>Student: Альтернативные варианты финансирования
    end

    FinAid->>System: Периодическая проверка соответствия

    loop Каждый семестр
        System->>Student: Запрос обновления финансовой информации
        Student->>System: Предоставление обновленной информации
        System->>FinAid: Повторная оценка потребности
        FinAid->>System: Корректировка суммы помощи
        System->>Student: Уведомление об изменениях
    end
```

## Административные процессы

### Процесс аккредитации программы

```mermaid
flowchart TD
    InitiateAccreditation[Инициация процесса аккредитации] --> ProgramEvaluation[Оценка программы]
    ProgramEvaluation --> SelfStudyPreparation[Подготовка самообследования]

    SelfStudyPreparation --> DocumentCollection[Сбор документации]
    DocumentCollection --> OutcomeAssessment[Оценка результатов обучения]
    OutcomeAssessment --> SurveyCollection[Сбор опросов и отзывов]

    SurveyCollection --> SelfStudySubmission[Отправка материалов самообследования]
    SelfStudySubmission --> AccreditationVisit[Визит аккредитационной комиссии]

    AccreditationVisit --> FeedbackReceived[Получение отзывов комиссии]
    FeedbackReceived --> ResponseToFeedback[Ответ на отзывы]

    ResponseToFeedback --> AccreditationDecision{Решение по аккредитации}
    AccreditationDecision -->|Одобрено| AccreditationGranted[Аккредитация получена]
    AccreditationDecision -->|Условно| ConditionsSet[Установление условий]
    AccreditationDecision -->|Отклонено| AccreditationDenied[Отказ в аккредитации]

    ConditionsSet --> ImprovementPlan[План улучшения]
    ImprovementPlan --> ImplementChanges[Внедрение изменений]
    ImplementChanges --> FollowUpReport[Последующий отчет]
    FollowUpReport --> AccreditationDecision

    AccreditationGranted --> AnnualReporting[Ежегодная отчетность]
    AnnualReporting --> MidCycleReview[Промежуточный обзор]
    MidCycleReview --> ReaccreditationPreparation[Подготовка к реаккредитации]
    ReaccreditationPreparation --> InitiateAccreditation

    AccreditationDenied --> AppealProcess[Процесс апелляции]
    AppealProcess --> AppealDecision{Решение по апелляции}
    AppealDecision -->|Удовлетворена| AccreditationDecision
    AppealDecision -->|Отклонена| MajorRestructuring[Существенная реструктуризация]
    MajorRestructuring --> InitiateAccreditation
```

### Процесс найма и аттестации преподавателей

```mermaid
sequenceDiagram
    participant HR as Отдел кадров
    participant Dept as Департамент
    participant Committee as Комитет по найму
    participant Candidate as Кандидат
    participant System as GSP Система

    Dept->>HR: Запрос на открытие вакансии
    HR->>System: Создание вакансии
    System->>System: Публикация вакансии

    Candidate->>System: Подача заявления
    System->>HR: Первичная проверка заявлений
    HR->>Dept: Передача подходящих кандидатов

    Dept->>Committee: Формирование комитета по найму
    Committee->>System: Доступ к заявлениям кандидатов
    Committee->>System: Оценка кандидатов

    Committee->>Candidate: Приглашение на интервью
    Candidate->>Committee: Участие в интервью
    Committee->>Candidate: Приглашение на пробную лекцию

    Candidate->>Committee: Проведение пробной лекции
    Committee->>Committee: Оценка лекции и кандидата
    Committee->>Dept: Рекомендации по кандидатам

    Dept->>HR: Решение о выборе кандидата
    HR->>Candidate: Предложение о работе

    alt Предложение принято
        Candidate->>HR: Принятие предложения
        HR->>System: Создание профиля преподавателя
        System->>Dept: Уведомление о новом сотруднике
        HR->>Candidate: Ориентационная программа

        loop Каждый академический год
            System->>Dept: Инициация процесса аттестации
            Dept->>System: Сбор данных о преподавателе
            System->>System: Агрегация оценок студентов
            System->>Dept: Анализ научных публикаций
            Dept->>System: Оценка производительности
            System->>HR: Результаты аттестации
            HR->>Candidate: Обратная связь и решение
        end
    else Предложение отклонено
        Candidate->>HR: Отклонение предложения
        HR->>Dept: Уведомление об отказе
        Dept->>Committee: Рассмотрение других кандидатов
    end
```

## Международное взаимодействие

### Процесс обмена студентами

```mermaid
flowchart TD
    EstablishPartnership[Установление партнерства между вузами] --> AgreeTerms[Согласование условий обмена]
    AgreeTerms --> PublishProgram[Публикация программы обмена]

    PublishProgram --> StudentApplication[Подача заявок студентами]
    StudentApplication --> HomeApproval[Одобрение домашним вузом]
    HomeApproval --> HostReview[Рассмотрение принимающим вузом]

    HostReview --> SelectionDecision{Решение о выборе}
    SelectionDecision -->|Принят| AcceptanceNotification[Уведомление о принятии]
    SelectionDecision -->|Отклонен| RejectionNotification[Уведомление об отказе]

    AcceptanceNotification --> VisaDocuments[Оформление визовых документов]
    AcceptanceNotification --> PreDepartureOrientation[Предотъездная ориентация]

    VisaDocuments --> TravelArrangements[Организация поездки]
    PreDepartureOrientation --> TravelArrangements

    TravelArrangements --> ArrivalRegistration[Регистрация по прибытии]
    ArrivalRegistration --> HostOrientation[Ориентация в принимающем вузе]

    HostOrientation --> CourseEnrollment[Запись на курсы]
    CourseEnrollment --> ExchangePeriod[Период обмена]

    ExchangePeriod --> CourseCompletion[Завершение курсов]
    CourseCompletion --> GradesTransfer[Перенос оценок]

    GradesTransfer --> ReturnHome[Возвращение домой]
    ReturnHome --> CreditRecognition[Признание кредитов домашним вузом]

    CreditRecognition --> FeedbackCollection[Сбор обратной связи]
    FeedbackCollection --> ProgramImprovement[Улучшение программы обмена]
    ProgramImprovement --> PublishProgram
```

### Процесс международной образовательной программы

```mermaid
sequenceDiagram
    participant HomeUni as Домашний университет
    participant PartnerUni as Университет-партнер
    participant System as GSP Система
    participant Students as Студенты

    HomeUni->>PartnerUni: Инициация совместной программы
    PartnerUni->>HomeUni: Обсуждение условий

    HomeUni->>System: Создание профиля программы
    PartnerUni->>System: Интеграция учебных планов

    HomeUni->>System: Добавление требований к программе
    PartnerUni->>System: Добавление местных требований

    System->>System: Согласование и интеграция учебных планов

    HomeUni->>Students: Анонс программы
    PartnerUni->>Students: Анонс программы

    Students->>System: Подача заявок
    System->>HomeUni: Заявки для рассмотрения
    System->>PartnerUni: Заявки для рассмотрения

    HomeUni->>System: Решения по заявкам
    PartnerUni->>System: Решения по заявкам
    System->>Students: Уведомления о решениях

    alt Студент принят
        Students->>System: Принятие предложения
        System->>HomeUni: Подтверждение зачисления
        System->>PartnerUni: Подтверждение зачисления

        par Обучение в домашнем вузе
            Students->>HomeUni: Обучение по программе
            HomeUni->>System: Загрузка оценок и кредитов
        and Обучение в вузе-партнере
            Students->>PartnerUni: Обучение по программе
            PartnerUni->>System: Загрузка оценок и кредитов
        end

        System->>System: Интеграция академических записей
        System->>Students: Общая академическая справка

        alt Выполнены требования обоих вузов
            System->>HomeUni: Проверка требований для диплома
            System->>PartnerUni: Проверка требований для диплома

            HomeUni->>System: Подтверждение выполнения требований
            PartnerUni->>System: Подтверждение выполнения требований

            System->>Students: Уведомление о соответствии для двойного диплома
            HomeUni->>Students: Выдача диплома
            PartnerUni->>Students: Выдача диплома
        else Выполнены требования только одного вуза
            System->>Students: Уведомление о соответствии для одного диплома
            alt Домашний вуз
                HomeUni->>Students: Выдача диплома
            else Вуз-партнер
                PartnerUni->>Students: Выдача диплома
            end
        end
    else Студент отклонен
        Students->>System: Поиск альтернативных программ
        System->>Students: Предложение других вариантов
    end
```
