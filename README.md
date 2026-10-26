# Поиск работы Frontend-разработчиком — IT-ПАРК

Практическая методичка для выпускников Web-курса без коммерческого опыта: от выбора Junior Frontend / Intern / Junior React до резюме, портфолио, откликов, интервью и оффера.

**[Читать опубликованный handbook](https://itpark32.github.io/web-14-job-offer/)** · [Шаблоны](docs/templates/index.md) · [План первой недели](docs/getting-started/plan.md)

## Два руководства

- [web-14-metodichka](https://itpark32.github.io/web-14-metodichka/) — обучение, повторение и технические упражнения.
- Этот handbook — действия кандидата, материалы, процесс поиска и подготовка к назначенному этапу.

Техническая теория не копируется. [Маршрутизатор](docs/technical/developer.md) ведёт в соответствующие блоки Web-методички. Fullstack/PHP — дополнительная траектория с отдельным CV.

## Локальный запуск

Нужны Python 3.10+ с `venv` и Git; CI использует Python 3.12. Первая установка требует PyPI.

```bash
git clone https://github.com/itpark32/web-14-job-offer.git
cd web-14-job-offer
python3 scripts/docs.py serve
```

Откройте [локальный сайт](http://127.0.0.1:8000/web-14-job-offer/). Скрипт сам создаёт `.venv` и устанавливает закреплённые зависимости. В Windows можно использовать `py`, в средах с `python` — это имя вместо `python3`. Остановка — Ctrl+C.

```bash
python3 scripts/docs.py serve --dev-addr 127.0.0.1:8001
```

## Проверки и сборка

| Команда | Результат |
|---|---|
| `python3 scripts/docs.py bootstrap` | Подготовка окружения, установка lock, pip check |
| `python3 scripts/docs.py build` | Строгая сборка в `site/` |
| `python3 scripts/docs.py check` | Полнота nav, законченные страницы, строгая сборка, внутренние ссылки, якоря и ресурсы |
| `.venv/bin/python scripts/check_theory_links.py` | HTTP-проверка всех ссылок на техническую Web-методичку, соответствие заголовкам |
| `git diff --check` | Проверка пробельных ошибок diff |

В Windows для отдельного скрипта используйте `.venv/Scripts/python.exe`. Внешняя проверка требует сети и запускается отдельно: ошибки сторонних ресурсов не должны мешать локальной работе. Скрипт возвращает ошибку при недоступном учебном маршруте.

## Структура

```text
docs/index.md, about.md     # начало и связь двух руководств
docs/getting-started/      # рынок, цель, первая работа, неделя
docs/resume/               # CV, GitHub, портфолио, проекты курса, demo
docs/job-search/           # вакансии, отклики, HR, follow-up, воронка
docs/interviews/           # этапы, проект, live coding, review, debugging,
                           # верстка, тестовое, STAR, вопросы команде
docs/technical/developer.md # маршрутизатор в техническую методичку
docs/salary/               # ожидания, переговоры, оффер
docs/templates/            # копируемые формы и пустой job-tracker.csv
docs/resources/sources.md  # источники, даты и ограничения
scripts/                   # запуск, сборка, проверки
mkdocs.yml                 # Material, поиск ru/en, темы, nav, toc
.github/workflows/ci.yml   # проверка и Pages deployment
REVIEW.md                  # карта выполненной миграции и проверок
```

Сохранены Material for MkDocs, светлая/тёмная темы, поиск, sidebar, оглавление, admonition, таблицы, чек-листы, копирование кода и git-даты. В архиве без истории даты отключаются автоматически; они не являются датой проверки источников. Для отключения: `ENABLE_GIT_DATES=false`.

## CI/CD и GitHub Pages

Push в `main` запускает проверку, сборку и публикацию через официальный GitHub Pages artifact flow. Pull request выполняет только проверку. Deployment использует environment `github-pages`, `pages: write`, `id-token: write` и concurrency; исходный контент workflow менять не может (`contents: read`).

В [Settings → Pages](https://github.com/itpark32/web-14-job-offer/settings/pages) выбран **Source: GitHub Actions**. Публикуется проверенный каталог `site/` через `actions/upload-pages-artifact` и `actions/deploy-pages`. Ветка `gh-pages` и `mkdocs gh-deploy` не используются.

[Статус Actions](https://github.com/itpark32/web-14-job-offer/actions) · [Официальная документация custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

Если deploy упал, сначала откройте logs build/deploy. Сверьте Pages Source, permissions и environment; исправьте причину, затем повторите запуск. После deploy откройте главную и вложенную страницу, проверьте поиск, темы, mobile и ссылки.

## Редактирование

Каждая новая Markdown-страница должна быть в `nav` ровно один раз, содержать один H1 и конкретный результат для кандидата. Между страницами используйте относительные ссылки на `.md`. Для технических объяснений давайте проверенный URL Web-методички. Изменяющиеся факты сопровождайте первичным источником, датой, периодом и ограничениями. Не выдавайте учебные примеры за достижения читателя.

После изменений запускайте `check`; после правки внешних технических ссылок — `check_theory_links.py`. Зависимости обновляйте осознанно в отдельном окружении с повторной проверкой; `requirements.in` содержит прямые зависимости, `requirements.txt` — полный lock. `.venv/`, `site/`, cache и секреты не коммитятся.

## Основа проекта

Методичка создана на базе структуры и инфраструктуры проекта
[1ommyS/itp-work-handbook](https://github.com/1ommyS/itp-work-handbook)
и адаптирована для выпускников Web-курса IT-ПАРК.

История исходника сохранена. Исходная точка: `869d83ebd7b39089e6390a68b3cc1a0cd5e2e69d`. Лицензия от имени адаптации не добавлена. Названия и исходные возможности проектов курса сверены с исторической страницей `docs/projects.md`, удалённой из текущей Web-методички; на сайте дана рабочая ссылка на историю.
