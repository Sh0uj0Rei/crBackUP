document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM загружен!");

    const form = document.getElementById("loanForm");

    // Обработчик отправки формы
    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Предотвращаем стандартную отправку формы
            console.log("Форма отправлена!");

            // Собираем данные из формы
            const formData = new FormData(form);

            // Отправляем данные на сервер
            fetch("/", {
                method: "POST",
                body: formData,
            })
                .then((response) => response.text())
                .then((html) => {
                    // Обновляем страницу с новыми данными
                    document.body.innerHTML = html;
                    console.log("Данные обновлены!");
                })
                .catch((error) => {
                    console.error("Ошибка при отправке формы:", error);
                });
        });
    }

    // Скачивание таблицы как изображения
    const downloadTableImageButton = document.getElementById("downloadTableImage");
    if (downloadTableImageButton) {
        downloadTableImageButton.addEventListener("click", function () {
            console.log("Нажата кнопка скачивания изображения");
            const paymentTable = document.getElementById("paymentTable");

            if (paymentTable) {
                console.log("Таблица найдена, начинаем создание изображения...");
                html2canvas(paymentTable).then((canvas) => {
                    console.log("Изображение создано, создаем ссылку для скачивания...");
                    const link = document.createElement("a");
                    link.download = "таблица_выплат.png";
                    link.href = canvas.toDataURL("image/png");
                    link.click();
                    console.log("Изображение скачано!");
                }).catch((error) => {
                    console.error("Ошибка при создании изображения:", error);
                });
            } else {
                console.error("Таблица не найдена!");
            }
        });
    }

    // Скачивание таблицы как CSV
    const downloadTableCSVButton = document.getElementById("downloadTableCSV");
    if (downloadTableCSVButton) {
        downloadTableCSVButton.addEventListener("click", function () {
            console.log("Нажата кнопка скачивания CSV");
            const table = document.getElementById("paymentTable");

            if (table) {
                console.log("Таблица найдена, создаем CSV...");
                let csvContent = "data:text/csv;charset=utf-8,";

                // Проходим по строкам таблицы
                table.querySelectorAll("tr").forEach(row => {
                    const rowData = [];
                    row.querySelectorAll("th, td").forEach(cell => {
                        rowData.push(cell.innerText);
                    });
                    csvContent += rowData.join(",") + "\n";
                });

                // Создаем ссылку для скачивания
                const encodedUri = encodeURI(csvContent);
                const link = document.createElement("a");
                link.setAttribute("href", encodedUri);
                link.setAttribute("download", "таблица_выплат.csv");
                document.body.appendChild(link);
                link.click();
                console.log("CSV скачан!");
            } else {
                console.error("Таблица не найдена!");
            }
        });
    }

    // Скачивание таблицы как Excel
    const downloadTableExcelButton = document.getElementById("downloadTableExcel");
    if (downloadTableExcelButton) {
        downloadTableExcelButton.addEventListener("click", function () {
            console.log("Нажата кнопка скачивания Excel");
            const table = document.getElementById("paymentTable");

            if (table) {
                console.log("Таблица найдена, создаем Excel...");
                const workbook = XLSX.utils.table_to_book(table);
                XLSX.writeFile(workbook, "таблица_выплат.xlsx");
                console.log("Excel скачан!");
            } else {
                console.error("Таблица не найдена!");
            }
        });
    }
});