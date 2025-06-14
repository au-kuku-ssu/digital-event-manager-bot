# Цифровой Управляющий Мероприятиями (ЦУМ) - техническое задание

## Описания проектов

Общие требования:
- Платформы: Telegram.
- Интуитивно понятный интерфейс для пользователей.
- Возможность обработки и хранения данных участников.
- Отправка уведомлений и отчетов по электронной почте.

#### 1. Регистрация участника:
Проект по автоматизации процесса регистрации участников мероприятия. Система позволяет новым пользователям создавать учетные записи, вводя необходимые данные, такие как ФИО, контактная информация и тип участия. Регистрация включает в себя подтверждение учетной записи через электронную почту. Участники могут редактировать свои данные и просматривать свою регистрацию в личном кабинете. Этот проект обеспечивает удобный интерфейс для организаторов для мониторинга и управления зарегистрированными участниками.

#### 2. Жеребьевка:
Проект, направленный на автоматизацию процесса жеребьевки тем для секций мероприятий. Система позволяет организатору загружать заранее определенные темы и автоматически распределять их среди зарегистрированных групп участников на основе случайного выбора. После жеребьевки каждая группа получает уведомление на электронную почту с назначенной темой и техническими требованиями. Проект обеспечивает справедливость и прозрачность в распределении тем, что повышает доверие участников к организаторам.

#### 3. Оценка докладов:
Проект по созданию закрытого режима оценки выступлений участников. Члены жюри имеют возможность выставлять оценки по пяти критериям (организация, содержание, визуализация, механика, доставка) с использованием шкалы от 0 до 4 баллов. Система автоматически рассчитывает итоговый балл и позволяет оставлять комментарии по каждому выступлению. Результаты и места участников отображаются в итоговой таблице, которая сортируется по баллам и алфавиту. Проект обеспечивает структурированный и объективный подход к оценке, а также автоматическую генерацию отчетов для организаторов.

#### 4. Генерация программы мероприятия:
Проект, который автоматизирует процесс создания программы мероприятия на основе введенных данных о секциях, выступлениях и участниках. Система собирает информацию из различных источников, формирует структуру программы, в том числе расписание и связанные материалы, и создает итоговый документ в форматах PDF и DOC. Организаторы получают возможность редактирования и настройки программы перед её публикацией. Это обеспечивает организованный подход к управлению мероприятием и удобство для участников в планировании своего времени.
- Бот должен быть надежно протестирован на предмет ошибок и некорректной работы.
- Обеспечение конфиденциальности данных участников (соблюдение норм GDPR).
- Реализовать возможность хранения и обработки данных в базе данных.
Дополнительные пожелания:
- Простой и понятный интерфейс для пользователей, включая визуальное оформление и подсказки.
- Возможность обновления списка мероприятий и преподавателей без внесения изменений в код бота.
- Поддержка многоязычного интерфейса (русский и английский).

### Требования к размещению решения и документации

#### 1. Размещение решения:
- Репозиторий: Разработанное программное решение должно быть размещено на платформе GitLab в закрытом приватном репозитории. Это обеспечит защиту кода и доступ к нему только у авторизованных пользователей.
- Доступ: Доступ к репозиторию должен быть предоставлен всем участникам проекта и ответственным лицам (например, организаторам и членам жюри), которые должны иметь соответствующие права для выполнения необходимых задач.

#### 2. Оформление документации кода:
- Документация: Каждая часть кода должна быть подробно задокументирована. Документация должна включать:
  - Описание функций, классов и методов.
  - Параметры и возвращаемые значения.
  - Примеры использования и область применения каждой функции.
  - Описание структуры и назначения каждого файла.

- README файл: В корне репозитория должен быть размещен файл README.md, содержащее:
  - Краткое описание проекта.
  - Инструкции по установке и настройке окружения.
  - Инструкции по запуску приложения и тестированию.
  - Ссылки на дополнительную документацию и ресурсы.

#### 3. Составление задач:
- Система управления задачами: Необходимо использовать встроенные инструменты GitLab для составления задач и эпиков, связанных с проектом. Каждая задача должна содержать:
  - Название задачи.
  - Описание задачи, включая поставленные цели и требования.
  - Оценку времени выполнения.
  - Статус выполнения (новая, в работе, завершена).

- Назначение ответственных: Каждой задаче должны быть назначены ответственные лица, которые будут следить за её выполнением.

#### 4. Создание базы данных:
- Проектирование БД: В рамках проекта должна быть разработана база данных, соответствующая требованиям приложения.
- Схема базы данных: Создание схемы базы данных, которая должна включать все необходимые таблицы, их связи и атрибуты. Схема должна быть доступна в виде визуального представления (например, в формате ER-диаграммы) и включать:
  - Названия таблиц.
  - Типы данных для каждого поля.
  - Связи между таблицами (первичные и внешние ключи).
  - Описание каждого поля и его назначения.

#### 5. Решение опубликовано на бесплатном хостинге


Регистрация участника
- Я как пользователь (участник) имею возможность:
  - Зарегистрироваться на мероприятии, предоставив необходимые личные данные.
  - Подтвердить свою учетную запись через электронную почту.
  - Просмотреть и редактировать свои регистрационные данные в любом времени.
  - Получить уведомления о статусе своей регистрации и о предстоящих мероприятиях.

Функциональность:
- Выбор мероприятия:
  - На первом шаге пользователь выбирает мероприятие из предложенного списка (например, "Конференция 1", "Семинар", и т.д.).

- Форма заявки:
  После выбора мероприятия пользователю предлагается заполнить следующие поля:
  1. ФИО (текстовое поле).
  2. Факультет обучения (выпадающий список из предложенных факультетов).
  3. Курс (выпадающий список из возможных курсов).
  4. Преподаватель (выпадающий список из предложенных преподавателей).
  5. Секция выступления (выпадающий список из доступных секций).
  6. Тема выступления (текстовое поле).
  7. Уровень учебника по английскому языку (выпадающий список).
  8. Участвую на переводчиках (да/нет).
  9. Наличие образования переводчика (да/нет).
  10. Электронная почта (текстовое поле).

- Форма регистрации группы:
  После выбора мероприятия пользователю предлагается заполнить следующие поля:

  1. Информация о группе:
     - Название группы (текстовое поле).
     - Количество участников (числовое поле).

  2. Сведения о каждом участнике:
     - ФИО (текстовое поле для ввода).
     - Факультет (выпадающий список).
     - Курс (выпадающий список).
     - Преподаватель (выпадающий список).
     - Секция выступления (выпадающий список).
     - Тема выступления (текстовое поле).
     - Уровень учебника по английскому языку (выпадающий список).
     - Участвую на переводчиках (да/нет, для каждого участника).
     - Наличие образования переводчика (да/нет, для каждого участника).
     - Электронная почта (текстовое поле).

#### 3. Регистрация и уведомления:
- Проверка данных: Бот должен обеспечивать проверку данных и возможность редактирования информации о каждом участнике до окончательной отправки.
- Отправка информации: После заполнения всех полей бот должен отправить информацию организаторам на электронную почту с данными о группе и каждом участнике в виде таблицы.
- Тема письма: "[Название мероприятия] [Год] [Название группы] [Количество участников]".
- Уведомление участникам: Бот отправляет уведомление на указанную почту и в Telegram каждому участнику группы с подтверждением регистрации.

- Регистрация и уведомления:
  - После заполнения всех полей, бот отправляет информацию организаторам на электронную почту в формате таблицы.
  - Тема письма: "[Название мероприятия] [Год] [Фамилия студента, инициалы] [Аббревиатура факультета]".
  - Также отправляется уведомление студенту на указанную почту и в Telegram с подтверждением регистрации.

Режим организатора
- Я как пользователь (организатор) имею возможность:
  - Формировать программу мероприятия на основе введенной информации о секциях и участниках.
  - Редактировать программу перед её окончательным утверждением и публикацией.
  - Получать итоговые документы программы в форматах PDF или DOC для дальнейшего распространения среди участников.

Режим организатора для чат-бота по регистрации участников

Режим организатора предназначен для управления мероприятием, обработки заявок участников и получения статистики. Главные функции и команды, доступные в этом режиме, включают:

#### 1. Основной интерфейс организатора:
- Авторизация: Организатор должен пройти процедуру авторизации для доступа к режиму, например, с помощью кода доступа или ключа.
- Главное меню: После входа в режим организатора пользователю будет представлено главное меню с выбором функций.

#### 2. Основные функции:
1. Управление мероприятиями:
   - Добавить мероприятие: Организатор может вводить новое мероприятие, указывая название, дату, описание и секции.
   - Изменить/удалить мероприятие: Возможность редактирования или удаления существующих мероприятий.

2. Просмотр заявок участников:
   - Список зарегистрированных участников: Организатор может просмотреть список всех зарегистрированных участников с возможностью фильтрации по мероприятию.
   - Информация об участнике: При выборе участника отображается полная информация из заявки (ФИО, факультет, курс, тема выступления и пр.).

3. Формирование итогового документа:
   - Сформировать программу мероприятия: По команде бот генерирует итоговый документ (DOC и PDF) с полным списком участников и метаинформацией по докладам.
   - Отправить программу: Возможность отправить сформированный документ на указанную почту организатора.
### Требования к внесению информации по оргкомитету и мероприятию

При формировании программы мероприятия организатор должен также внести необходимую информацию по оргкомитету и самой программе мероприятия. 

#### 1. Ввод информации по оргкомитету:
Организатор должен иметь возможность вводить данные по членам оргкомитета, который отвечает за проведение мероприятия. Ввод информации включает следующие поля:

1. Состав оргкомитета:
   - ФИО члена оргкомитета: Поле для ввода полного имени каждого члена.
   - Степень: (если применимо) Выпадающий список с уровнями (например, "Кандидат наук", "Доктор наук").
   - Звание: Поле для указания должности (например, "Доцент", "Профессор").
   - Должность: Поле для указания должности в оргкомитете (например, "Координатор", "Секретарь").
   - Контактная информация: Поле для ввода телефонного номера и электронной почты.

2. Добавление членов оргкомитета:
   - Возможность добавления нескольких членов оргкомитета, включая кнопку "Добавить члена оргкомитета" для создания новых полей ввода.

3. Удаление и редактирование членов оргкомитета:
   - Кнопки для удаления или редактирования информации о каждом члене оргкомитета.

#### 2. Ввод информации о мероприятии:
Организатор должен ввести подробную информацию о мероприятии, включающую:

1. Название мероприятия:
   - Поле для ввода названия мероприятия (например, "Научная конференция 2023").

2. Тип мероприятия:
   - Выпадающий список с типами мероприятий (например, "Конференция", "Семинар", "Круглый стол").

3. Дата и время проведения:
   - Дата: Поле для ввода даты (формат: ДД.ММ.ГГГГ).
   - Время: Поля для ввода времени начала и окончания мероприятия (например, "09:00 - 17:00").

4. Место проведения:
   - Поле для ввода места проведения (например, "Город, улица, здание").

5. Описание мероприятия:
   - Текстовое поле для краткого описания мероприятия, его целей и задач.

6. Контакты организатора:
   - Поля для ввода имени контактного лица, его должности, рабочего телефона и электронной почты.

#### 3. Проверка и сохранение информации:
- Проверка заполненных данных: Перед сохранением информации бот должен проверять на корректность и полноту введенную информацию.
- Сохранение данных: После завершения ввода организатор должен сохранить введенную информацию в базе данных для дальнейшего использования при формировании программы мероприятия.
### Требования к функционалу для формирования программы мероприятия с учетом секций

#### 1. Ввод данных по секциям:
При формировании программы организатор должен иметь возможность ввести данные для каждой секции мероприятия:

1. Название секции:
   - Поле для ввода текстового названия секции (например, "Научные исследования", "Методические разработки").

2. Жюри:
   - ФИО жюри: Поле для ввода полного имени.
   - Если жюри является сотрудником СГУ:
     - Степень: Выпадающий список с уровнями (например, "Кандидат наук", "Доктор наук").
     - Звание: Поле для ввода должности (например, "Доцент", "Профессор").
     - Должность: Поле для указания текущей должности.
   - Если жюри не является сотрудником СГУ:
     - Степень: Поле для ввода степени, если есть (например, "Кандидат наук").
     - Место работы: Поле для ввода названия организации.
     - Должность: Поле для указания текущей должности.

3. Данные по председателю жюри:
   - ФИО председателя: Поле для ввода полного имени председателя.
   - Если председатель является сотрудником СГУ:
     - Степень: Выпадающий список с уровнями.
     - Звание: Поле для ввода должности.
     - Должность: Поле для указания текущей должности.
   - Если председатель не является сотрудником СГУ:
     - Степень: Поле для ввода степени, если есть.
     - Место работы: Поле для ввода названия организации.
     - Должность: Поле для указания текущей должности.

4. Дата проведения и аудитория:
   - Дата: Выбор даты из календаря или текстовое поле для ввода (формат: ДД.ММ.ГГГГ).
   - Аудитория: Поле для ввода номера аудитории (например, "Ауд. 101").

5. Количество участников:
   - Поле для ввода общего количества участников секции (числовое поле).

#### 2. Обработка участников:
- При задании количества участников и формировании программы, бот должен проверять общее количество зарегистрированных участников. 
- Предупреждение о разделении:
  - Если количество участников больше 10, бот должен делить их на несколько равных групп, учитывая, что в каждой группе должно быть не более 10 докладов.
  - Например, если зарегистрировано 25 участников, они будут разделены на 3 группы: 
    - Первая группа — 9 участников,
    - Вторая группа — 8 участников,
    - Третья группа — 8 участников.

#### 3. Вывод программы мероприятия:
- Итоговая программа должна содержать:
  - Названия всех секций.
  - Списки членов жюри для каждой секции с их данными.
  - Дата и аудитория для каждой секции.
  - Списки участников, сгруппированные по секциям с указанием количества докладов в каждой группе.

#### 4. Генерация и отправка итогового документа:
- После ввода всех данных организатор может сгенерировать итоговой документ (DOC и PDF) с программой мероприятия, который будет содержать всю указанную информацию о секциях и участниках.
- Итоговый документ отправляется организатору по электронной почте по команде, например, "Сформировать программу мероприятия".

### Дополнительные пожелания:
- Интерфейс ввода: Бот должен предоставлять интуитивно понятный интерфейс для ввода данных по секциям и участникам.
- Валидация данных: Проверка корректности введенных данных (например, проверки на пустые поля, формат даты и т.д.).
- История изменений: Возможность отслеживать изменения данных (при редактировании секций или участников). 

4. Получение статистики:
   - Получить статистический отчет: Организатор может запросить отчет по участникам с разбивкой по критериям (факультет, курс, преподаватель и пр.).
   - Графическое отображение: Отчет будет представлен в виде круговых диаграмм с процентами и количественным соотношением.

5. Уведомления:
   - Просмотр уведомлений: Организатор может просмотреть уведомления, отправленные участникам, включая подтверждения регистрации.
   - Отправка сообщений участникам: Возможность отправки сообщений или уведомлений непосредственно участникам.

6. Настройки бота:
   - Обновить список преподавателей и факультетов: Организатор может добавлять или удалять преподавателей и факультеты, доступные для выбора участниками.
   - Настройки уведомлений: Настройка формата и текста уведомлений, отправляемых участникам.

#### 3. Удобный интерфейс:
- Командный ввод: Все функции должны быть доступны через простые текстовые команды или кнопки.
- Подсказки: Бот должен предоставлять подсказки и инструкции по использованию каждой функции, чтобы организатор не запутался в функционале.

#### 4. Безопасность:
- Защита данных: Доступ к режиму организатора должен быть заблокирован от несанкционированного доступа, а все действия должны быть защищены паролем или другим методом аутентификации.
- Хранение данных участников: Организатор должен иметь доступ только к необходимой информации и во избежание утечки данных соблюдать правила конфиденциальности.



Жеребьевка
- Я как пользователь (организатор) имею возможность:
  - Запускать процесс жеребьевки тем для участников.
  - Загружать и редактировать доступные темы для жеребьевки.
  - Просматривать результаты жеребьевки и распределение тем между группами участников.
  - Отправлять уведомления участникам о назначенных темах и технических требованиях.
#### 1. Общие требования к режиму жеребьевки:
- Режим предназначен для случайного распределения заранее определенных тем среди зарегистрированных групп участников.
- Жеребьевка должна быть справедливой и обеспечивать равные условия для всех групп.
- После жеребьевки группы должны получить уведомления с информацией о назначенной теме и техническими требованиями к оформлению работы.

#### 2. Подготовка к жеребьевке:
- Задание тем: Администраторы должны заранее вводить в систему доступные темы для мероприятий «Плакаты 1» и «Плакаты 2». Темы должны быть структурированы так, чтобы их можно было легко распределить между зарегистрированными группами.

- Регистрация групп: Система должна хранить информацию о всех зарегистрированных группах-участниках, включая их представителей и контактные данные.

#### 3. Процесс жеребьевки:
1. Запуск жеребьевки: 
   - Организатор инициирует процесс жеребьевки через команду (например, "Запустить жеребьевку тем").

2. Случайное распределение тем:
   - Система должна случайным образом назначить каждую из доступных тем группе участников.
   - Если количество тем меньше количества групп, следует реализовать логику отправки сообщений о том, что некоторым группам могут не достаться темы.
   - В случае избыточного количества тем, их можно распределить по принципу "темы многопоточности", так чтобы одна и та же группа могла получить несколько тем (при необходимости).

3. Фиксация результатов: 
   - После завершения жеребьевки система сохраняет информацию о распределении тем по группам.

#### 4. Уведомление участников:
- Генерация уведомлений: 
  - Для каждой группы после жеребьевки система должна автоматически сформировать уведомление, содержащее:
    - Название мероприятия.
    - Год проведения.
    - Название группы.
    - Назначенная тема.
    - Технические требования к оформлению работы (например, формат, размеры, содержание плакатов и ссылки на вспомогательные ресурсы).

- Отправка уведомлений:
  - Уведомления должны быть отправлены на электронные почты всех участников группы, а также руководителю группы.
  - Тема письма должна быть оформлена следующим образом: 
    - "[Название мероприятия + год проведения] [Название группы] - Результаты жеребьевки".



Оценка докладов
- Я как пользователь (член жюри) имею возможность:
  - Входить в режим оценки докладов с авторизацией по коду доступа.
  - Выбирать выступление для оценки из списка участников.
  - Выставлять оценки по пяти критериям и оставлять комментарии.
  - Просматривать итоговую таблицу с результатами и комментариями от других членов жюри.
  - Редактировать результаты оценок (только для председателя жюри) и фиксировать окончательные итоги.
### Требования к режиму оценки докладов

#### 1. Общие требования:
- Режим оценки добродетельно должен быть закрытым и доступен только по коду доступа.
- Гарантия конфиденциальности данных и результатов оценки.
- Доступ к режиму должен иметь только члены жюри и председатель жюри.

#### 2. Авторизация:
- Ввод кода доступа: Оценивающий должен ввести уникальный код доступа для входа в режим оценки.
- Выбор жюри: После авторизации оценивающий выбирает себя из заранее подготовленного списка членов жюри, имеющих право на оценку.

#### 3. Режим оценки:
1. Выбор выступления для оценки: 
   - Оценивающий выбирает выступление (по номеру или ФИО участника) из списка выступлений, доступного для оценки.

2. Выставление оценок по критериям:
   - Оценивающий последовательно выставляет оценки по заранее определенным критериям, каждый из которых имеет шкалу от 0 до 4:
     - Organization (0-4 балла): Оценивается логичность и целостность выступления.
     - Content (0-4 балла): Оценивается уровень понимания темы выступающим.
     - Visuals (0-4 балла): Оценивается оформление презентации (соответствие ключевым моментам, отсутствие излишнего текста).
     - Mechanics (0-4 балла): Оценивается правильность речи (грамматика, произношение).
     - Delivery (0-4 балла): Оценивается уверенность и выразительность презентации.

3. Расшифровка критериев:
   - При выборе каждого критерия оценивающий получает небольшую расшифровку, объясняющую, что именно учитывается в данной категории.

4. Итоговая оценка:
   - После выставления всех критерия оценивающий нажимает кнопку "Итог", и система автоматически рассчитывает итоговый балл.

5. Комментарии:
   - Оценивающий может оставить комментарии к оценке, указав особые замечания по выступлению.

#### 4. Просмотр итоговой таблицы:
- Доступ к результатам: 
  - Председатель жюри и каждый из членов жюри могут видеть итоговую таблицу, которая отображает результаты всех выступлений в секции. Таблица включает:
    - Номера выступлений.
    - ФИО участников.
    - Темы работ.
    - Итоговые баллы.
    - Комментарии от каждого члена жюри.

- Сортировка: Результаты в таблице должны быть автоматически отсортированы в порядке убывания итоговых баллов.

#### 5. Редактирование результатов:
- Право редактирования: Только председатель жюри имеет право редактировать результаты через специальную команду, избегая случайных правок другими членами жюри.

#### 6. Финальная фиксация результатов:
- После завершения оценки председатель жюри фиксирует результаты, что влечет за собой автоматическую отправку письма организаторам мероприятия.

#### 7. Письмо организаторам:
Письмо будет содержать:
- Дата проведения мероприятия.
- Место проведения.
- Название мероприятия.
- Название секции.
- ФИО председателя жюри и членов жюри.
- Распределение мест между участниками, выделяя первые три места жирным шрифтом.

### Дополнительные пожелания:
- Интуитивно понятный интерфейс: Удобный и простой интерфейс для жюри, чтобы облегчить процесс выставления оценок и просмотра результатов.
- Защита данных: Необходимость в шифровании и защите личной информации участников и оценок.
- Логирование действий: Ведение журнала действий для аудита и отслеживания изменений, если они происходили.

### Дополнимая информация к режиму оценки докладов

При формировании итоговой таблицы результатов необходимо учитывать случаи, когда несколько участников получают одинаковые баллы. В таких ситуациях описывается следующий порядок действий:

#### 1. Обработка одинаковых результатов:
- При наличии одинаковых итоговых баллов у нескольких участников необходимо их выделить и отсортировать по алфавиту.

#### 2. Пример сортировки и представления результатов:
- Итоговая таблица должна правильно отображать участников с одинаковыми баллами. Если два или более участника получили одинаковые результаты, они должны иметь одинаковый номер и быть перечислены по алфавиту. Пример:

1. Иванов АА - 20 баллов
1. Жуков ПП - 20 баллов
2. Панфилов ФФ - 19 баллов

#### 3. Примечания в итоговой таблице:
- В финальной таблице следует добавить примечание о том, что участники с одинаковыми баллами были отсортированы в алфавитном порядке.
- Можно добавить в таблицу пояснительную записку или комментарий, указывающий, что участники с одинаковыми результатами имеют одинаковый ранг, что повышает уровень понимания итогов для организаторов и участников.

#### 4. Автоматизация:
- Система должна автоматически определять, когда два или более участника имеют одинаковые баллы, и осуществлять их сортировку по алфавиту без необходимости ручного вмешательства.