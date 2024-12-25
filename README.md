## Проект по автоматизации мобильного приложения БГ "СПАС"


### Используемые инструменты
<div>
<img src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" title="python" alt="python" width="40" height="40"/>&nbsp
<img src="https://user-images.githubusercontent.com/25181517/184117132-9e89a93b-65fb-47c3-91e7-7d0f99e7c066.png" title="pytest" alt="pytest" width="40" height="40"/>&nbsp
<img src="https://user-images.githubusercontent.com/25181517/184103699-d1b83c07-2d83-4d99-9a1e-83bd89e08117.png" title="selene" alt="selene" width="40" height="40"/>&nbsp
<img src="https://img.icons8.com/?size=100&id=3tC9EQumUAuq&format=png&color=000000" title="github" alt="github" width="40" height="40"/>&nbsp
<img src="https://user-images.githubusercontent.com/25181517/179090274-733373ef-3b59-4f28-9ecb-244bea700932.png" title="jenkins" alt="jenkins" width="40" height="40"/>&nbsp
<img src="https://molecula.gallerycdn.vsassets.io/extensions/molecula/allure-test-reports/1.1/1474455326332/Microsoft.VisualStudio.Services.Icons.Default" title="allure" alt="allure" width="40" height="40"/>&nbsp
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/pycharm/pycharm-original.svg" title="pycharm" alt="pycharm" width="40" height="40"/>&nbsp
<img src="https://cdn-icons-png.flaticon.com/512/2111/2111646.png" title="telegram" alt="telegram" width="40" height="40"/>&nbsp
</div>

## Запуск тестов и получение отчета

### **Локально**

<details><summary>1. Склонировать репозиторий</summary>

```
git clone https://github.com/msborja/bg_spas
```
</details>

<details><summary>2. Установить зависимости и запустить тесты</summary>

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest .
```
</details>

<details><summary>3. Получить отчет о прохождении тестов в allure</summary>

```
allure serve allure-results/
```
</details>

<details><summary>4. После выполнения команды откроется браузер с отчетом</summary>
    
<img src="resources/allure-report.png">

</details>

### **Удалённо**

Удаленный запуск автотестов осуществляется при помощи Jenkins. Для этого необходимо выполнить следующие действия:

<details><summary>1. Открыть [проект в Jenkins]</summary> 

(https://jenkins.autotests.cloud/job/python_qa_bg_spas/)

</details>

<details><summary>2. Нажать на кнопку "Build with Parameters"</summary>

<img src="resources/jenkins.png">

</details>

<details><summary>3. Дождаться окончания выполнения автотестов и нажать на иконку allure <img src="https://molecula.gallerycdn.vsassets.io/extensions/molecula/allure-test-reports/1.1/1474455326332/Microsoft.VisualStudio.Services.Icons.Default" title="allure" alt="allure" width="20" height="20"/> для просмотра отчета</summary>

<img src="resources/jenkins2.png">

</details>

## **Дополнительно**

Реализована отправка результатов тестирования в Telegram <img src="https://cdn-icons-png.flaticon.com/512/2111/2111646.png" title="telegram" alt="telegram" width="20" height="20"/>  
<details><summary>Пример отчета</summary>

<img src="resources/telegram-report.png" alt="report Telegram">

</details>