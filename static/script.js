document.addEventListener('DOMContentLoaded', function () {
    // Кнопка для импорта предохранителей
    const importBtn = document.getElementById('import-btn');
    if (importBtn) {
        importBtn.addEventListener('click', () => {
            fetch('/import_fuses', { method: 'POST' })
                .then(response => response.json())
                .then(data => alert(data.message || data.error))
                .catch(() => alert('Error importing data'));
        });
    }

    // Сохранение предохранителя в профиль
    document.querySelectorAll('.save-btn').forEach(button => {
        button.addEventListener('click', () => {
            const fuseId = button.dataset.fuseId;

            fetch(`/save_to_profile/${fuseId}`, {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                } else {
                    alert('Failed to save the fuse.');
                }
            })
            .catch(() => alert('An error occurred.'));
        });
    });

    // Динамический поиск по названию
    const searchInput = document.getElementById('search');
    const searchResultsDiv = document.getElementById('search-results');

    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();

        if (query.length > 0) {
            // Отправка запроса на сервер для поиска предохранителей по названию
            fetch(`/search_fuse?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchResultsDiv.innerHTML = '';

                    if (data.fuses && data.fuses.length > 0) {
                        data.fuses.forEach(fuse => {
                            const fuseElement = document.createElement('div');
                            fuseElement.classList.add('fuse-card');
                            fuseElement.innerHTML = `
                                <h3>${fuse.name}</h3>
                                <p><strong>Price:</strong> ${fuse.price} RUB</p>
                                <p><strong>Types:</strong> ${fuse.types.join(', ')}</p>
                            `;
                            searchResultsDiv.appendChild(fuseElement);
                        });
                    } else {
                        searchResultsDiv.innerHTML = '<p>No fuses found.</p>';
                    }
                })
                .catch(error => {
                    searchResultsDiv.innerHTML = '<p>Error fetching data.</p>';
                });
        } else {
            searchResultsDiv.innerHTML = '';
        }
    });
});
