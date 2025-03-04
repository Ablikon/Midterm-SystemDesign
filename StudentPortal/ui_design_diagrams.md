# Диаграммы пользовательского интерфейса - Глобальный Студенческий Портал (GSP)

## Содержание

1. [Структура пользовательского интерфейса](#структура-пользовательского-интерфейса)
2. [Макеты основных экранов](#макеты-основных-экранов)
3. [Пользовательские потоки](#пользовательские-потоки)
4. [Адаптивный дизайн](#адаптивный-дизайн)
5. [Тематизация по университетам](#тематизация-по-университетам)

## Структура пользовательского интерфейса

### Общая структура портала

```mermaid
flowchart TD
    subgraph "GSP Portal"
        Landing["Лендинг/Вход в систему"]
        Dashboard["Дашборд"]

        subgraph "Студенческие разделы"
            Profile["Личный профиль"]
            Courses["Курсы"]
            Schedule["Расписание"]
            Grades["Оценки"]
            Finances["Финансы"]
            Library["Библиотека"]
            Communication["Коммуникации"]
            Documents["Документы"]
        end

        subgraph "Преподавательские разделы"
            FacultyProfile["Профиль преподавателя"]
            ClassManagement["Управление занятиями"]
            GradingTools["Инструменты оценивания"]
            AttendanceTool["Учёт посещаемости"]
            Messaging["Сообщения"]
        end

        subgraph "Административные разделы"
            AdminDashboard["Панель администрирования"]
            UserManagement["Управление пользователями"]
            CourseManagement["Управление курсами"]
            ReportingTools["Инструменты отчётности"]
            SystemSettings["Настройки системы"]
        end

        Landing --> Dashboard
        Dashboard --> Profile
        Dashboard --> Courses
        Dashboard --> Schedule
        Dashboard --> Grades
        Dashboard --> Finances
        Dashboard --> Library
        Dashboard --> Communication
        Dashboard --> Documents

        Dashboard --> FacultyProfile
        Dashboard --> ClassManagement
        Dashboard --> GradingTools
        Dashboard --> AttendanceTool
        Dashboard --> Messaging

        Dashboard --> AdminDashboard
        AdminDashboard --> UserManagement
        AdminDashboard --> CourseManagement
        AdminDashboard --> ReportingTools
        AdminDashboard --> SystemSettings
    end
```

### Компоненты основного интерфейса

```mermaid
flowchart TD
    subgraph "Компоненты UI"
        Header["Шапка с лого университета\n+ Поиск + Уведомления + Профиль"]
        Sidebar["Боковое меню\n(Навигация по разделам)"]
        MainContent["Основное содержимое"]
        Footer["Подвал\n(Контактная информация, ссылки)"]

        Modals["Модальные окна\n(Подтверждения, формы)"]
        Toast["Уведомления\n(Toast messages)"]
        Drawer["Выдвижные панели\n(Доп. информация)"]
    end

    subgraph "Общие компоненты"
        Tables["Таблицы данных"]
        Forms["Формы"]
        Cards["Карточки"]
        Tabs["Вкладки"]
        Buttons["Кнопки и действия"]
        Filters["Фильтры и сортировка"]
        Charts["Графики и диаграммы"]
        Calendar["Календарь"]
        FileUpload["Загрузка файлов"]
        RichText["Редактор текста"]
    end

    Header --- MainContent
    Sidebar --- MainContent
    MainContent --- Footer
    MainContent -.-> Modals
    MainContent -.-> Toast
    MainContent -.-> Drawer

    MainContent --> Tables
    MainContent --> Forms
    MainContent --> Cards
    MainContent --> Tabs
    MainContent --> Buttons
    MainContent --> Filters
    MainContent --> Charts
    MainContent --> Calendar
    MainContent --> FileUpload
    MainContent --> RichText
```

## Макеты основных экранов

### Страница входа в систему

```mermaid
graph TD
    subgraph "Страница входа"
        LoginContainer["Контейнер входа"]

        subgraph "Шапка страницы"
            Logo["Логотип GSP"]
            TenantSelect["Выбор учреждения"]
            LangSelect["Выбор языка"]
        end

        subgraph "Форма входа"
            LoginHeader["Заголовок формы + Логотип учреждения"]
            UsernameField["Поле имени пользователя"]
            PasswordField["Поле пароля"]
            RememberMe["Запомнить меня"]
            LoginButton["Кнопка входа"]
            ForgotPassword["Забыли пароль?"]
            SSOOptions["Варианты единого входа (SSO)"]
        end

        subgraph "Подвал страницы"
            HelpLink["Помощь"]
            PrivacyLink["Конфиденциальность"]
            TermsLink["Условия использования"]
            Copyright["Авторские права"]
        end
    end

    Logo --- TenantSelect
    TenantSelect --- LangSelect

    LoginHeader --- UsernameField
    UsernameField --- PasswordField
    PasswordField --- RememberMe
    RememberMe --- LoginButton
    LoginButton --- ForgotPassword
    ForgotPassword --- SSOOptions

    SSOOptions --- HelpLink
    HelpLink --- PrivacyLink
    PrivacyLink --- TermsLink
    TermsLink --- Copyright
```

### Дашборд студента

```mermaid
graph TD
    subgraph "Дашборд студента"
        HeaderBar["Шапка с навигацией"]

        subgraph "Боковое меню"
            MenuProfile["Профиль"]
            MenuCourses["Курсы"]
            MenuSchedule["Расписание"]
            MenuGrades["Оценки"]
            MenuLibrary["Библиотека"]
            MenuFinances["Финансы"]
            MenuCommunication["Коммуникации"]
            MenuDocuments["Документы"]
            MenuSettings["Настройки"]
        end

        subgraph "Основное содержимое"
            WelcomeCard["Приветственная карточка"]

            subgraph "Верхний ряд виджетов"
                UpcomingEvents["Предстоящие события"]
                Notifications["Уведомления"]
                QuickActions["Быстрые действия"]
            end

            subgraph "Средний ряд виджетов"
                CurrentCourses["Текущие курсы"]
                Assignments["Задания"]
                GradeOverview["Обзор оценок"]
            end

            subgraph "Нижний ряд виджетов"
                FinancialSummary["Финансовая сводка"]
                AnnouncementsWidget["Объявления"]
                UsefulLinks["Полезные ссылки"]
            end
        end

        FooterBar["Подвал страницы"]
    end

    HeaderBar --- MenuProfile
    MenuProfile --- MenuCourses
    MenuCourses --- MenuSchedule
    MenuSchedule --- MenuGrades
    MenuGrades --- MenuLibrary
    MenuLibrary --- MenuFinances
    MenuFinances --- MenuCommunication
    MenuCommunication --- MenuDocuments
    MenuDocuments --- MenuSettings

    HeaderBar --- WelcomeCard
    WelcomeCard --- UpcomingEvents
    UpcomingEvents --- Notifications
    Notifications --- QuickActions

    QuickActions --- CurrentCourses
    CurrentCourses --- Assignments
    Assignments --- GradeOverview

    GradeOverview --- FinancialSummary
    FinancialSummary --- AnnouncementsWidget
    AnnouncementsWidget --- UsefulLinks

    UsefulLinks --- FooterBar
```

### Страница курса

```mermaid
graph TD
    subgraph "Страница курса"
        CourseHeader["Заголовок курса + Код + Преподаватель"]

        subgraph "Навигация по курсу"
            TabOverview["Обзор"]
            TabSyllabus["Программа"]
            TabMaterials["Материалы"]
            TabAssignments["Задания"]
            TabDiscussions["Обсуждения"]
            TabGrades["Оценки"]
            TabAttendance["Посещаемость"]
        end

        subgraph "Обзор курса"
            CourseInfo["Информация о курсе"]
            InstructorInfo["Информация о преподавателе"]
            UpcomingDeadlines["Предстоящие сроки"]
            RecentAnnouncements["Последние объявления"]
            ProgressBar["Прогресс по курсу"]
        end

        subgraph "Секция материалов"
            WeeklyModules["Модули по неделям"]

            subgraph "Модуль недели"
                ModuleTitle["Заголовок модуля"]
                LectureNotes["Конспекты лекций"]
                ReadingMaterials["Материалы для чтения"]
                PracticalMaterials["Практические материалы"]
                ModuleAssignments["Задания модуля"]
            end
        end
    end

    CourseHeader --- TabOverview
    TabOverview --- TabSyllabus
    TabSyllabus --- TabMaterials
    TabMaterials --- TabAssignments
    TabAssignments --- TabDiscussions
    TabDiscussions --- TabGrades
    TabGrades --- TabAttendance

    TabOverview --- CourseInfo
    CourseInfo --- InstructorInfo
    InstructorInfo --- UpcomingDeadlines
    UpcomingDeadlines --- RecentAnnouncements
    RecentAnnouncements --- ProgressBar

    TabMaterials --- WeeklyModules
    WeeklyModules --- ModuleTitle
    ModuleTitle --- LectureNotes
    LectureNotes --- ReadingMaterials
    ReadingMaterials --- PracticalMaterials
    PracticalMaterials --- ModuleAssignments
```

## Пользовательские потоки

### Регистрация на курс

```mermaid
flowchart LR
    Start([Начало]) --> Dashboard[Дашборд]
    Dashboard --> CourseRegistration[Раздел регистрации на курсы]
    CourseRegistration --> BrowseCourses[Просмотр доступных курсов]
    BrowseCourses --> SelectCourse[Выбор курса]
    SelectCourse --> CourseDetails[Просмотр деталей курса]
    CourseDetails --> CheckPrerequisites{Проверка\nпререквизитов}

    CheckPrerequisites -- Не выполнены --> PrerequisitesInfo[Информация о неудовлетворенных пререквизитах]
    PrerequisitesInfo --> BrowseCourses

    CheckPrerequisites -- Выполнены --> CheckScheduleConflict{Проверка\nконфликтов\nрасписания}

    CheckScheduleConflict -- Есть конфликты --> ConflictInfo[Информация о конфликтах]
    ConflictInfo --> BrowseCourses

    CheckScheduleConflict -- Нет конфликтов --> ConfirmRegistration[Подтверждение регистрации]
    ConfirmRegistration --> ProcessRegistration[Обработка регистрации]
    ProcessRegistration --> RegistrationComplete[Регистрация завершена]
    RegistrationComplete --> ViewMyCourses[Просмотр моих курсов]
    ViewMyCourses --> End([Конец])
```

### Подача и оценка задания

```mermaid
sequenceDiagram
    actor Student as Студент
    actor Instructor as Преподаватель
    participant CourseUI as Страница курса
    participant AssignmentUI as Страница задания
    participant SubmissionUI as Форма отправки
    participant GradingUI as Интерфейс оценивания

    Student->>CourseUI: Открывает страницу курса
    CourseUI->>Student: Отображает список заданий
    Student->>AssignmentUI: Открывает страницу задания
    AssignmentUI->>Student: Отображает детали задания и форму загрузки
    Student->>SubmissionUI: Загружает файл(ы) и пишет комментарии
    SubmissionUI->>Student: Подтверждает отправку

    Instructor->>CourseUI: Открывает страницу курса
    CourseUI->>Instructor: Отображает список заданий
    Instructor->>AssignmentUI: Открывает страницу задания
    AssignmentUI->>Instructor: Отображает список отправленных работ
    Instructor->>GradingUI: Открывает работу студента
    GradingUI->>Instructor: Отображает работу, форму для оценки и комментариев
    Instructor->>GradingUI: Оценивает работу и оставляет отзыв
    GradingUI->>Instructor: Подтверждает сохранение оценки

    Student->>CourseUI: Открывает страницу курса
    CourseUI->>Student: Отображает уведомление о новой оценке
    Student->>AssignmentUI: Открывает страницу задания
    AssignmentUI->>Student: Отображает полученную оценку и отзыв
```

## Адаптивный дизайн

### Структура адаптивного интерфейса

```mermaid
graph TD
    subgraph "Адаптивная структура интерфейса"
        subgraph "Десктоп (>1200px)"
            DesktopLayout["Полная боковая панель\n+ Широкое основное содержимое\n+ Дополнительные колонки"]
            DesktopComponents["Расширенные таблицы\n+ Многоколоночные формы\n+ Полные графики"]
        end

        subgraph "Планшет (768-1199px)"
            TabletLayout["Сворачиваемая боковая панель\n+ Подстраиваемое основное содержимое\n+ Скрытые дополнительные колонки"]
            TabletComponents["Упрощенные таблицы\n+ Одноколоночные формы\n+ Адаптированные графики"]
        end

        subgraph "Мобильный (<767px)"
            MobileLayout["Бургер-меню\n+ Полноширинное основное содержимое\n+ Вертикальное расположение"]
            MobileComponents["Карточки вместо таблиц\n+ Компактные формы\n+ Упрощенные графики\n+ Touch-оптимизированные элементы"]
        end
    end

    DesktopLayout --- DesktopComponents
    TabletLayout --- TabletComponents
    MobileLayout --- MobileComponents
```

### Пример адаптивной страницы курса

```mermaid
graph TD
    subgraph "Адаптивный дизайн страницы курса"
        subgraph "Десктоп"
            DeskNavigation["Основная навигация (сбоку)"]
            DeskCourseNav["Курсовая навигация (верх)"]
            DeskMainContent["Основное содержимое\n(широкая колонка)"]
            DeskSideContent["Боковой контент\n(узкая колонка)"]
        end

        subgraph "Планшет"
            TabNavigation["Сворачиваемая навигация"]
            TabCourseNav["Курсовая навигация (верх)"]
            TabMainContent["Основное содержимое\n(полная ширина)"]
            TabSideContent["Боковой контент\n(под основным)"]
        end

        subgraph "Мобильный"
            MobNavigation["Бургер-меню"]
            MobCourseNav["Выпадающий список вкладок"]
            MobMainContent["Основное содержимое\n(полная ширина)"]
            MobSideContent["Боковой контент\n(вкладка или аккордеон)"]
        end
    end

    DeskNavigation --- DeskCourseNav
    DeskCourseNav --- DeskMainContent
    DeskMainContent --- DeskSideContent

    TabNavigation --- TabCourseNav
    TabCourseNav --- TabMainContent
    TabMainContent --- TabSideContent

    MobNavigation --- MobCourseNav
    MobCourseNav --- MobMainContent
    MobMainContent --- MobSideContent
```

## Тематизация по университетам

### Система тематизации

```mermaid
graph TD
    subgraph "Система тематизации"
        ThemeBase["Базовая тема\n(общие компоненты и структура)"]

        subgraph "Кастомизируемые элементы"
            Colors["Цветовая схема\n(Primary, Secondary, Accent)"]
            Typography["Типографика\n(Шрифты, размеры, стили)"]
            Logos["Логотипы и брендинг"]
            Components["Стили компонентов\n(кнопки, карточки и т.д.)"]
            Layouts["Варианты компоновки"]
        end

        subgraph "Университетские темы"
            Uni1Theme["Тема Университета 1"]
            Uni2Theme["Тема Университета 2"]
            Uni3Theme["Тема Университета 3"]
        end
    end

    ThemeBase --> Colors
    ThemeBase --> Typography
    ThemeBase --> Logos
    ThemeBase --> Components
    ThemeBase --> Layouts

    Colors --> Uni1Theme
    Typography --> Uni1Theme
    Logos --> Uni1Theme
    Components --> Uni1Theme
    Layouts --> Uni1Theme

    Colors --> Uni2Theme
    Typography --> Uni2Theme
    Logos --> Uni2Theme
    Components --> Uni2Theme
    Layouts --> Uni2Theme

    Colors --> Uni3Theme
    Typography --> Uni3Theme
    Logos --> Uni3Theme
    Components --> Uni3Theme
    Layouts --> Uni3Theme
```

### Пример тематизации по университетам

```mermaid
graph TD
    subgraph "Визуальные примеры"
        subgraph "Университет 1 (Синяя тема)"
            Uni1Logo["Логотип"]
            Uni1Header["Синяя шапка + Белый текст"]
            Uni1Buttons["Синие кнопки, белые иконки"]
            Uni1Cards["Белые карточки с синими заголовками"]
        end

        subgraph "Университет 2 (Зеленая тема)"
            Uni2Logo["Логотип"]
            Uni2Header["Зеленая шапка + Белый текст"]
            Uni2Buttons["Зеленые кнопки, белые иконки"]
            Uni2Cards["Белые карточки с зелеными заголовками"]
        end

        subgraph "Университет 3 (Бордовая тема)"
            Uni3Logo["Логотип"]
            Uni3Header["Бордовая шапка + Белый текст"]
            Uni3Buttons["Бордовые кнопки, белые иконки"]
            Uni3Cards["Белые карточки с бордовыми заголовками"]
        end
    end

    Uni1Logo --- Uni1Header
    Uni1Header --- Uni1Buttons
    Uni1Buttons --- Uni1Cards

    Uni2Logo --- Uni2Header
    Uni2Header --- Uni2Buttons
    Uni2Buttons --- Uni2Cards

    Uni3Logo --- Uni3Header
    Uni3Header --- Uni3Buttons
    Uni3Buttons --- Uni3Cards
```
